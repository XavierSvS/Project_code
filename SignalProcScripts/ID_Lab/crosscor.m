function [acf,up_bound,low_bound] = crosscor(first_series,second_series,lag)

%
% CROSSCOR
%
% estimates the normalized sample cross correlation function between 
% two time-series. 
%
% [ccf,up_bound,low_bound] = crosscor(first_series,second_series,lag)
%
% first_series : the [Nx1] first time-series
% second_series: the [Nx1] second time-series
% lag      : the maximum lag. Usually lower than N/4.
% ccf      : [(1+lag)x1] vector containing the estimate
% up_bound : [(1+lag)x1] upper bound of statistical significance 
% low_bound: [(1+lag)x1] lower bound of statistical significance
%
% The statistical significance is by default set at the a=0.05 level.
%
% If the function is executed without output arguments plots the cross
% correlation function for the specified lags.
%
% See also XCOV.
%

%
% Author: V.K. Dertimanis
% 1st Ed: 28-02-1998
% Last Update: 14-03-2017
% ETH Zurich
% Institut fur Baustatik und Konstruktion
% Chair of Structural Mechanics
%

if length(first_series)~=length(second_series)
    error('mdac:crosscor','The two time-series must have the same number of data.')
end
lim=max(size(first_series));
a=xcov(first_series,second_series,'coeff');
dummy=max(size(a));
acf=a(((dummy-1)/2)+2:((dummy-1)/2)+1+lag,1);
% Computation of the statistical significance bounds
up_bound=(1.96/sqrt(lim))*ones(lag,1);
low_bound=-up_bound;
if nargout==0
    % Make the plot excluding acf(0).
    x_axis=(1:1:lag)';
    % Bar-plot of the acf.
    bar(x_axis,acf,'k')
    hold on
    % After holding the acf, line-plot the statistical bounds.
    plot(x_axis,up_bound,'r--',x_axis,low_bound,'r--')
    % Recalibrate axis.
    axis([1 lag 4*low_bound(1) 4*up_bound(1)])
    hold off
    xlabel('lag')
    ylabel('CCF')
    title('Sample cross-correlation')
end