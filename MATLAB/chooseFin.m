function fInReturn = chooseFin(fIn, fSample, nSample);

%nSample = 2^13;
%fIn = 25e6;
%fSample = 82e6;

primes = returnPrime(nSample);
[temp pos] = min(abs(primes - (fIn / fSample *nSample)));
nWindow = primes(pos);

fInReturn = nWindow / nSample * fSample;
%fprintf('fin is : %13.10f\n', fIn);