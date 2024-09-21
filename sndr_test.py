import FFT.sndr_fft as sndr

[timestamps, waveform] = sndr.readWaveformCSV("out_0v5.csv")
f, Pyy, PyydB, Nmax = sndr.convertWaveformToPSD(timestamps, waveform)
sndr.plotPSD(f, PyydB, Nmax)