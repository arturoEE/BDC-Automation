import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import math
import csv
import statistics

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
    dc_term = statistics.mean(waveform)
    waveformAC = [sample-dc_term for sample in waveform]
    fsamp = 1/(timestamp[1]-timestamp[0])
    nx = len(waveformAC)
    na = 1
    W = signal.windows.blackmanharris(math.floor(nx/na))
    N = len(W)
    f, Pxx = signal.welch(waveformAC,window=W,noverlap=0,fs=fsamp, detrend=False)
    Nmax = math.ceil(math.floor(nx/na)/2)  # Minus 1 to adj from MATLAB？
    # 65500
    fbin = f[1]-f[0] # Frequency Bin Width
    CG = sum(W)/N; # Normalized Coherent Gain
    NG = sum([w**2 for w in W])/N # Normalized Noise Gain
    NF = fbin*NG/(CG**2)
    Pyy = [pxx*NF for pxx in Pxx]
    PyydB = [10*np.log10(pyy) for pyy in Pyy]
    return [f, Pyy, PyydB, Nmax]

def plotPSD(f, PyydB, Nmax, binLow, binHigh):
    #pdiff = pdiff = np.gradient(PyydB)
    fig, ax = plt.subplots()
    ax.semilogx(f[0:Nmax], PyydB[0:Nmax])
    ax.semilogx(f[binLow:binHigh], PyydB[binLow:binHigh], 'r--')
    #ax.semilogx(f[0:Nmax], pdiff[0:Nmax], 'g.-')
    fig.suptitle("PSD for measurement")
    ax.set_xlabel("Log Frequency (Hz)")
    ax.set_ylabel("PSD (dB relative to 1VRMS)")
    fig.dpi = 100
    plt.grid()
    fig.show()
    input()
def savePSD(f, PyydB, Nmax, binLow, binHigh,savefile,SNDR):
    #pdiff = pdiff = np.gradient(PyydB)
    fig, ax = plt.subplots()
    ax.semilogx(f[0:Nmax], PyydB[0:Nmax])
    ax.semilogx(f[binLow:binHigh], PyydB[binLow:binHigh], 'r--')
    #ax.semilogx(f[0:Nmax], pdiff[0:Nmax], 'g.-')
    fig.suptitle("PSD for measurement")
    ax.set_xlabel("Log Frequency (Hz)")
    ax.set_ylabel("PSD (dB relative to 1VRMS)")
    ax.annotate("SNDR="+str(SNDR), xy=(0.1, 0.8), xycoords="axes fraction")
    fig.dpi = 100
    plt.grid()
    plt.savefig(savefile)
def caculateSNDRFromPSD(Pyy, Nmax, binLow, binHigh):
    signal_power = sum(Pyy[binLow:binHigh])
    total_power = sum(Pyy[7:Nmax])
    noise_and_distortion_power = total_power-signal_power
    SNDR = signal_power/noise_and_distortion_power
    SNDR_dB =10*np.log10(SNDR)
    ENOB = (SNDR_dB-1.76)/6.02
    return [SNDR_dB, ENOB]

def getSignalPowerBins(f, PyydB, fin):
    pdiff = pdiff = np.gradient(PyydB)
    fbin = f[1]-f[0]
    index = math.ceil(fin/fbin)
    # Find forward Index:
    forward_offset = 1
    while(1):
        if (pdiff[index+forward_offset] < 0):
            forward_offset = forward_offset+1
        else:
            #forward_offset = forward_offset-1
            break
    forward_index = index+forward_offset 
    # Find reverse Index:
    reverse_offset = -1
    while(1):
        if (pdiff[index+reverse_offset] > 0):
            reverse_offset = reverse_offset-1
        else:
            reverse_offset = reverse_offset+1
            break
    reverse_index = index+reverse_offset 
    return [reverse_index, forward_index]

## Goal: Automated PSD/SNDR
## Compare the two methods, pwelch, vs Tim's
## SNDR Sweep Test versus input.
## Data Logging Setup