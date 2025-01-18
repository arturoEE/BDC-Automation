import FFT.jang_fft as fftlib
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import csv

def correctWaveform(waveform):
    idx = 0
    waveformcorrected = waveform
    for point in waveform:
        if point < 0:
            waveformcorrected[idx] = waveform[idx-1]+(waveform[idx+1]-waveform[idx-1])/2
        idx = idx +1
    return waveformcorrected

resultfolder = "AD4_INL"
freq = "10.001182556152344"
freqnum = 10.001182556152344

resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","singleSNDR_new")

folder = os.path.join(resultsfolderpath, resultfolder)
voltages = [0.1058]
for voltage in voltages:
    subvoltages = [voltage]
    for subvoltage in subvoltages:
        folder2 = os.path.join(folder, "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f"+freq)
        csvfile = os.path.join(folder, "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f"+freq, "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f"+freq+"_post_processed.csv")
        timestamps, waveform = fftlib.readWaveformCSV(csvfile)
        waveform = correctWaveform(waveform)
        path_to_save = os.path.join(resultsfolderpath, folder, "AD4_INLCodes.csv")
        with open(path_to_save, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(waveform)