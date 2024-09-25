import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math
import csv
import statistics

def returnPrime(maxVal):
    primeNumbers = [y for y in range(1,maxVal)]
    for k in [z for z in range(1,maxVal)]:
        for l in [w for w in range(2,math.floor(math.sqrt(k)))]:
            if(k%l == 0):
                primeNumbers[k-1] = 0
                break

    primeNumbers = [x for x in primeNumbers if x != 0]
    return primeNumbers

def chooseFin(ftarget, fs, nSample):
    primes = returnPrime(nSample)
    templist = [abs(x-(ftarget/fs*nSample)) for x in primes]
    pos = templist.index(min(templist))
    nWindow = primes[pos]

    return nWindow / nSample * fs

print(chooseFin(10,1000,2**16))