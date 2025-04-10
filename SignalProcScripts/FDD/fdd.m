
function out = fdd(in)

% FDD
%   input arguments
%    in.x = accel;
%    in.DF = 3; %Hz. Frequency interval in which mean values is evaluated.
%    in.Nfft = 2048;
%    in.fs = fs;
%    in.fc = fc;
%    in.isShowingFigures = 1;
%    in.Npeaks = 5;
%    in.curv_cut = 0.3;
%    in.hw = 10; % half width of sdof


% Cross spectrum
Nacc = size(in.x,2);
Gyy = zeros(Nacc, Nacc, in.Nfft/2+1);

for i=1:Nacc % response
    for j=1:Nacc % reference
        Gyy(i,j,:) = cpsd(in.x(:,i), in.x(:,j), in.Nfft, in.Nfft/2, in.Nfft, in.fs);
    end
end

% SVD----------------------------------------------------------------------
sw = zeros(size(Gyy,3),1);
for i=1:size(Gyy,3)
    [ug, sg, vg] = svd(Gyy(:,:,i));
    sw(i) = sg(1);
end
    semilogy([1:length(sw)]/in.Nfft*in.fs,sw)

%     xlabel('index')
    xlabel('Frequency (Hz)')
    ylabel('Singular Values')

% Peak-picking-------------------------------------------------------------
df = in.fs/in.Nfft;

if strcmp(in.ppm, 'manual')
    nextPeak = 1;
    ithpeak = 1;
    ifn = zeros(in.Npeaks,1);
    figure(176)
    semilogy(sw)
%  semilogy([1:length(sw)]/in.Nfft*in.fs,sw)
%  xlim([0 1.2*in.fc])
%     semilogy([1:length(sw)]/1024*100,sw)

    xlabel('index')
%     xlabel('Frequency (Hz)')
    ylabel('Singular Values')
    title('select peak regions')
    
    while nextPeak
        rec = ginput(2);
        
        if rec(1,1) > rec(2,1)
            disp('peak picking complete.')
            break;
        end
        
        if ithpeak > in.Npeaks
            disp('max number of peaks reached')
            break;
        end
        
        idx_f1 = rec(1,1); idx_f1 = floor(idx_f1);
        idx_f2 = rec(2,1); idx_f2 = floor(idx_f2);
        
        if idx_f1 >= idx_f2 || idx_f1 < 1 || idx_f2 > length(sw)
            disp('wrong peak region. select new')
            continue;
            
        else
            [pv, ifn(ithpeak)] = max(sw(idx_f1:idx_f2));
            ifn(ithpeak) = ifn(ithpeak) + idx_f1 - 1;
            ithpeak = ithpeak + 1;
        end
    end
    
else
    
    % 1. smoothing
    Nf = floor(in.DF/df);
    
    % mean of each block
    mean_sw = zeros(floor(length(sw)/Nf)-1,1);
    for i=1:length(mean_sw)
        mean_sw(i) = mean(sw(i*Nf+1:i*Nf+Nf));
    end
    
    
    % 2. curvature of the mean
    curv_sw = zeros(length(mean_sw)-2,1);
    for i=1:length(curv_sw)
        curv_sw(i) = log10(mean_sw(i+2)) - 2*log10(mean_sw(i+1)) + log10(mean_sw(i));
    end
    curv_sw = nmlize(curv_sw(curv_sw>-1e10 & curv_sw<1e10),0);
    
    if in.isShowingFigures
        figure;
        subplot(211); semilogy(mean_sw,'o-')
        subplot(212); plot(curv_sw,'o-')
    end
    
    
    
    % select freq..
    idx_peak = find(abs(curv_sw)>in.curv_cut); % this is index in curvature
    idx_peak = idx_peak + 1; % This index is in mean of sv
    diff_idx = diff(idx_peak);
    idx_freq = zeros(in.Npeaks,2); % 2--> from and to
    npeak = 1;
    for i=1:length(diff_idx)
        if i==1
            idx_freq(npeak,1) = idx_peak(1);
        else
            idx_freq(npeak,2) = idx_peak(i);
            if diff_idx(i)<3 % 2 is allowed.
                
            else
                npeak = npeak + 1;
                idx_freq(npeak,1) = idx_peak(i+1);
            end
        end
    end
    
    % get natural frequencies and their indices
    ifn = zeros(in.Npeaks,1);
    for i=1:in.Npeaks
        if idx_freq(i,1) == 0
            break;
        else
            i_left = (idx_freq(i,1)-1)*Nf;
        end
        
        if idx_freq(i,2) == 0
            i_right = i_left + 3*Nf - 1;
        else
            i_right = (idx_freq(i,2)+1)*Nf;
        end
        
        [psd_w, idx_fn] = max(sw(i_left:i_right));
        ifn(i) = idx_fn + i_left - 1;
    end
