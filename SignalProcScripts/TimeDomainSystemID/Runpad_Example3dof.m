%======== MATLAB Demo ====================================================
% Eleni N. Chatzi, Minas Spiridonakos, Institute of Structural Engineering,
% ETH Zurich                                                03.06.2013
%======== Define the 3DOF System (linear) ================================  
% Perform ERA (Eigenvalue Realization Algorithm) on impulse response data 
% of a 3DOF linear mechanical system.

clear all; close all; clc;
addpath([pwd, '/Source']);  % Add custom source code directory to path

global fs sys V  % Define global variables for sampling frequency, system, and mode shapes

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Data generation & System simulation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%---------------- System Matrices ----------------%
% Mass Matrix [kg]
M = 0.001 * eye(3);  % 3 DOFs with equal mass

% Stiffness Matrix [N/m]
K = [ 4  -2   0;
     -2   4  -2;
      0  -2   2];

% Damping Ratio (per mode)
xi = 0.02;  % 2% modal damping

%---------------- Modal Properties ----------------%
% Solve generalized eigenvalue problem for undamped free vibration
[V, D] = eig(K, M);  % V: mode shapes (mass-normalized), D: eigenvalues (omega^2)
w = sqrt(diag(D));   % Natural frequencies (rad/s)

%---------------- Rayleigh Damping ----------------%
% Rayleigh damping coefficients α and β from two natural frequencies
beta = 2 * xi / (w(1) + w(2));
alpha = 2 * xi * w(1) - beta * w(1)^2;

% Damping Matrix: C = α*M + β*K
C = alpha * M + beta * K;

%---------------- Discrete Time Info ----------------%
fs = 100;             % Sampling frequency [Hz] (must be > 2*f_max)
dt = 1 / fs;          % Time step [s]
Ttot = 10;            % Total simulation time [s]
time = 0:dt:Ttot;     % Time vector
N = length(time);     % Number of time samples

%======== Define the Excitation Type ===========================
inptype = 'imp';  % Options: 'imp', 'WN', 'known'

switch inptype
    % --- Case A: Unit impulse input ---
    case 'imp'
        f = zeros(N,1);
        f(1) = 1;  % Unit impulse at t = 0

    % --- Case B: White noise input (ambient excitation) ---
    case 'WN'
        f = 100 * randn(N,1);  % White noise input
        ref = 1;  % Reference channel for cross-correlation (if needed)

    % --- Case C: Known random excitation (e.g., earthquake) ---
    case 'known'
        f = 1000 * randn(N,1);  % Scaled random excitation
end

%======== Continuous-Time State-Space Model ===================
% State vector: [x; x_dot]
Ac = [zeros(3), eye(3);
     -inv(M)*K, -inv(M)*C];

% Print modal frequencies and damping of system (for validation)
[Wn, zeta] = damp(Ac);
disp('Frequencies of the real system (Hz):');
disp(Wn([6 4 2]) / (2*pi));  % Select meaningful modal indices

% Input matrix: assume force acts on all masses equally
Bc = [zeros(3,1); diag(inv(M))];

% Output matrix: assuming acceleration measurement
Cc = [-inv(M)*K, -inv(M)*C];
Dc = zeros(3,1);  % No direct feedthrough

% Create continuous-time state-space system
sys = ss(Ac, Bc, Cc, Dc);

% Simulate system response to excitation f
[Y, T, X] = lsim(sys, f, time, zeros(6,1));
output = Y;  % Measurement output (e.g., accelerations)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Frequency Analysis & ERA identification
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%======== Frequency Analysis (Welch PSD Estimate) ================
figure;
pwelch(Y(:,3), [], [], [], fs);  % Power spectral density of DOF 3 response

%======== ERA Identification ====================================
nch = size(Y, 2);       % Number of output channels
L = length(time);       % Number of time samples
Nfft = 2^(nextpow2(L)-1);  % FFT size for analysis

ndof = 3;  % Number of modes to identify

% Define size of Hankel matrix (depends on excitation type)
switch inptype
    case 'WN'
        order = 15;    % Shorter for ambient
    case 'known'
        order = 100;   % Larger for broadband input
    otherwise
        order = 50;    % Default
end

% Run the ERA routine (external script)
Run_ERA_NEXT_3dof

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Stochastic Subspace Identification
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%======== SSI Method (optional) ==================================
% Run_n4sid_3dof  % Uncomment to run subspace identification

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% AutoRegressive Moving Average model Identification
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%======== ARMA Model Identification ==============================
% Fit ARMA model to 3rd DOF output displacement
nmin = 4;     % Minimum ARMA order
nmax = 12;    % Maximum ARMA order

[th, modal] = runARMA(output(:,3), dt, nmin, nmax);

% Display modal frequencies and damping
disp('Frequencies (Hz) and Damping:');
disp(modal);
