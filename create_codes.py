import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np
import os
import Saleae.saleae_utils as saleae_utils
import csv

def getSine(folder, voltage, subvoltage):
	resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","DifferentialSNDR_INLDNL")
	file1 = "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f10.001182556152344"
	new_data_file = os.path.join(resultsfolderpath, folder, file1, file1)
	DATA = saleae_utils.SaleaeData(new_data_file+".csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], 11)
	DATA.loadData()
	DATA.convertDataToHex()
	DATA.readHexAtTriggerEdges()
	DATA.convertSynchHexdataToInt()
	#print(max(DATA.synchronousDataInt)-min(DATA.synchronousDataInt))
	path_to_save = os.path.join(resultsfolderpath, folder, file1+"_Codes.csv")
	with open(path_to_save, 'w', newline='') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(DATA.synchronousDataInt)
	return DATA.synchronousDataInt

folder = "SNDR_3FF_FIA_100VCM2024-11-12_12-54-02"
resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","DifferentialSNDR_INLDNL")
#voltages = [0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
voltages = [0.105]
for voltage in voltages:
    #subvoltages = np.linspace(voltage*0.8, voltage, 10)
    #subvoltages = np.linspace(0, voltage, 5)
    subvoltages = np.linspace(0.005, voltage, 10)
    #subvoltages = [0.07]
    fixedsubvoltages = np.linspace(4*10**(-3), 4*10**(-2), 5)
    #subvoltages = [0.02]
    subvoltages = np.append(subvoltages,fixedsubvoltages)
    subvoltages = np.append(subvoltages,voltage*1.1)
    subvoltages = np.append(subvoltages,voltage*0.95)
    #subvoltages = [0.1]
    subvoltages = np.sort(subvoltages)
    subvoltages = [voltage]
    #subvoltages = np.append(subvoltages,[(voltage + 0.1*voltage)])
    for subvoltage in subvoltages:
        getSine(folder, voltage, subvoltage)