function M = getAR(Y,Fs,orderRange)

% create iddata object
z = iddata(Y,[],1/Fs);
N = length(z.OutputData);

% estimate models from minOrder to maxOrder
BIC = zeros(1,length(orderRange));
RSS = BIC;
for n = 1:length(orderRange)
    M = ar(z,orderRange(n),'ls');
    e = pe(M,z);
    BIC(n) = log(var(e.OutputData))+(length(M.ParameterVector)*(log(N)/N));
    RSS(n) = sum(e.OutputData.^2);    
end

% plot criteria and select order
figure
subplot(211)
plot(orderRange,RSS,'-o')
title('RSS of AR(n)')
subplot(212)
plot(orderRange,BIC,'-o')
title('BIC of AR(n)')
ni = input('Select AR order: ');

% store and validate selected model
M = ar(z,ni,'ls','Ts',1/Fs);
e = pe(M,z);
figure
subplot(2,2,1)
plot(e.OutputData), axis tight
title('residual time-series')
subplot(2,2,2)
moments(e.OutputData,floor(N/4));
subplot(2,2,3)
histfit(e.OutputData,45)
title('histogram')
subplot(2,2,4)
normplot(e.OutputData)