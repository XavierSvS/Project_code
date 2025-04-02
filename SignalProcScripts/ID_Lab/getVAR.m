function M = getVAR(Y,Fs,orderRange)

% create iddata object
z = iddata(Y,[],1/Fs);
N = length(z.OutputData);

% estimate models from minOrder to maxOrder
BIC = zeros(1,length(orderRange));
RSS = BIC;
for n = 1:length(orderRange)
    M = arx(z,orderRange(n)*ones(size(Y,2)));
    e = pe(M,z);
    s = e.OutputData'*e.OutputData;
    BIC(n) = log(det(s))+length(M.ParameterVector)*(log(N)/N);
    RSS(n) = trace(s);    
end

% plot criteria and select order
figure
subplot(211)
plot(orderRange,RSS,'-o')
title('trace(\Sigma) of VAR(n)')
subplot(212)
plot(orderRange,BIC,'-o')
title('BIC of VAR(n)')
ni = input('Select VAR order: ');

% store and validate selected model
M = arx(z,ni*ones(size(Y,2)),'Ts',1/Fs);
e = pe(M,z);
figure
vscf(e.OutputData,floor(N/4));
