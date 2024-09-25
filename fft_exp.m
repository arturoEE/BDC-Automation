% FFT Basic
%
% Arturo di Girolamo, ETH Zürich

%% Evaluate Fourier Transform and plot
% Fs = 1000;
% [pxx,f] = pwelch(vout(:,2),[],[],[],Fs);
% 
% plot(f,pow2db(pxx))
% hold on

nx = max(size(vout));
na = 1;                 % Averaging factor
W = blackmanharris(floor(nx/na));
N = length(W);
[Pxx,f]=pwelch(vout(:,2),W,0,[],1/TSamp);
Nmax = ceil(floor(nx/na)/2);

fbin=f(2)-f(1);          % Frrequency bin width
CG=sum(W)/N;             % Normalised Coherent Gain of Window
NG=sum(W.^2)/N;          % Normalised Noise Gain of Window
NF=fbin*NG/CG^2;         % Factor to be used when plotting a PSD
                         % into a plot normalized to Vrms           
Pyy=Pxx*NF;
PyydB=10*log10(Pyy);

semilogx(f(1:Nmax),PyydB(1:Nmax))
title('Power spectral density of vout')
xlabel('frequency (Hz)')
ylabel('PSD (dB re 1 Vrms)')

a=axis(); axis([f(1) f(Nmax) a(3) a(4)]);

SINAD_Power = sum(Pyy(20:Nmax))-sum(Pyy(1234:1320));
fundemental_power = sum(Pyy(1234:1320));
SNDR = fundemental_power/SINAD_Power;
SNDR_db = 10*log10(SNDR);