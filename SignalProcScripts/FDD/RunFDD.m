% =========================================================================
% Frequency Domain Decomposition (FDD)
% =========================================================================
% In this script, we simulate or analyze the dynamic response of a 3-DOF
% structure under ambient excitation. The aim is to identify modal 
% properties (natural frequencies and mode shapes) using Frequency Domain 
% Decomposition (FDD) techniques, which are commonly used in structural 
% health monitoring and experimental modal analysis.
%
% You are encouraged to:
% - Understand how the mass, stiffness, and damping matrices are defined.
% - Inspect the state-space formulation and dynamic simulation.
% - Explore the influence of different damping levels or sensor outputs.
% - Compare identified modes to theoretical ones (if synthetic data is used).
%
% Use this script as a base to analyze your own measurements on the bridge 
% structure using the roving accelerometers provided.
% =========================================================================

% Perform Frequency Domain Decomposition (FDD) on ambient excitation data of a 3-DOF system
clc; clear all; close all

%----------------------------------------------
% CHOOSE DATA SOURCE: Use existing data or generate synthetic data
%----------------------------------------------
source = 'loadData';  % Options: 'loadData' or 'create'

switch source

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % OPTION 1: Load pre-recorded ambient excitation data
    case 'loadData'
        % Load all channels (assumed 120)
        load data.dat
        Ndata = size(data,1);
        Nch = size(data,2);
        
        % Compute variance of each channel
        channel_variances = var(data);  % 1 x 120
        
        % Sort variances and keep track of original indices
        [sorted_var, sorted_idx] = sort(channel_variances, 'ascend');
        
        % Number of bins
        Nbins = 10;
        bin_size = floor(Nch / Nbins);
        
        % Select one channel from each bin (spread across variance range)
        selected_idx = zeros(1, Nbins);
        for i = 1:Nbins
            bin_start = (i-1)*bin_size + 1;
            bin_end = i*bin_size;
            bin_range = sorted_idx(bin_start:bin_end);
            
            % Randomly pick one index from the current bin
            selected_idx(i) = bin_range(randi(length(bin_range)));
        end
        
        % Extract selected 10 channels
        Y = data(:, selected_idx);

        % Sampling frequency and corresponding time vector
        in.fs = 100;                         % [Hz]
        dt = 1 / in.fs;
        time = 0:dt:(length(data)-1)*dt;     % Time vector

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % OPTION 2: Create synthetic data for a 3-DOF system
    case 'create'

        % Define system parameters
        %----------------------------------------------
        % MASS MATRIX (diagonal - lumped masses)
        M = 0.01 * eye(3);

        % STIFFNESS MATRIX (tridiagonal - spring system)
        % Represents a typical shear-building model
        K = [ 4 -2  0;
             -2  4 -2;
              0 -2  2];

        % TARGET DAMPING RATIO for all modes (assumed constant)
        xi = 0.0050;

        %----------------------------------------------
        % EIGENVALUE ANALYSIS
        [V, D] = eig(K, M);          % Solve generalized eigenvalue problem
        w = sqrt(diag(D))';          % Natural frequencies [rad/s]

        %----------------------------------------------
        % RAYLEIGH DAMPING COEFFICIENTS
        % (computed using first two modes)
        alpha = sqrt(2 * xi * w(1) * w(2) / (w(1) + w(2)));
        beta  = 2 * xi / (w(1) + w(2));
        C = alpha * M + beta * K;    % Damping matrix

        %----------------------------------------------
        % AMBIENT EXCITATION (white noise)
        f = 100 * randn(20000,1);    % External random force (e.g., wind, footsteps)

        %----------------------------------------------
        % SIMULATE SYSTEM RESPONSE
        % Create state-space model of second-order system
        in.fs = 100;                  % Sampling frequency
        dt = 1 / in.fs;
        time = 0:dt:(length(f)-1)*dt;

        % System matrices for state-space model (6 states: [x; x_dot])
        Ad = [zeros(3), eye(3); -inv(M)*K, -inv(M)*C];
        Bd = [zeros(3,1); diag(inv(M))];    % Single input force
        Cd = [eye(3), zeros(3)];            % Measure displacements

        % Optional: simulate acceleration measurements instead
        % Cd = [-inv(M)*K, -inv(M)*C];
        % Dd = diag(inv(M));

        Dd = zeros(3,1);                    % No direct feedthrough
        sys = ss(Ad, Bd, Cd, Dd);           % Build state-space system
        [Y, T, X] = lsim(sys, f, time, zeros(6,1));  % Simulate response
end

%----------------------------------------------
% OPTIONAL: Zero-padding improves frequency resolution in FFT
%----------------------------------------------
Y = [Y; zeros(size(Y))];  % Add zeros to end of signal
acce = Y;                 % Measurement matrix (each column: DOF)

%----------------------------------------------
% FDD SETUP
%----------------------------------------------
in.x = acce;           % Input signal matrix
in.DF = 0.25;          % Desired frequency resolution [Hz]
in.Nfft = 1024;        % Number of FFT points
in.fc = 10;            % Max frequency to display in plots
in.isShowingFigures = 1; % Set to 1 to display intermediate results
in.Npeaks = 3;         % Expected number of dominant modes
in.curv_cut = 0.3;     % Threshold for peak sharpness (automated picking)
in.ppm = 'manual';     % 'manual' or 'auto' peak picking
in.hw = 8;             % Half-width of fitting window for SDOF fitting

%----------------------------------------------
% RUN FDD ALGORITHM
%----------------------------------------------
out = fdd(in);         % Perform Frequency Domain Decomposition

% Output:
% out.fd  - Identified natural frequencies [Hz]
% out.phi - Corresponding mode shapes (each column is a mode)

% Display identified frequencies
out.fd;

% Mode shapes (keep real part for plotting)
phi = real(out.phi); 

%----------------------------------------------
% PLOT MODE SHAPES (identified vs analytical)
%----------------------------------------------
close all
for i = 1:size(phi,2)
    subplot(1,size(phi,2),i)

    % Normalize identified mode shape and ensure consistent direction
    [mval, ind] = max(abs(phi(:,i)));
    p1 = plot([0:size(phi,1)], [0 phi(:,i)' * sign(phi(ind,i)) / mval], 'b');
    hold on
    legend([p1], 'calculated');

    % Overlay analytical mode shape if synthetic data used
    switch source
        case 'create'
            [mval, ind] = max(abs(V(:,i)));
            p2 = plot([0:size(phi,1)], [0 V(:,i)' * sign(V(ind,i)) / mval], 'r');
            legend([p1 p2], 'calculated', 'analytical');
    end
end
