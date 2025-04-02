function M = getARMAX(Y,U,Fs,orderRange)

% create iddata object
z = iddata(Y,U,1/Fs);
N = length(z.OutputData);

% estimate models from minOrder to maxOrder
BIC = zeros(1,length(orderRange));
RSS = BIC;
for n = 1:length(orderRange)
    M = armax(z,[orderRange(n) orderRange(n)+1 orderRange(n) 0]);
    e = pe(M,z);
    BIC(n) = log(var(e.OutputData))+(length(M.ParameterVector)*(log(N)/N));
    RSS(n) = sum(e.OutputData.^2);    
end

% plot criteria and select order
figure
subplot(211)
plot(orderRange,RSS,'-o')
title('RSS of ARMAX(n,n,0)')
subplot(212)
plot(orderRange,BIC,'-o')
title('BIC of ARMAX(n,n,0)')
ni = input('Select AR/X/MA order: ');

% store and validate selected model
M = armax(z,[ni ni+1 ni 0],'Ts',1/Fs);
e = pe(M,z);
figure
subplot(3,2,1)
plot(e.OutputData), axis tight
title('residual time-series')
subplot(3,2,2)
moments(e.OutputData,floor(N/4));
subplot(3,2,3)
histfit(e.OutputData,45)
title('histogram')
subplot(3,2,4)
normplot(e.OutputData)
subplot(3,2,5:6)
crosscor(U,e.OutputData,floor(N/4));
