import FFT.jang_fft as fftlib

timestamps, waveform = fftlib.readWaveformCSV(r"9hz.csv")
fs, Ydb, SNDR, Enob, SNR, Enob_noise_only, THD, n = fftlib.convertWaveformToPSD(timestamps, waveform, 9.963989257812500)
fftlib.plotPSD(fs, Ydb, n, SNDR, SNR, Enob, THD)
fftlib.savePSD(fs, Ydb, n, SNDR, SNR, Enob, THD, "newtest.png")