import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math
import csv

def readWaveformCSV(datafile):
    # Zip performs a transpose operation
    with open(datafile, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        rows = []
        for row in csvreader:
            rows.append([float(rowitem) for rowitem in row])
        #result = list(zip(*csvreader))
        #print(result[0:len(result)][0])
        return rows

def convertCodeToVoltage(nbit, inputfs, codes):
    lsb = inputfs/(2**nbit)
    return [code*lsb for code in codes]

def convertWaveformToPSD(timestamp,waveform):
    fsamp = 1/(timestamp[1]-timestamp[0])
    nx = len(waveform)
    na = 1
    W = signal.windows.blackmanharris(math.floor(nx/na))
    N = len(W)
    f, Pxx = signal.welch(waveform,window=W,noverlap=0,fs=fsamp, detrend=False)
    Nmax = math.ceil(math.floor(nx/na)/2)-1  # Minus 1 to adj from MATLAB？

    fbin = f[1]-f[0] # Frequency Bin Width
    CG = sum(W)/N; # Normalized Coherent Gain
    NG = sum([w**2 for w in W])/N # Normalized Noise Gain
    NF = fbin*NG/(CG**2)
    Pyy = [pxx*NF for pxx in Pxx]
    PyydB = [10*np.log10(pyy) for pyy in Pyy]
    return [f, Pyy, PyydB, Nmax]

def plotPSD(f, PyydB, Nmax):
    fig, ax = plt.subplots()
    ax.semilogx(f[0:Nmax], PyydB[0:Nmax])
    fig.suptitle("PSD for measurement")
    ax.set_xlabel("Log Frequency (Hz)")
    ax.set_ylabel("PSD (dB relative to 1VRMS)")
    fig.dpi = 100
    plt.grid()
    fig.show()
    input()

def caculateSNDRFromPSD(f, Pyy, Nmax):
    pass

## Goal: Automated PSD/SNDR
## Compare the two methods, pwelch, vs Tim's
## SNDR Sweep Test versus input.