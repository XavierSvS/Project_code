function G = vscf(dat,k)

%
% VSCF
%
% sample covariance function of multivariate processes.
%
% G = vscf(dat,k)
%
% returns an [p x p x (k+1)] array G, whose entries are 
% the estimated sample covariance matrices from 0 to k 
% lag, for the multivariate time-series DAT ([N x p]).
%
% Every column of DAT must represent a different series
% realization. 
%
% vscf(dat,k)
%
% without outputs plots the sample correlation estimates.
%
% See also MOMENTS, ACF, CROSSCOR.
%

%
% Author: V.K. Dertimanis
% 1st Ed: 04-01-2009
% Last Update: 14-03-2017
% ETH Zurich
% Institut fur Baustatik und Konstruktion
% Chair of Structural Mechanics
%


[N,p]=size(dat);
G=zeros(p,p,k+1);
dat=rm(dat);
for h=0:k
    G(1:p,1:p,h+1)=(1/N)*dat(h+1:end,:)'*dat(1:end-h,:);
end

if nargout==0    
    
    V=diag(diag(G(1:p,1:p,1)))^(-1/2);
    for h=1:k+1
        G(:,:,h)=V*G(:,:,h)*V;
    end
    
    % create a [p x p] figure
    counter=1;
    xdat=0:1:k;
    for ROWS=1:p        
        for COLUMNS=1:p
            subplot(p,p,counter)
            YDAT(1:k+1,1)=G(ROWS,COLUMNS,:);
            if k>500
                bar(xdat,YDAT,0.32)
            else
                bar(xdat,YDAT,0.40)
            end
            if ROWS==COLUMNS
                title(['TS ',int2str(ROWS)])
            else
                title(['TS ',int2str(ROWS),' x TS ',int2str(COLUMNS)])
            end
            xlabel('lag {\tau}')
            if ROWS==COLUMNS
                ylabel('ACF')
            else
                ylabel('CCF')
            end
            h1=line([-2 k+1],[1.96/sqrt(N) 1.96/sqrt(N)]);
            set(h1,'color','r')
            h2=line([-2 k+1],[-1.96/sqrt(N) -1.96/sqrt(N)]);
            set(h2,'color','r')
            axis([-2 k+1 -1 1])            
            counter=counter+1;
        end        
    end   
end





























    
