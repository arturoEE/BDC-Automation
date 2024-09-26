function outx = sinusx(in,f,n)
%
% Extraction of a sinusoidal signal
% from fourier series
% in is the input sinusoidal waveform
% f is the actual frequency (Fin/Fs)
% n must be integer multiples of the period

sinx=sin(2*pi*f*[1:n]);
cosx=cos(2*pi*f*[1:n]);
in=in(1:n);
a0 = sum(in)/n;
a1=2*sinx.*in;
a=sum(a1)/n;
b1=2*cosx.*in;
b=sum(b1)/n;
outx= a0+a.*sinx + b.*cosx;

