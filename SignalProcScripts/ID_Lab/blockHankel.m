function H = blockHankel(dat,k,a,b)

%
% blockHankel
%
% creates Hankel or block Hankel matrices.
%
% H = blockHankel(X,k,a,b)
%
% Given a matrix X, the function returns a block Hankel
% matrix H which contains A block rows, B block columns
% and its first block entry equals to X(k,:)'.
%
% If X is three dimensional array the first block entry
% of H equals to X(:,:,k).
%
% If X is a vector, the function calls HANKEL instead.
%
% See also HANKEL.
%

%
% Author: V. Ntertimanis
% 1st Ed: 15-06-2011
% Last Update: 04-05-2020
% ETH Zurich
%

% checks
[N,s,q] = size(dat);
% construct matrix
if q == 1
%     if s == 1 || N == 1
%         % single time - series: Hankel matrix
%         h = hankel(dat(k:k+a+b-2));
%         H = h(1:a,1:b);
%     elseif s > 1
        % vector time - series: block Hankel matrix
        if k+a+b-2 > N
            error('mdac:blockHankel','Index outside data range. Check input arguments (a and/or b).')
        end
        Y = dat';
        H = zeros(a*s,b);
        for n = 1:a
            H((n-1)*s+1:n*s,1:b) = Y(:,k+n-1:k+n-1+b-1); % b block columns
        end
%     end    
elseif q > 1
    % "impulse response" data
    if k+a+b-2 > q
        error('mdac:blockHankel','The specified number of block rows/columns leads index outside the data range (at least the [end,end] point).')
    end
    % three dimensional array
    arr2Mat = array2mat('hor',dat(:,:,k:end));
    H = zeros(a*N,b*s);
    for n = 1:a
        H((n-1)*N+1:n*N,1:s*b) = arr2Mat(:,(n-1)*s+1:(n-1)*s+s*b); % b block columns
    end
end




    