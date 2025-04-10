function X = gsample(gauss, N)

% gsample  Draw N samples from the Gaussian distribution (pdf) described by the
%             Gaussian data structure 'gauss'.
%=============================================================================================
S = chol(gauss.cov)';
X = S * randn(gauss.dim,N) + gauss.mu(:,ones(N,1));