end

ifn = ifn(ifn>0);
freq = 0:df:(in.Nfft/2+1-1)*df;
fd_fdd2 = freq(ifn);
[fd_fdd, z_fdd] = sdof(sw, ifn, in.fs,in.hw);

if in.isShowingFigures
    figure(176)
    semilogy(freq, sw(:)); hold on
    semilogy(freq(ifn), sw(ifn),'ro')
    xlabel('frequency')
    xlim([0 in.fc])
    ylabel('singular values of S_{yy}(j\omega)')
end

save sw sw

% get mode shape
phi = zeros(size(Gyy,1), length(ifn));
phi_pp = zeros(size(Gyy,1), length(ifn));
for i=1:length(ifn)
    ifn1 = floor(fd_fdd(i)/df) + 1;
    ifn2 = floor(fd_fdd(i)/df) + 2;
    [ug1, sg, vg] = svd(Gyy(:,:,ifn1));
    [ug2, sg, vg] = svd(Gyy(:,:,ifn2));
    p1 = ug1(:,1);
    p2 = ug2(:,1);
    phi(:,i) = (fd_fdd(i)-freq(ifn1))/(freq(ifn2)-freq(ifn1))*(p2-p1) + p1;
    
    [ug, sg, vg] = svd(Gyy(:,:,ifn(i)));
    phi_pp(:,i) = ug(:,1);
end

% select fn under fc
idx_fc = find(fd_fdd<in.fc);
fd_fdd = fd_fdd(idx_fc);
fd_fdd2 = fd_fdd2(idx_fc);
z_fdd = z_fdd(idx_fc);
phi = phi(:,idx_fc);


% save
out = struct();

out.phi = phi;
out.phi_pp = phi_pp;

out.fd = fd_fdd;
out.fd_pp = fd_fdd2';

out.z = z_fdd;


function [f,z] = sdof(p,i,fs,hw)

% hw = 10; % half width of sdof
nf = length(i); % number of f
f = zeros(nf,1);
z = zeros(nf,1);
df = fs/(length(p)-1)/2;

if size(p,1) < size(p,2)
    p = p'; % p should be a column vector
end

for j=1:nf
    pj = zeros(size(p));
    pj(i(j)-hw:i(j)+hw) = p(i(j)-hw:i(j)+hw);
    pj = [pj; flipud(pj(2:end-1))];
    x = ifft(pj);
    [f(j), z(j)] = fz(x(1:floor(end/3)),fs);
    fpp = df*(i(j)-1);
    if abs(fpp-f(j)) > df
        f(j) = fpp;
    end
end



function [f,z] = fz(x,fs)

thrshld = 0.1; % 10 percent
n = length(x);
time = 0:1/fs:(n-1)/fs;
nzc = 0; % # of zero crossing (up->down)
izc = zeros(n-1,1);
t0 = zeros(n-1,1);

for i=2:n
    if x(i-1)>0 && x(i)<0
        nzc = nzc + 1;
        izc(nzc) = i;
        xa = x(i-1);
        xb = -x(i);
        ta = time(i-1);
        tb = time(i);
        t0(nzc) = (xa*tb+xb*ta)/(xa+xb);
    end
    
    if nzc > 2
        max_0 = max(abs(x(izc(1):izc(2))));
        max_x = max(abs(x(izc(nzc-1):izc(nzc))));
        if max_x / max_0 < thrshld
            break;
        end
    end
end

if nzc > 1
    f = (nzc-1)/(t0(nzc)-t0(1));
    max_1 = - min(x(izc(1):izc(2)));
    max_2 = - min(x(izc(nzc-1):izc(nzc)));
    z = 1/(2*pi)*log(max_1/max_2)/(nzc-1);
    
else
    f = 0;
    z = 0;
end












