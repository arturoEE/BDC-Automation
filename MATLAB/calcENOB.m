function [Enob, Ydb, Ydbn, SNDR,Enob_noise_only,SNR] = calcENOB(input,Fin,Fs, Win)


%% input should be single row %%
if (size(input,1)~=1)
    input = input';
end
nSample = length(input);

%% nSample should be even %%
if(mod(nSample, 2) == 1)
    nSample = nSample - 1;
end
    
y = input(1:nSample);
%% remove DC offset %%%
%% DC offset is not part of the signal nor the noise
y = y-mean(y);

if(nargin == 3)
    ywindow = boxcar(nSample)';
elseif(strcmp(Win, 'hanning'))
    ywindow = hanning(nSample)';
elseif(strcmp(Win, 'hamming'))
    ywindow = hamming(nSample)';
elseif(strcmp(Win, 'blackman'))
    ywindow = blackman(nSample)';
else
    ywindow = boxcar(nSample)';
end
ysignal = nSample/sum(ywindow)*sinusx(y.*ywindow,Fin/Fs,nSample);
ysignal2 = nSample/sum(ywindow)*sinusx(y.*ywindow,2*Fin/Fs,nSample);
ysignal3 = nSample/sum(ywindow)*sinusx(y.*ywindow,3*Fin/Fs,nSample);
ysignal4 = nSample/sum(ywindow)*sinusx(y.*ywindow,4*Fin/Fs,nSample);
ysignal5 = nSample/sum(ywindow)*sinusx(y.*ywindow,5*Fin/Fs,nSample);
ysignal6 = nSample/sum(ywindow)*sinusx(y.*ywindow,6*Fin/Fs,nSample);
ysignal7 = nSample/sum(ywindow)*sinusx(y.*ywindow,7*Fin/Fs,nSample);
ysignal8 = nSample/sum(ywindow)*sinusx(y.*ywindow,8*Fin/Fs,nSample);
ysignal9 = nSample/sum(ywindow)*sinusx(y.*ywindow,9*Fin/Fs,nSample);
ysignal10 = nSample/sum(ywindow)*sinusx(y.*ywindow,10*Fin/Fs,nSample);
ysignal11 = nSample/sum(ywindow)*sinusx(y.*ywindow,11*Fin/Fs,nSample);
ysignal12 = nSample/sum(ywindow)*sinusx(y.*ywindow,12*Fin/Fs,nSample);
ysignal13 = nSample/sum(ywindow)*sinusx(y.*ywindow,13*Fin/Fs,nSample);
ysignal14 = nSample/sum(ywindow)*sinusx(y.*ywindow,14*Fin/Fs,nSample);

ynoise = y-ysignal;
ynoise_only = y-ysignal-ysignal2-ysignal3-ysignal4-ysignal5-ysignal6-ysignal7-ysignal8-ysignal9-ysignal10-ysignal11-ysignal12-ysignal13-ysignal14;


RMSsignal = norm(fft(ysignal.*ywindow));
RMSsignal2 = norm(fft(ysignal2.*ywindow));
RMSsignal3 = norm(fft(ysignal3.*ywindow));
RMSsignal4 = norm(fft(ysignal4.*ywindow));
RMSsignal5 = norm(fft(ysignal5.*ywindow));
RMSsignal6 = norm(fft(ysignal6.*ywindow));
RMSsignal7 = norm(fft(ysignal7.*ywindow));

RMSnoise = norm(fft(ynoise.*ywindow));
RMSnoise_only = norm(fft(ynoise_only.*ywindow));

SNDR = 20*log10(RMSsignal/RMSnoise);
SNR = 20*log10(RMSsignal/RMSnoise_only);
Enob = (SNDR - 1.76)/6.02;
Enob_noise_only = (SNR - 1.76)/6.02;


Ydb = 20*log10(abs(fft(y.*ywindow)));
Ydbn = 20*log10(abs(fft(ynoise.*ywindow)));

%subplot(211);
%plot(ydB(1:floor(nSample/2)));
%subplot(212);
%plot(ysigdB(1:floor(nSample/2)));


