%% System Simulation
%
% Tasks:
% Create structural matrices
% Obtain an insight among different domains
% Simulate for displacement and acceleration output
% Noise corrupt the output data
% Store input-output data for further processing
%

clear
close all
clc

% create structural matrices
n = 2;
m = [1.241 4.500];  % Kg
k = [900 300 500];  % N/m
M = diag(m);
K = [k(1)+k(2) -k(2);-k(2) k(2)+k(3)];
wn = sqrt(eig(M^(-1/2)*K*M^(-1/2)));
A = [ones(length(wn),1) wn.^2];
b = 2*wn.*[0.01;0.01];
x = A\b;
C = x(1)*M + x(2)*K;
P = [0;1];

% Obtain an insight among different domains: displacement
Ac = [zeros(n) eye(n);-M\K -M\C];
Bc = [zeros(n,1);M\P];
Cc = [eye(n) zeros(n)];
Dc = 0;
sys_D_ss_c = ss(Ac,Bc,Cc,Dc); % state-space
sys_D_tf_c = tf(sys_D_ss_c);  % transfer function
figure(1)
sys_D_frf_c = bodeplot(sys_D_tf_c(1,1),'k',sys_D_tf_c(2,1),'r'); grid on % frequency response
setoptions(sys_D_frf_c,'FreqUnits','Hz','Xlim',[.1 25]);

% Obtain an insight among different domains: acceleration
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% simulate: displacement
Fs = 50;                            % Hz
Ts = 1/Fs;                          % s
N  = 2^14;                          % data points 
t  = 0:Ts:Ts*(N-1);t = t.';         % time vector
uk = 10*randn(N,1);                 % input
sys_D_ss_d = c2d(sys_D_ss_c,Ts);    % discrete-time state-space
yk_D = lsim(sys_D_ss_d,uk,t);       % response
figure(3)
subplot(211)
plot(t,yk_D(:,1),'k'), axis tight
xlabel('t (s)')
ylabel('y_1[t] (m)')
subplot(212)
plot(t,yk_D(:,2),'k'), axis tight
xlabel('t (s)')
ylabel('y_2[t] (m)')

% simulate: acceleration
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% Noise corrupt the output data
nsRatio = 0.05;
nk_D = repmat(nsRatio*std(yk_D),N,1).*randn(N,n);
yk_D_n = yk_D + nk_D;
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% Store input-output data for further processing
save displacementData sys_D_ss_c sys_D_tf_c sys_D_ss_d t uk yk_D nk_D yk_D_n Fs N
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------


%% Non–parametric Time–Series Analysis
%
% Tasks:
% Mean value removal
% PDF estimation
% Correlation analysis
% Spectral estimation
%

clear
close all
clc

% load data
load('accelerationData.mat','yk_A','uk','Fs','N')

% mean value removal
inp = uk - mean(uk);
out = yk_A - repmat(mean(yk_A),N,1);

% pdf estimation
figure(1)
subplot(311)
spdf(inp);
subplot(312)
spdf(out(:,1));
subplot(313)
spdf(out(:,2));

% correlation analysis
figure(2)
moments([inp out],300);

% spectral analysis: amplitude spectrum
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% spectral analysis: power spectrum
figure(4)
subplot(311)
pwelch(inp,2048,1024,2048,Fs);
subplot(312)
pwelch(out(:,1),2048,1024,2048,Fs);
subplot(313)
pwelch(out(:,2),2048,1024,2048,Fs);

% spectral analysis: frequency response functions
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

%% Output–only Identification
%
% Tasks:
% AR(na) estimation
% ARMA(na,nc) estimation
%

clear
close all
clc

% load data
load('accelerationData.mat','yk_A','Fs','N')

% mean value removal
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% create estimation and validation sets
outE = out(1:floor(0.8*N),:); Ne = length(outE);
outV = out(Ne+1:end,:);       

% AR(n) estimation
arModel = getAR(outE(:,1),Fs,4:20);
figure
compare(outV(:,1),arModel,1);

% ARMA(n,n) estimation
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

%% Input–output Identification
%
% Tasks:
% ARX(na,nb,nk)
% ARMAX(na,nb,nc,nk)
%

clear
close all
clc

% load data
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% mean value removal
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% create estimation and validation sets
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% ARX(n,n,0) estimation
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% ARMAX(n,n,n,0) estimation
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

%% Vector Time–Series Analysis
%
% Tasks:
% Covariance matrix estimation
% VAR(na) estimation
% VARX(na,nb,nk) estimation
%

clear
close all
clc

% load data
load('accelerationData.mat','yk_A','uk','Fs','N')

% mean value removal
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% create estimation and validation sets
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% covariance matrix estimation
figure(1)
vscf(out,500);

% VAR(n) estimation
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% VARX(n,n,0) estimation
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

%% Subspace Identification
%
% Tasks:
% MOESP estimation
%

clear
close all
clc

% load data
load('accelerationData.mat','yk_A','uk','Fs','N')

% mean value removal
%--------------------------------------------------------
% MISSING CODE BLOCK
%--------------------------------------------------------

% MOESP estimation
ssModel = getSS(out,inp,Fs,2:10);
