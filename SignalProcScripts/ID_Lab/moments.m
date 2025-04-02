function [sacorr,smean,svar] = moments(dat,k)

%
% MOMENTS
%
% computes the sample mean, sample variance and sample autocorrelation 
% function of time - series.
%
% [sacorr,smean,svar] = moments(dat,k)
%
% returns the unbiased mean value SMEAN, the sample variance SVAR and 
% the autocorrelation function SACORR, of the [N x 1] series DAT. The 
% latter is calculated up to K lags (zero lag included).
%
% The estimation is performed on the basis of the basic definitions of 
% the involved quantities. All estimators are unbiased.
%
% For the estimation of the sample autocorrelation function, the sample 
% mean is subtracted from the data.
%
% If DAT is a [N x p] matrix, MOMENTS performs at each column. In this
% case, SMEAN and SVAR are [1 x p] vectors and SACORR is a [k + 1 x p] 
% matrix.
%
% NOTE: the function does not estimate the sample covariance matrix.
%
% moments(dat,k)
%
% plots the sample autocorrelations of each time-series and prints the
% results.
%
% See also NSACF, CROSSCOR.
%

%
% Author: V.K. Dertimanis
% 1st Ed: 10-12-2004
% Last Update: 14-03-2017
% ETH Zurich
% Institut fur Baustatik und Konstruktion
% Chair of Structural Mechanics
%

[N,p] = size(dat);
if p > N
    warning('mdac:moments','Vector series appear to have more channels than data.')
end
maxlag = k;
% initialize estimates
smean = zeros(1,p);
svar = smean;
srms = smean;
COL = zeros(p,4);
sacorr = zeros(maxlag+1,p);
% perform estimation
for ind = 1:p
    
    % unbiased mean
    smean(1,ind) = sum(dat(1:N,ind))/N;
    % ubiased sample variance
    svar(1,ind) = (1/(N-1))*sum((dat(1:N,ind)-smean(1,ind)).^2);
    % sample rms
    srms(1,ind) = rms(dat(1:N,ind));
    % unbiased sample autocorrelation function
    TS = rm(dat(:,ind));
    for kk = 0:maxlag
        sacorr(kk+1,ind) = (1/(N-kk))*sum(TS(1:N-kk).*TS(kk+1:N));
    end
    
    if nargout==0
        COL(ind,1:4)=[ind smean(1,ind) svar(1,ind) srms(1,ind)];
    end
    
end

if nargout == 0
        
    % plot
    plag = (0:maxlag)';
    for k = 1:p
        if p > 1
            subplot(p,1,k)
        end
        if maxlag > 500
            bar(plag,sacorr(:,k)/sacorr(1,k),0.32,'r'),grid
        else
            bar(plag,sacorr(:,k)/sacorr(1,k),0.40,'r'),grid
        end
        line([0 maxlag],[1.96/sqrt(N) 1.96/sqrt(N)],'color','k')
        line([0 maxlag],[-1.96/sqrt(N) -1.96/sqrt(N)],'color','k')
        if k == 1
            title('Series sampled autocorrelation function')
        end
        if k == p
            xlabel('Lag {\tau}')
        end
        str = ['Series ',num2str(k)];
        ylabel(str)
        axis tight
    end
    
end




