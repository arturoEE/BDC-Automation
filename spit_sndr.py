import FFT.jang_fft as fftlib
import os
import matplotlib.pyplot as plt
import numpy as np

resultfolder = "1F_FIA_10HZ_1KLinearized_SR560_hiz_AD2_SINGLEENDED_0VCM2024-10-22_13-02-14"

resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","DifferentialSNDR")


plt.style.use('seaborn-v0_8-deep')
fig, ax = plt.subplots()
plt.grid()
#fig2, ax2 = plt.subplots()
folder = os.path.join(resultsfolderpath, resultfolder)
#voltages = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
voltages = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035,0.04, 0.045, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
#voltages = [0.052,0.054,0.056,0.058, 0.06, 0.062,0.064, 0.066, 0.068, 0.07, 0.072, 0.074]
#voltages =  [0.025, 0.027, 0.029, 0.03, 0.031, 0.032, 0.034, 0.036, 0.038, 0.06, 0.062, 0.064, 0.068, 0.07, 0.072, 0.074]
SNRs = []
SNDRs = []
f = open("results_AD7_10G.txt", "a")
f.write("FS, Input, SNDR\n")
ENOBs = []
ENOBs2 = [[],[],[],[],[]]
for voltage in voltages:
    subvoltages =np.linspace(4*10**(-3), 4*10**(-2), 5)
    subSNDRs = []
    subENOBs = []
    SNDR_last = 0
    subvoltage_last = 0
    flag = 0
    idx = 0
    for subvoltage in subvoltages:
        if subvoltage < 0.002:
            index = np.argwhere(subvoltages==subvoltage)
            subvoltages = np.delete(subvoltages, index)
            continue
        csvfile = os.path.join(folder, "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f9.9639892578125", "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f9.9639892578125_post_processed.csv")
        timestamps, waveform = fftlib.readWaveformCSV(csvfile)
        fs, Ydb, SNDR, Enob, SNR, Enob_noise_only, THD, n,a = fftlib.convertWaveformToPSD(timestamps, waveform, 9.963989257812500)
        if SNDR < SNDR_last:
            flag = 1
        if SNDR > SNDR_last and flag == 1:
            index = np.argwhere(subvoltages==subvoltage_last)
            subvoltages = np.delete(subvoltages, index)
            subSNDRs = [i for i in subSNDRs if i != SNDR_last]
            flag = 0
        subSNDRs.append(SNDR)
        ENOBs.append(Enob)
        SNDR_last = SNDR
        subvoltage_last = subvoltage
        f = open("results_AD2_10G.txt", "a")
        f.write(str(voltage)+","+str(subvoltage)+","+str(SNDR)+"\n")
        f.close()
        ENOBs2[idx].append(Enob)
        idx = idx+1
    SNDRs.append(str(subSNDRs))
    #ENOBs.append(subENOBs)
    #subvoltages[0] = 0.002
    #ax.semilogx([2*x for x in subvoltages], subSNDRs)
#Input_v0.01Sub_v0.0_f9.9639892578125
print(ENOBs)

idx = 0
for x in np.linspace(4*10**(-3), 4*10**(-2), 5):
    fs_nyq = 1000
    Pbridge = [2*(0.63*VFS/0.15)**2*40*10**(-12)*fs_nyq for VFS in voltages]
    Power = [0.07314*10**(-6)+p for p in Pbridge]
    FOM = []
    for j in range(len(voltages)):
        FOM.append(Power[j]/(fs_nyq*2**(ENOBs2[idx][j]))*10**(12))
    ax.plot(voltages, FOM)
    idx = idx+1

plt.legend(subvoltages)
plt.ylabel("FOM pJ/Step")
plt.xlabel("Input FS")
plt.title("S5G FOM")
plt.show()