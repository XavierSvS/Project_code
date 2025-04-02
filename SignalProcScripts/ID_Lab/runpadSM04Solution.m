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
Cc = [-M\K -M\C];
Dc = M\P;
sys_A_ss_c = ss(Ac,Bc,Cc,Dc); % state-space
sys_A_tf_c = tf(sys_A_ss_c);  % transfer function
figure(2)
sys_A_frf_c = bodeplot(sys_A_tf_c(1,1),'k',sys_A_tf_c(2,1),'r'); grid on
setoptions(sys_A_frf_c,'FreqUnits','Hz','Xlim',[.1 25]);

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
sys_A_ss_d = c2d(sys_A_ss_c,Ts);    % discrete-time state-space
yk_A = lsim(sys_A_ss_d,uk,t);       % response
figure(4)
subplot(211)
plot(t,yk_A(:,1),'k'), axis tight
xlabel('t (s)')
ylabel('y_1[t] (m/s^2)')
subplot(212)
plot(t,yk_A(:,2),'k'), axis tight
xlabel('t (s)')
ylabel('y_2[t] (m/s^2)')

% Noise corrupt the output data
nsRatio = 0.05;
nk_D = repmat(nsRatio*std(yk_D),N,1).*randn(N,n);
yk_D_n = yk_D + nk_D;
nk_A = repmat(nsRatio*std(yk_A),N,1).*randn(N,n);
yk_A_n = yk_A + nk_A;

% Store input-output data for further processing
save displacementData sys_D_ss_c sys_D_tf_c sys_D_ss_d t uk yk_D nk_D yk_D_n Fs N
save accelerationData sys_A_ss_c sys_A_tf_c sys_A_ss_d t uk yk_A nk_A yk_A_n Fs N


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
DFT = fft([inp out]);
f = linspace(0,Fs/2,N/2+1);
Sxx = abs(DFT(1:N/2+1,1))/N; Sxx(2:end-1) = 2*Sxx(2:end-1);
Syy1 = abs(DFT(1:N/2+1,2))/N; Syy1(2:end-1) = 2*Syy1(2:end-1);
Syy2 = abs(DFT(1:N/2+1,3))/N; Syy2(2:end-1) = 2*Syy2(2:end-1);
figure(3)
subplot(311)
plot(f,Sxx)
title('Amplitude Spectrum')
xlabel('f (Hz)')
ylabel('u[t]')
subplot(312)
plot(f,Syy1)
title('Amplitude Spectrum')
xlabel('f (Hz)')
ylabel('y_1[t]')
subplot(313)
plot(f,Syy2)
title('Amplitude Spectrum')
xlabel('f (Hz)')
ylabel('y_2[t]')

% spectral analysis: power spectrum
figure(4)
subplot(311)
pwelch(inp,2048,1024,2048,Fs);
subplot(312)
pwelch(out(:,1),2048,1024,2048,Fs);
subplot(313)
pwelch(out(:,2),2048,1024,2048,Fs);

% spectral analysis: frequency response functions
[Txy1,~] = tfestimate(inp,out(:,1),2048,1024,2048,Fs);
magdB1 = 20*log10(abs(Txy1));
phasi1 = (180/pi)*phase(Txy1);
[Txy2,F] = tfestimate(inp,out(:,2),2048,1024,2048,Fs);
magdB2 = 20*log10(abs(Txy2));
phasi2 = (180/pi)*phase(Txy2);
figure(5)
subplot(211)
plot(F,magdB1,'k',F,magdB2,'r')
axis tight
grid on
subplot(212)
plot(F,phasi1,'k',F,phasi2,'r')
axis tight
grid on

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
out = yk_A - repmat(mean(yk_A),N,1);

% create estimation and validation sets
outE = out(1:floor(0.8*N),:); Ne = length(outE);
outV = out(Ne+1:end,:);       

% AR(n) estimation
arModel = getAR(outE(:,1),Fs,4:20);
figure
compare(outV(:,1),arModel,1);

% ARMA(n,n) estimation
armaModel = getARMA(outE(:,1),Fs,4:20);
figure
compare(outV(:,1),armaModel,1);

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
load('accelerationData.mat','yk_A','uk','Fs','N')

% mean value removal
inp = uk - mean(uk);
out = yk_A - repmat(mean(yk_A),N,1);

% create estimation and validation sets
outE = out(1:floor(0.8*N),:);    Ne = length(outE);
outV = out(Ne+1:end,:);      
inpE = inp(1:floor(0.8*N),:);
inpV = inp(Ne+1:end,:);

% ARX(n,n,0) estimation
arxModel = getARX(outE(:,1),inpE,Fs,2:10);
figure
compare([outV(:,1) inpV],arxModel,1);

% ARMAX(n,n,n,0) estimation
armaxModel = getARMAX(outE(:,1),inpE,Fs,2:10);
figure
compare([outV(:,1) inpV],armaxModel,1);

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
inp = uk - mean(uk);
out = yk_A - repmat(mean(yk_A),N,1);

% create estimation and validation sets
outE = out(1:floor(0.8*N),:);    Ne = length(outE);
outV = out(Ne+1:end,:);      
inpE = inp(1:floor(0.8*N),:);
inpV = inp(Ne+1:end,:);

% covariance matrix estimation
figure(1)
vscf(out,500);

% VAR(n) estimation
varModel = getVAR(outE,Fs,2:10);
figure
compare(outV,varModel,1);

% VARX(n,n,0) estimation
varxModel = getVARX(outE,inpE,Fs,2:10);
figure
compare([outV inpV],varxModel,1);

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
inp = uk - mean(uk);
out = yk_A - repmat(mean(yk_A),N,1);

% MOESP estimation
ssModel = getSS(out,inp,Fs,2:10);
