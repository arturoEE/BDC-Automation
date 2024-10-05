import csv
import statistics
import math
import numpy as np
import matplotlib.pyplot as plt

def convertCodeToVoltage(nbit, inputfs, codes):
    lsb = inputfs/(2**nbit)
    return [code*lsb for code in codes]


def readWaveformCSV(datafile):
    with open(datafile, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        rows = []
        for row in csvreader:
            rows.append([float(rowitem) for rowitem in row])
        return rows

def findNoiseValue(codes):
    error = codes - np.mean(codes)
    sigma1 = (np.percentile(error, 50+34.1, axis=0)- np.percentile(error, 50-34.1, axis=0))/2.
    sigma2 = (np.percentile(error, 50+34.1+13.6, axis=0)- np.percentile(error, 50-34.1-13.6, axis=0))/2.
    sigma3 = (np.percentile(error, 50+34.1+13.6+2.1, axis=0)- np.percentile(error, 50-34.1-13.6-2.1, axis=0))/2.
    return [np.mean(codes), np.std(error), sigma2, sigma3]

def calculateSNR(mean, sigma1):
    print(mean)
    print(sigma1)
    SNR = 10*math.log10((1023/2/np.sqrt(2))**2/sigma1**2)
    return SNR

def findMinMaxCode(codes):
    return [np.mean(codes)-min(codes),max(codes)-np.mean(codes)]

def plotRamp(setofinputs, setofmeans,setofpeaks, setofsigma1):
    fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=False)
    # Plot 1 Ramp with Error Bars
    setofpeaks = np.array(setofpeaks).T
    ax0.errorbar(setofinputs, setofmeans, yerr=setofpeaks, fmt='-o')
    ax0.set_title('Output code versus Input')
    # Plot 2 1Sigma Noise vs Input?
    ax1.plot(setofinputs, setofsigma1)
    ax1.set_title('RMS Noise (Voltage) versus Input')
    plt.show()

def saveRamp(setofinputs, setofmeans,setofpeaks, setofsigma1,savefile):
    fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=False)
    # Plot 1 Ramp with Error Bars
    setofpeaks = np.array(setofpeaks).T
    ax0.errorbar(setofinputs, setofmeans, yerr=setofpeaks, fmt='-o')
    ax0.set_title('Output code versus Input')
    # Plot 2 1Sigma Noise vs Input?
    ax1.plot(setofinputs, setofsigma1)
    ax1.set_title('RMS Noise (Voltage) versus Input')
    plt.savefig(savefile)