function [sysH,Gee] = stochasticRealizationV(dat,n,k,Ts)

%
% stochasticRealizationV
%
% balanced stochastic realization (least squares).
%
% [sysH,Gee] = stochasticRealizationV(dat,n,k,Ts)
%
% estimates a stochastic realization SYSH of order 
% n and sampling period Ts for an s - variate time 
% series DAT, of size [N x S]. K controls the size
% of the "past" and "future" data matrices.
%
% Gee is the estimated noise covariance matrix.
%
% See also STOCHASTICREALIZATIONIV.
%
% Reference page in Help browser:
% <a href="matlab: web([docroot '/toolbox/mdac/funref/stochasticRealizations.html'],'-helpbrowser')">doc stochasticRealizations</a>
%

%
% Author: V. Ntertimanis
% 1st Ed: 16-07-2011
% Last Update: 27-10-2014
% National Technical University of Athens
% School of Mechanical Engineering
% Department of Mechanical Design & Automatic Control
% Copyright 1995-2011 V.K. Ntertimanis
%

% NOTE: implements Algorithm B of Katayama, p. 228 - 229.

y = dat';
% 1. construct the past and future data matrices
[Yp,Yf,p,N] = pastFutureDataMatrix(y,k);
% 2. LQ factorization
H = [Yp;Yf]; 
[~,L] = qr(H',0); L = L'/sqrt(N);
L11 = L(1:k*p,1:k*p); 
L21 = L(k*p+1:2*k*p,1:k*p);
L22 = L(k*p+1:2*k*p,k*p+1:2*k*p);
% 3. covariance matrices
Rff = (L21*L21'+L22*L22');
Rfp = L21*L11'; Rpp = L11*L11';
% 4. SVD's
[Uf,Sf,Vf] = svd(Rff); 
[Up,Sp,Vp] = svd(Rpp);
Sf = sqrtm(Sf); 
Sp = sqrtm(Sp);
Linv = Vf*(Sf\Uf'); 
Minv = Vp*(Sp\Up');
OC = Linv*Rfp*Minv';
[~,SS,VV] = svd(OC); VV = VV';
Sn = SS(1:n,1:n);
Vn = VV(1:n,:);
% 4. compute the estimate of the state vector
Xk = sqrtm(Sn)*Vn*Minv*Yp;
Xk1 = Xk(:,2:N);hXk = Xk(:,1:N-1);Ykk = y(:,1:N-1);
% 5. estimate A and C
Als = hXk;Bls = [Xk1;Ykk];
AC = Als'\Bls'; AC = AC';
Ah = AC(1:n,:);
Ch = AC(n+1:end,:);
% 6. compute the sample covariance matrices of residuals
RhoWV = Bls - AC*Als;
Wls = RhoWV(1:n,:);Vls = RhoWV(n+1:end,:);
Wls = Wls'; Vls = Vls';
Gwv = (1/(N-1))*([Wls';Vls']*[Wls Vls]);
% 7. estimate Kalman gain
[Kh,Gee] = kalmanGain(Gwv,Ch,Ah,n);
if isempty(Kh) == 1
    sysH = ss;
else
    sysH = ss(Ah,Kh,Ch,eye(p),Ts);
    % add meta data to ss object
    sysH.UserData.pastDataMatrix = Yp;
    sysH.UserData.futureDataMatrix = Yf;
    sysH.UserData.pastFutureIndex = k;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%--------------------------------------------------------------------------------------------------------------------------------------
function [Yp,Yf,p,N] = pastFutureDataMatrix(y,k)

%
% refer to p.227 of Katayama
%

[p,Ndat] = size(y);                 % the matrix is already transposed
N = Ndat - 2*k;
if 2*p*k > N 
    error('mdac:stochasticRealizationIV','Data matrix has incompatible size. Reduce k, or increase data size.')
end
Yf = blockHankel(y',k+1,k,N);       % [kp x N]
Yp = zeros(size(Yf));               % [kp x N]
for m = 1:k
    Yp((m-1)*p+1:m*p,:) = y(:,k-m+1:(k-m)+N);
end
%--------------------------------------------------------------------------------------------------------------------------------------

%--------------------------------------------------------------------------------------------------------------------------------------
function [Kh,Gee] = kalmanGain(Gwv,Ch,Ah,n)

Q = Gwv(1:n,1:n);
S = Gwv(1:n,n+1:end);
R = Gwv(n+1:end,n+1:end);
[P,~,G,~] = dare(Ah',Ch',Q,R,S,eye(n));
Kh = G';
if isempty(Kh) == 1
    warning('mdac:stochasticRealizationV','No stabilizing solution for the ARE found.\n         No model returned.')
    Gee = [];
    return
end
Gee = Ch*P*Ch' + R;
%--------------------------------------------------------------------------------------------------------------------------------------



