%======== MATLAB Demo ====================================================
% Eleni N. Chatzi, Minas Spiridonakos, Institute of Sructural Engineering,
% ETH Zurich                                                03.06.2013
%======== Define the 3dof System (linear) ================================  
% Perform ERA on impulse (free response) data of 3dof system
clear all;close all;clc;
global fs sys

% Mass Matrix
M=.001*[1 0 0;0 1 0;0 0 1];

% Stiffness Matrix
K=[4 -2 0;-2 4 -2;0 -2 2];

% Damping ratio  (\zeta_i)
xi=0.02;

%======== Natural Frequencies, Modes ====================== 
% Solve the eigenvalue problem
[V,D]=eig(K,M); %V:eigenvectors, D:eigenvalues(=w^2)
% Note: The Eigenvectors V are already Mass Normalized in MATLAB

% Natural Frequencies
w=[sqrt(D(1,1)) sqrt(D(2,2)) sqrt(D(3,3))];

%======== Define Raleigh damping ===========================
% alpha and beta
beta=2*xi/(w(1)+w(2));
alpha=2*xi*w(1)-beta*w(1)^2;

% Damping Matrix
C=alpha*M+beta*K;

% Discrete Time Domain Info
fs=500;                 %Sampling Frequency (has to be above 2*max freq expected in response signal)
dt=1/fs;                %Sampling interval
Ttot=20;                %Total analysis time in seconds
time=[0:dt:Ttot];       %Time vector for this example
N=length(time);         %Number of points

%======== Define the type of Excitation ===========================
%%%%%%%%%%%%%%% A. UNIT IMPULSE %%%%%%%%%%%%%%%
% inptype='imp';          
f=zeros(N,1);
% f(1)=1;
%%%%%%%%%%%%%%% B. White noise excitation (ambient-unmeasured) %%%%%%%%%%%%%%%
inptype='WN';       %Choose this option if input is white noise and you desire otput only id, 
% exploiting the fact that the cross correlation of response signals to any reference one satisfy the free response equation
ref=1;      %Determine the reference channel, i.e. the channel with respect to which you will obtain the cross correlation function
%%%%%%%%%%%%%%% C. Measured random excitation (could also be earthquake) %%%%%%%%%%%%%%%
% inptype='random';
f=wgn(N,1,60);
% f=100*(rand(N,1)-.5);
  
%%
%======== Continuous State Space Form ===========================

Ac=[zeros(3) eye(3);-inv(M)*K -inv(M)*C];
% print modal quantities for checking
damp(Ac)
Bc=[zeros(3,1);diag(inv(M))];
Cc=[eye(3) zeros(3);-inv(M)*K -inv(M)*C]; %assuming we measure relative displacements, relative accelerations
Dc=[zeros(3,1);diag(inv(M))];

% Simulate the discrete system using lsim
%???????????????????????????
% Question: What would be an alternative approach (defined in discrete domain) 
%???????????????????????????

sysc=ss(Ac,Bc,Cc,Dc);
[Y,T,X]=lsim(sysc,f,time,zeros(1,6));
output=Y;                     %Here you choose which measurement channels you would like to use


%%
%======== call the (linear) Kalman Filter ===========================
% The KF can function using the 1st floor displacement as measurement and
% the collocated 1st floor accaeleration as input to the state space
y=output(:,1)';               %Here we choose to observe only the 1st displacement
acc_meas=output(:,4)';

Ac2=[0 1;0 0];
Bc2=[0;1];
Cc2=[1 0];      %Assuming we measure only the first displacement
Dc2=0;
sys=ss(Ac2,Bc2,Cc2,Dc2);         %Redefine the continuous system

%=============================================================================================
 
model = define_model('init');
% pnoise = model.pNoise.sample( model.pNoise, N);   % generate process noise
% onoise = model.oNoise.sample( model.oNoise, N);   % generate observation noise

    
  %   Corrupt the observations with some white noise to simulate true case
  %   scenario
  S = chol(1e4)';
  onoise = S * randn(1,N);
  y = y+onoise;                   
  
  %--- Setup runtime buffers
  Xh = zeros(model.statedim,N);          % state estimation buffer
  Xh(:,1) = zeros(model.statedim,1);         % initial estimate of state E[X(0)]
  Px = 1e1*eye(model.statedim);         % initial state covariance, defines the cnfidence we have in the initial conditions

  
%--- Call inference algorithm / estimator --------------------------------------

%------------------- Linear Kalman Filter --------------------------------------

        [Xh, Px] = kf(Xh(:,1), Px, model.pNoise, model.oNoise, y, acc_meas, [], model);
        
%%
%========Plot Results ===========================
figure
p1 = plot(X(:,1)); hold on; grid on
p2 = plot(y(1,:),'g+');
p3 = plot(Xh(1,:),'r--'); hold off;
legend([p1 p2 p3],'clean','noisy','kf estimate');
xlabel('time');
title('Observed Noisy 1st floor Displacement');


