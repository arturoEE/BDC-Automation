import FFT.jang_fft as fftlib
import os
import matplotlib.pyplot as plt
import numpy as np
import re

resultfolder = "new3FF_FIA_10HZ_1KLinearized_SR560_hiz_AD2_SINGLEENDED_0VCM2024-10-25_20-57-51"
freq = "9.9639892578125"
freqnum = 9.9639892578125
#freq = "10.001182556152344"
#freqnum = 10.001182556152344

results_name = "new3ff_FIA_for_pres.txt"

resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","DifferentialSNDR")

plt.style.use('seaborn-v0_8-deep')
fig, ax = plt.subplots()
#fig2, ax2 = plt.subplots()
plt.grid()
#fig2, ax2 = plt.subplots()
folder = os.path.join(resultsfolderpath, resultfolder)
#voltages = [0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
voltages = [0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
#voltages = [0.052,0.054,0.056,0.058, 0.06, 0.062,0.064, 0.066, 0.068, 0.07, 0.072, 0.074]
SNRs = []
SNDRs = []
f = open(results_name, "a")
f.write("FS, Input, SNDR, SFDR, SNR, CIC_Bias\n")
for voltage in voltages:
    subvoltages = np.linspace(0.005, voltage, 10)
    #subvoltages = [voltage]
    #subvoltages = [0.05, 0.025, 0.0125]
    fixedsubvoltages = np.linspace(4*10**(-3), 4*10**(-2), 5)
    #subvoltages = [0.02]
    subvoltages = np.append(subvoltages,fixedsubvoltages)
    subvoltages = np.append(subvoltages,voltage*1.1)
    #subvoltages = np.append(subvoltages,voltage*0.95)
    #subvoltages = [voltage]
    subvoltages = np.sort(subvoltages)
    #subvoltages = np.append(subvoltages,[(voltage + 0.1*voltage)])
    subSNDRs = []
    subSFDRs = []
    subSNRs = []
    SNDR_last = 0
    SFDR_last = 0
    SNR_last = 0
    subvoltage_last = 0
    flag = 0
    for subvoltage in subvoltages:
        if subvoltage < 0.002:
            index = np.argwhere(subvoltages==subvoltage)
            subvoltages = np.delete(subvoltages, index)
            continue
        folder2 = os.path.join(folder, "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f"+freq)
        files = [f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))]
        pngfiles = [x for x in files if "png" in x]
        for png in pngfiles:
            result = re.search(r"Input_v\d+.\d+Sub_v\d+.\d+_f\d+.\d+_SNDR_(\d.\d+)", png)
            cibias = result.group(1)
            #cibias = ""
            print(cibias)
        csvfile = os.path.join(folder, "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f"+freq, "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f"+freq+"_post_processed.csv")
        timestamps, waveform = fftlib.readWaveformCSV(csvfile)
        #ax2.plot(waveform)
        print("Max: " + str(max(waveform)))
        print("Min: " + str(min(waveform)))
        fs, Ydb, SNDR, Enob, SNR, Enob_noise_only, THD, n,SFDR = fftlib.convertWaveformToPSD(timestamps, waveform, freqnum)
        if SNDR < SNDR_last:
            flag = 1
        if SNDR > SNDR_last and flag == 1:
            index = np.argwhere(subvoltages==subvoltage_last)
            subvoltages = np.delete(subvoltages, index)
            subSNDRs = [i for i in subSNDRs if i != SNDR_last]
            subSFDRs = [i for i in subSFDRs if i != SFDR_last]
            subSNRs = [i for i in subSNRs if i != SNR_last]
            flag = 0
        subSFDRs.append(SFDR)
        subSNDRs.append(SNDR)
        subSNRs.append(SNR)
        SNDR_last = SNDR
        SFDR_last = SFDR
        SNR_last = SNR
        subvoltage_last = subvoltage
        f = open(results_name, "a")
        f.write(str(voltage)+","+str(subvoltage)+","+str(SNDR)+","+str(SFDR)+","+str(SNR)+","+cibias+"\n")
        f.close()
    SNDRs.append(subSNDRs)
    print(subSFDRs)
    print(subvoltages)
    #subvoltages[0] = 0.002
    ax.semilogx([x for x in subvoltages], subSNDRs)
#Input_v0.01Sub_v0.0_f9.9639892578125
plt.legend([x for x in voltages])
plt.ylabel("SFDR (dB)")
plt.xlabel("Input FS")
plt.title("SFDR vs Input FT 10G 0CM")
plt.show()