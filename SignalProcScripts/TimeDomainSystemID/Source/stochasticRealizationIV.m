function [sysH,Gee] = stochasticRealizationIV(dat,n,k,Ts)

%
% stochasticRealizationIV
%
% balanced stochastic realization (covariance).
%
% [sysH,Gee] = stochasticRealizationIV(dat,n,k,Ts)
%
% estimates a stochastic realization SYSH of order 
% n and sampling period Ts for an s - variate time 
% series DAT, of size [N x S]. K controls the size
% of the "past" and "future" data matrices.
%
% Gee is the estimated noise covariance matrix.
%
% See also STOCHASTICREALIZATIONIII.
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

% NOTE: implements Algorithm A of Katayama, p. 227 - 228.

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
Rfp = L21*L11';
Rpp = L11*L11';
% 4. SVD's
[Uf,Sf,Vf] = svd(Rff); 
[Up,Sp,Vp] = svd(Rpp);
Sf = sqrtm(Sf); 
Sp = sqrtm(Sp);
L = Uf*Sf*Vf'; 
M = Up*Sp*Vp';
Linv = Vf*(Sf\Uf'); 
Minv = Vp*(Sp\Up');
OC = Linv*Rfp*Minv';
[UU,SS,VV] = svd(OC); VV = VV';
Un = UU(:,1:n);
Sn = SS(1:n,1:n);
Vn = VV(1:n,:);
% 4. observability and controlability matrices
Ok = L*Un*sqrtm(Sn);
Ck = sqrtm(Sn)*Vn*M';
% 5. estimate stochastic realization
Ah = Ok(1:k*p-p,:)\Ok(p+1:k*p,:);
Ch = Ok(1:p,:);
[Kh,Gee] = kalmanGain(Sn,Rpp,Ah,Ch,Ck,k,p);
sysH = ss(Ah,Kh,Ch,eye(p),Ts);
% add meta data to ss object
sysH.UserData.pastDataMatrix = Yp;
sysH.UserData.futureDataMatrix = Yf;
sysH.UserData.pastFutureIndex = k;

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
function [Kh,Gee] = kalmanGain(Sn,Rpp,Ah,Ch,Ck,k,p)

Lambda = Rpp(1:p,1:p); % Covariance matrix of output
Cb = Ck(:,(k-1)*p+1:k*p)';
Gee = Lambda-Ch*Sn*Ch'; Kh = (Cb'-Ah*Sn*Ch')/Gee;
%--------------------------------------------------------------------------------------------------------------------------------------



