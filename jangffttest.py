import FFT.jang_fft as fftlib

timestamps, waveform = fftlib.readWaveformCSV(r"9hz.csv")
fftlib.convertWaveformToPSD(timestamps, waveform, 9.9639892578125)
