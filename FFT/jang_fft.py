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

def sinusx(sigin,f,n):
    sinx=np.sin(2*math.pi*f*np.linspace(1,n,n))
    cosx=np.cos(2*math.pi*f*np.linspace(1,n,n))
    inputarray2=sigin[0:n]
    a0 = np.sum(inputarray2)/n
    a1=2*sinx*inputarray2
    a=np.sum(a1)/n
    b1=2*cosx*inputarray2
    b=np.sum(b1)/n
    outx= a0+ np.add(a*sinx, b*cosx)
    return outx

def calcENOB(wavein, fin, fs, win='blackman'):
    nSample = len(wavein)
    if nSample%2 == 1:
        nSample = nSample -1

    y = wavein[0:nSample]
    y = np.array(y)
    y = y - np.mean(y)

    ywindow = np.blackman(nSample)

    thing = y*ywindow
    ysignal = nSample/np.sum(ywindow)*sinusx(thing,fin/fs,nSample)
    ysignal2 = nSample/np.sum(ywindow)*sinusx(thing,2*fin/fs,nSample)
    ysignal3 = nSample/np.sum(ywindow)*sinusx(thing,3*fin/fs,nSample)
    ysignal4 = nSample/np.sum(ywindow)*sinusx(thing,4*fin/fs,nSample)
    ysignal5 = nSample/np.sum(ywindow)*sinusx(thing,5*fin/fs,nSample)
    ysignal6 = nSample/np.sum(ywindow)*sinusx(thing,6*fin/fs,nSample)
    ysignal7 = nSample/np.sum(ywindow)*sinusx(thing,7*fin/fs,nSample)
    ysignal8 = nSample/np.sum(ywindow)*sinusx(thing,8*fin/fs,nSample)
    ysignal9 = nSample/np.sum(ywindow)*sinusx(thing,9*fin/fs,nSample)
    ysignal10 = nSample/np.sum(ywindow)*sinusx(thing,10*fin/fs,nSample)
    ysignal11 = nSample/np.sum(ywindow)*sinusx(thing,11*fin/fs,nSample)
    ysignal12 = nSample/np.sum(ywindow)*sinusx(thing,12*fin/fs,nSample)
    ysignal13 = nSample/np.sum(ywindow)*sinusx(thing,13*fin/fs,nSample)
    ysignal14 = nSample/np.sum(ywindow)*sinusx(thing,14*fin/fs,nSample)

    ynoise = y-ysignal
    ynoise_only = y-ysignal-ysignal2-ysignal3-ysignal4-ysignal5-ysignal6-ysignal7-ysignal8-ysignal9-ysignal10-ysignal11-ysignal12-ysignal13-ysignal14
    ywindow = np.array(ywindow)

    RMSsignal = np.linalg.norm(np.fft.fft(ysignal*ywindow),2)
    RMSsignal2 = np.linalg.norm(np.fft.fft(ysignal2*ywindow),2)
    RMSsignal3 = np.linalg.norm(np.fft.fft(ysignal3*ywindow),2)
    RMSsignal4 = np.linalg.norm(np.fft.fft(ysignal4*ywindow),2)
    RMSsignal5 = np.linalg.norm(np.fft.fft(ysignal5*ywindow),2)
    RMSsignal6 = np.linalg.norm(np.fft.fft(ysignal6*ywindow),2)
    RMSsignal7 = np.linalg.norm(np.fft.fft(ysignal7*ywindow),2)

    RMSnoise = np.linalg.norm(np.fft.fft(ynoise*ywindow))
    RMSnoise_only = np.linalg.norm(np.fft.fft(ynoise_only*ywindow))

    THD = np.sqrt(RMSsignal2**2+RMSsignal3**2+RMSsignal4**2+RMSsignal5**2+RMSsignal6**2+RMSsignal7**2)/(RMSsignal)
    SNDR = 20*math.log10(RMSsignal/RMSnoise)
    SNR = 20*math.log10(RMSsignal/RMSnoise_only)
    Enob = (SNDR - 1.76)/6.02
    Enob_noise_only = (SNR - 1.76)/6.02

    Ydb = 20*np.log10(np.absolute(np.fft.fft(y*ywindow)))
    return [Enob, Ydb, SNDR, Enob_noise_only, SNR, THD]

def convertWaveformToPSD(timestamp,waveform, fin):
    nSample = 2**16
    fs = round(1/(timestamp[1]-timestamp[0]))
    offset = 0
    dout = waveform[offset:nSample+offset]
    [Enob, Ydb, SNDR,Enob_noise_only,SNR, THD] = calcENOB(dout, fin, fs, 'blackman')
    Ydb = Ydb - max(Ydb)
    print("SNDR: "+str(SNDR)+" ENOB: "+ str(Enob) + " SNR: "+str(SNR))
    return [fs, Ydb, SNDR, Enob, SNR, Enob_noise_only, THD, nSample]

def plotPSD(fs, ydb, n, SNDR,SNR, ENOB, THD):
    plt.style.use('seaborn-v0_8-deep')
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0,int(fs/2),int(n/2)),ydb[0:int(n/2)])
    fig.suptitle("PSD for measurement")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSD")
    ax.annotate("SNDR="+str("{:.2f}".format(SNDR)), xy=(0.1, 0.8), xycoords="axes fraction")
    #ax.annotate("SNR="+str("{:.2f}".format(SNR)), xy=(0.1, 0.75), xycoords="axes fraction")
    ax.annotate("THD="+str("{:.2f}".format(THD*100))+"%", xy=(0.1, 0.7), xycoords="axes fraction")
    ax.annotate("ENOB="+str("{:.2f}".format(ENOB)), xy=(0.1, 0.65), xycoords="axes fraction")
    fig.dpi = 100
    plt.grid()
    fig.show()
def savePSD(fs, ydb, n, SNDR, SNR, ENOB, THD, savefile):
    plt.style.use('seaborn-v0_8-deep')
    fig, ax = plt.subplots()
    ax.plot(np.linspace(0,int(fs/2),int(n/2)),ydb[0:int(n/2)])
    fig.suptitle("PSD for measurement")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSD")
    ax.annotate("SNDR="+str("{:.2f}".format(SNDR)), xy=(0.1, 0.8), xycoords="axes fraction")
    #ax.annotate("SNR="+str("{:.2f}".format(SNR)), xy=(0.1, 0.75), xycoords="axes fraction")
    ax.annotate("THD="+str("{:.2f}".format(THD*100))+"%", xy=(0.1, 0.7), xycoords="axes fraction")
    ax.annotate("ENOB="+str("{:.2f}".format(ENOB)), xy=(0.1, 0.65), xycoords="axes fraction")
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
