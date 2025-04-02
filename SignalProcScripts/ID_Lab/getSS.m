function M = getSS(Y,U,Fs,orderRange)

% create iddata object
z = iddata(Y,U,1/Fs);

% n4sid options
opt = n4sidOptions('N4Weight','MOESP');

M = n4sid(z,orderRange,'Ts',1/Fs,'Feedthrough','DisturbanceModel','none',true(1,1),opt);