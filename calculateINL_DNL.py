import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np
import os
import Saleae.saleae_utils as saleae_utils
import csv

def sin_pdf(bits, amp, shift):
	vfs = 1
	code_max = (np.floor(2**bits).astype(int))
	#print(code_max)
	shift = np.ceil(shift)
	pdf = list()
	for n in range(code_max):
		n += shift
		res = (1/np.pi)*(np.arcsin((vfs*(n-code_max/2))/(amp*code_max))-np.arcsin((vfs*(n-1-code_max/2))/(amp*code_max)))
		#print(res)
		pdf.append(res)
	#fig, ax = plt.subplots()
	#ax.plot(range(code_max),pdf)
	#plt.show()
	#input()
	return pdf

def getSine():
	resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","singleSNDR_new")
	file1 = "Input_v0.12Sub_v0.04333333333333333_f9.9639892578125"
	new_data_file = os.path.join(resultsfolderpath, "new3FF_FT_10HZ_VEXVC_hiz_AD2_0VCM2024-11-05_17-34-10", file1, file1)
	DATA = saleae_utils.SaleaeData(new_data_file+".csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], 11)
	DATA.loadData()
	DATA.convertDataToHex()
	DATA.readHexAtTriggerEdges()
	DATA.convertSynchHexdataToInt()
	#print(max(DATA.synchronousDataInt)-min(DATA.synchronousDataInt))
	with open("forINLDNL.csv", 'w', newline='') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		wr.writerow(DATA.synchronousDataInt)
	return DATA.synchronousDataInt

if __name__ == "__main__":
	dat = getSine()
	nbit = 10
	hist, bin_edges = np.histogram(dat, bins = list(range(2**nbit+1)), density=True)
	bin_edges = bin_edges[:-1]
	print(2**nbit)
	a = np.asarray(hist)
	b = sin_pdf(nbit, 0.088, 358)
	minf = lambda inp: np.sum(np.abs(np.nan_to_num((np.asarray(hist) - np.nan_to_num(sin_pdf(nbit, inp[0], inp[1]))))))
	min_val_res = np.inf
	saved_ic = None
	code_max = (np.floor(2**nbit).astype(int))
	pdf = []
	for n in range(code_max):
		n += 0
		res = (1/np.pi)*(np.arcsin((1*(n-code_max/2))/(0.088*code_max))-np.arcsin((1*(n-1-code_max/2))/(0.088*code_max)))
		#print(res)
		pdf.append(res)
	fig, ax = plt.subplots()
	ax.plot(pdf)
	plt.show()
	input()

	for guess_n in [1]:
		for guess_a in [1]:
			bnds = ((0.01, 0.2), (-900, 900))
			guess = (0.2, 200)
			res = minimize(minf, guess,method="Powell",bounds=bnds,options={'disp': True, 'ftol':1e-12, 'maxiter':100000})
			print(res.x)
			val_res = np.sum(np.abs(np.nan_to_num((np.asarray(hist) - np.nan_to_num(sin_pdf(nbit, res.x[0], res.x[1])))**2)))
			if val_res < min_val_res:
				min_val_res = val_res
				saved_ic = res.x



	#res.x = [0.08, 350]
	# Plot Histogram
	res.x = [1.6664624e-01, 2.74693621e+02]
	fig = plt.figure()
	bars = plt.bar(bin_edges, hist/np.sum(hist), width=1, linewidth=1, color='blue', alpha=0.5, label="ADC Data")
	plt.bar(bin_edges, np.abs(np.asarray(hist) - np.nan_to_num(sin_pdf(nbit, saved_ic[0], saved_ic[1]))), width=1, linewidth=1, color='green', alpha=0.5)
	plt.title("Sine Histogram Actual vs. Fitted")
	plt.xlabel("ADC code")
	plt.ylabel("Code probability")
	for bar in bars:
		bar.set_edgecolor("blue")
		bar.set_linewidth(1)
	bars = plt.bar(range((np.floor(2**nbit).astype(int))), sin_pdf(nbit, res.x[0], res.x[1]), width=1, color='red', alpha=0.5, label="Fitted Data")
	print(range((np.floor(2**nbit).astype(int))-1))
	print(sin_pdf(nbit, res.x[0], res.x[1]))
	for bar in bars:
		bar.set_edgecolor("red")
		bar.set_linewidth(1)
	plt.tight_layout()
	plt.show()
	
	fig = plt.figure()
	plt.plot(range((np.floor(2**nbit).astype(int))), (np.asarray(hist) / sin_pdf(nbit, res.x[0], res.x[1]))-1, color='red')
	plt.title("ADC DNL")
	plt.ylabel("DNL (LSBs)")
	plt.xlabel("ADC code")
	
	plt.show()
	fig = plt.figure()
	plt.plot(range((np.floor(2**nbit).astype(int))), np.cumsum(np.nan_to_num((np.asarray(hist) / sin_pdf(nbit, res.x[0], res.x[1]))-1, nan=0.0, posinf=0.0, neginf=0.0)), color='red')
	plt.title("ADC INL")
	plt.ylabel("INL (LSBs)")
	plt.xlabel("ADC code")
	plt.show()