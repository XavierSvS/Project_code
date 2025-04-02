function [newvec,a]=rm(vec)

%
% RM 
%
% removes the mean value from a vector.
%
% [newvec,a]=rm(vec);
%
% Output argument a is the new mean value.
%
% When argument vec is a matrix, RM removes
% the mean value out of each column of vec.
% Argument a is a row vector that contains
% the corresponding new mean values.
%
% See also MEAN.
%

%
% Author: V.K. Dertimanis
% 1st Ed: 26-07-2003
% Last Update: 14-03-2017
% ETH Zurich
% Institut fur Baustatik und Konstruktion
% Chair of Structural Mechanics
%

newvec=vec-transpose(mean(vec)'*ones(1,size(vec,1)));a=mean(newvec);
