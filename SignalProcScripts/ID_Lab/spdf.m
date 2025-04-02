function [p,x] = spdf(dat,varargin)

%
% SPDF
%
% sample probability density data.
%
% [p,x] = spdf(dat)
%
% estimates the probability density function of the time-series 
% DAT. With this syntax estimation is based on the "frequency",
%
% p = Ni/(Nh)
%
% with Ni denoting the number of the data fall in the i interval,
%
% x(k)-0.5*h  x(k)+0.5*h
%
% h is the width of each interval centered at x(k) and N is the 
% length of DAT. By default, the probability density function is
% estimated in the range,
%
% [-4*std(DAT) 4*std(DAT)]
%
% divided to a number of 8*std(DAT)/h intervals. This range can
% be set to an arbitrary one, say [A  B], so that a number of,
%
% K = (B-A)/W
%
% intervals are generated.
%
% [p,x] = spdf(dat,'CalcType','kernel')
%
% shifts to the kernel density sample estimator which generally 
% provides more smooth estimates.
%
% [p,x] = spdf(dat,'Width',h,'Range',[a b])
%
% or,
%
% [p,x] = spdf(dat,'CalcType','kernel','Width',h,'Range',[a b])
%
% passes user defined range and width.
%
% spdf(dat...
%
% without output arguments, normalizes the data prior to the 
% estimation and plots in a log scale the sample probability
% density function together with the normal distribution.
%
% See also KSDENSITY, HISTC.
%

%
% Author: V.K. Dertimanis
% 1st Ed: 20-09-2008
% Last Update: 14-03-2017
% ETH Zurich
% Institut fur Baustatik und Konstruktion
% Chair of Structural Mechanics
%

N=length(dat);
% set default options
defaultopt=struct('CalcType','frequency','Width',0.2*std(dat),'Range',[-4*std(dat) 4*std(dat)]);
if nargin>1
    % check how many varargins are present
    nvarargin=nargin-1;
    if any(nvarargin==[2 4 6])==0
        error('mdac:spdf','Enter function control as a PROPERTY/VALUE pair.')
    end
    for i=1:2:nvarargin
        if ischar(varargin{i})==0
            error('mdac:spdf','Enter function control as a PROPERTY/VALUE pair.')
        end
        switch varargin{i}
            case 'CalcType'
                if (strcmp(varargin{i+1},'frequency')==0 && strcmp(varargin{i+1},'kernel')==0)
                    error('mdac:spdf','Wrong calculation type. Enter ''frequency'' or ''kernel''.')                
                end                       
                defaultopt.CalcType=varargin{i+1};
            case 'Width'             
                defaultopt.Width=varargin{i+1};     
            case 'Range'             
                defaultopt.Range=varargin{i+1};                
            otherwise
                error('mdac:spdf','Unknown PROPERTY/VALUE assignment.')                
        end
    end 
end
% normalize is nargout=0
if nargout==0
    % normalize
    dat=(dat - mean(dat))/std(dat);
    % reset width 
    if strcmp(defaultopt.CalcType,'frequency')==1
        defaultopt.Width=0.2;
    else
        defaultopt.Width=(4/(3*N))^(1/5);
    end
    % reset range
    defaultopt.Range=[-4 4];    
end
h=defaultopt.Width;
% build basis vector
x=defaultopt.Range(1):h:defaultopt.Range(2)+h;
p=zeros(length(x),1);
switch defaultopt.CalcType    
    case 'frequency'
        % number of class intervals
        Ni=histc(dat,x);
        p=Ni/(N*h);
    case 'kernel'
        for k=1:length(x)
            p(k)=(1/(N*h))*sum((1/(sqrt(2*pi)))*exp(-(x(k)*ones(size(dat))-dat).^2/(2*h^2)));
        end       
end
if nargout==0
    % calulate N(0,1) for x
    px=(1/sqrt(2*pi))*exp(-x.^2/2);
    semilogy(x,px,'g','LineWidth',2')
    axis('tight')
    hold on
    semilogy(x,p,'o','MarkerFaceColor','r')
    hold off
%     legend('Gaussian Reference','Sample pdf')
    grid
    xlabel('Standard deviation')
    ylabel('spdf')
    title('Sample probability density function for the normalized series x-\mu/\sigma')
    axis([-4 4 (1/sqrt(2*pi))*exp(-defaultopt.Range(2)^2/2) 1])
    set(gca,'XTick',[-4 -3 -2 -1 0 1 2 3 4])
end

