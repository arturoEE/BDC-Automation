import FFT.jang_fft as fftlib
import os
import matplotlib.pyplot as plt
import numpy as np
from Saleae import saleae_utils
import csv

resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","DifferentialSNDR")
plt.style.use('seaborn-v0_8-deep')
fig, ax = plt.subplots()
plt.grid()
fig2, ax2 = plt.subplots()
folder = os.path.join(resultsfolderpath, "3FF_FIA_5mvVCM_1KLinearized_SR560_hiz2024-10-09_17-02-31")
voltages = [0.08,0.07, 0.06, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02, 0.015, 0.01]
SNRs = []
SNDRs = []
for voltage in voltages:
    csvfile = os.path.join(folder, "Input_v"+str(voltage)+"_f9.9639892578125", "Input_v"+str(voltage)+"_f9.9639892578125.csv")
    new_data_file = os.path.join(folder, "Input_v"+str(voltage)+"_f9.9639892578125", "Input_v"+str(voltage))
    DATA = saleae_utils.SaleaeData(csvfile, ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], 11)
    DATA.loadData()
    DATA.convertDataToHex9b()
    DATA.readHexAtTriggerEdges()
    DATA.convertSynchHexdataToInt()
    fig, ax = plt.subplots()
    #for idx, val in enumerate(DATA.synchronousDataInt):
    #    if DATA.synchronousDataInt[idx] ==0:
    #        print(DATA.synchronousDataInt[idx])
    #        DATA.synchronousDataInt[idx] = DATA.synchronousDataInt[idx]+20
    ax.plot([float(item) for  item in DATA.synchronousDataTimeStamp], DATA.synchronousDataInt)
    plt.show()
    waveform_to_save = [[float(item) for  item in DATA.synchronousDataTimeStamp], fftlib.convertCodeToVoltage(10,voltage, DATA.synchronousDataInt)]
    with open(new_data_file+"_post_processed9b.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(waveform_to_save)
    timestamps, waveform = fftlib.readWaveformCSV(new_data_file+"_post_processed9b.csv")
    fs, Ydb, SNDR, Enob, SNR, Enob_noise_only, THD, n, a = fftlib.convertWaveformToPSD(timestamps, waveform, 9.963989257812500)
    SNRs.append(SNR)
    SNDRs.append(SNDR)
print(SNDRs)