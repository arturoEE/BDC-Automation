function dout = adc(ain, nBit, range)

vmin = range(1);
vmax = range(2);
vRange = vmax - vmin;
nSample = length(ain);
ain = ain - vmin;
% ain = ain + random('uniform', 0, vRange/2^(nBit + 6), [1 nSample])-vmin;
% dout= floor(ain / vRange * 2^nBit);
% dout= round(ain / vRange * (2^nBit));
dout= round(ain / vRange * (2^nBit-1));
% dout = round(2^nBit * (ain - mod(ain, vRange / 2^nBit))/vRange);
% dout(logical(dout == 2^nBit)) = 2^nBkit - 1;