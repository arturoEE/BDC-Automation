import FFT.sndr_fft as sndr

[timestamps, waveform] = sndr.readWaveformCSV(r"thing.csv")
f, Pyy, PyydB, Nmax = sndr.convertWaveformToPSD(timestamps, waveform)
binLow, binHigh = sndr.getSignalPowerBins(f, PyydB, 9.963989)
SNDR, ENOB = sndr.caculateSNDRFromPSD(Pyy, Nmax, binLow, binHigh)
print(str(binLow) + ", "+str(binHigh))
print("SNDR: "+ str(SNDR)+" ENOB"+str(ENOB))
sndr.savePSD(f, PyydB, Nmax, binLow, binHigh, "test.png",SNDR)
sndr.plotPSD(f, PyydB, Nmax, binLow, binHigh)