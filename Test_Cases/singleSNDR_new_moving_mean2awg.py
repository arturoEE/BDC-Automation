import Keysight.awg as awg
import Keysight.smu as smu
import Keysight.scope as scope
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import Test_Cases.defaultTest as dft
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import FFT.jang_fft as fftlib
import csv
import Calibration.auto_full_scale_improved as afs

##SMU1 P1: VCM
##SMU1 P2: CI-Cell
#Scope Wavegen: Clock
# AWG1: VP
# AWG2: Vn

class singleSNDR_mm(dft.Test):
    samplerate = 1000
    FS_Set = 0.08
    input_freq = 10
    saleae_dev_port = 10430
    trigger_channel = 11
    Nsamples = 2**20
    #[0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12]
    #inputRange = [0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]
    inputRange = [0.1058]

    #inputRange = [0.104]
    #inputRange = [0.08731]

    #inputRange = [1.0]
    subvoltage_record =[]
    #inputRange = [0.07]
    resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results")
    #resultsfolderpath = "C:\\Users\\eecis\\Desktop\\Arturo_Sem_Project\\Automation_git\\Results"
    testname = "singleSNDR_new"
    note = ""
    #temploggingfolder = r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\TEMPLOG" # TEMPLOG folder holds temp data?
    temploggingfolder = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","TEMPLOG")
    SNDR_Measurements = []
    ENOB_Measurements = []
    SNR_Measurements = []
    SFDR_Measurements = []
    Measurements = []

    def __init__(self, note,freq,vcm):
        self.awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
        self.smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
        self.awg2 = awg.AWG("USB0::0x0957::0x5707::MY53801784::0::INSTR")
        self.input_freq = fftlib.chooseFin(freq, self.samplerate, self.Nsamples)
        self.note = note
        self.VCM = vcm
    def configureInstruments(self):
        self.awg1.disableALL()
        self.smu1.disableALL()

        # Configure CI-Cell Voltage
        self.smu1.setMode(1,'VOLT')
        self.smu1.configureChannel(1,'VOLT',0.4,0.001)
        #self.smu1.enableALL()

        # Input Differential Sinusoid
        self.awg2.configureChannelALT(2, 'SIN', 0.02, 0.01+self.VCM, self.input_freq)
        # Clock
        self.awg1.configureChannel(1,'SQU',0.0,0.4,1000)
        self.awg1.setPhase(1,30)
        self.awg1.configureChannel(2,'SQU',0.0,0.8,1000)
        self.awg1.setPhase(2,0)
        self.awg1.syncPhase(2)
        self.awg1.enableALL()


        self.LA = saleae_atd.Saleae(devicePort=self.saleae_dev_port)
        self.LA.open()

        self.LA.configureLogic()
        self.LA.setCaptureDuration(1/self.samplerate*self.Nsamples)
        self.LA.setupDigitalTriggerCaptureMode(channel=self.trigger_channel)
    def run(self):
        self.input_freq = fftlib.chooseFin(self.input_freq, self.samplerate, self.Nsamples)
        self.generateLoggingFolder()
        for voltage in self.inputRange:
            subvoltages = np.linspace(0.005, voltage, 20)
            #subvoltages = [0.05, 0.025, 0.0125]
            fixedsubvoltages = np.linspace(4*10**(-3), 4*10**(-2), 5)
            #subvoltages = [0.02]
            subvoltages = np.append(subvoltages,fixedsubvoltages)
            subvoltages = np.append(subvoltages,voltage*1.1)
            subvoltages = np.append(subvoltages,voltage*0.95)
            #subvoltages = np.linspace(0.08, voltage, 10)
            #subvoltages = [0.09066666666666667]#
            #subvoltages = [0.08921052631578948]
            subvoltages = [voltage]
            self.awg2.configureChannelALT(2,'SIN',voltage*1.0, voltage/2+self.VCM, self.input_freq)
            self.awg2.setPhase(2,0)
            self.awg2.enableALL()
            CIC_Set = afs.autoFS(voltage, self.input_freq, single=False, negative=False)
            #CIC_Set = 0.6593749999999999
            CIC_Set = 0.645 # to match resistor measurement
            #CIC_Set = 0.47890625000000003
            # Configure SMU CI-Cell Bias
            self.smu1.configureChannel(1,'VOLT',CIC_Set,0.001)
            self.smu1.enableCH2()
            time.sleep(10) # Time to Settle
            subvoltage_list = []
            for subvoltage in subvoltages:
                self.awg2.configureChannelALT(2,'SIN',subvoltage*1.0, subvoltage/2+self.VCM+((voltage-subvoltage)/2), self.input_freq)
                self.awg2.setPhase(2,0)
                time.sleep(1)
                # Take Measurmement
                self.LA.capture()
                # Save Measurement
                note = "Input_v"+str(voltage)+"Sub_v"+str(subvoltage)+"_f"+str(self.input_freq)
                self.LA.exportData(self.temploggingfolder)
                new_data_file = self.saveData(self.temploggingfolder,note)
                # Post Process Measurement
                DATA = saleae_utils.SaleaeData(new_data_file+".csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], self.trigger_channel)
                DATA.loadData()
                DATA.convertDataToHex()
                DATA.readHexAtTriggerEdges()
                DATA.convertSynchHexdataToInt()
                fig, ax = plt.subplots()
                #for idx, val in enumerate(DATA.synchronousDataInt):
                #    if DATA.synchronousDataInt[idx] ==0:
                #        print(DATA.synchronousDataInt[idx])
                #        DATA.synchronousDataInt[idx] = DATA.synchronousDataInt[idx]+20
                ax.plot([float(item) for  item in DATA.synchronousDataTimeStamp], DATA.synchronousDataInt)
                #plt.show()
                #waveform_to_save = [[float(item) for  item in DATA.synchronousDataTimeStamp], fftlib.convertCodeToVoltage(10,self.FS_Set, DATA.synchronousDataInt)]
                waveform_to_save = [[float(item) for  item in DATA.synchronousDataTimeStamp], DATA.synchronousDataInt]
                # Save Post Processed Data
                with open(new_data_file+"_post_processed.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(waveform_to_save)
                #SNDR Time
                [timestamps, waveform] = fftlib.readWaveformCSV(new_data_file+"_post_processed.csv")
                fs, Ydb, SNDR, Enob, SNR, Enob_noise_only, THD, n, SFDR = fftlib.convertWaveformToPSD(timestamps, waveform, self.input_freq)
                self.subvoltage_record.append(subvoltage)
                self.SNDR_Measurements.append(SNDR)
                subvoltage_list.append(SNDR)
                self.ENOB_Measurements.append(Enob)
                self.SNR_Measurements.append(SNR)
                self.SFDR_Measurements.append(SFDR)
                #print(str(binLow) + ", "+str(binHigh))
                print("SNDR: "+ str(SNDR)+" ENOB: "+str(Enob))
                # Save PSD Image Annotated with ENOB and SNDR
                fftlib.savePSD(fs, Ydb, n, SNDR, SNR, Enob, THD,new_data_file+"_SNDR_"+str(CIC_Set)+".png")
                # Clean Up
                plt.close('all')
            self.Measurements.append(subvoltage_list)
        self.teardown() # Take Down Simulation Setup
    def teardown(self):
        self.LA.close()
        #self.awg2.disableALL()
        self.awg1.disableALL()
        self.awg2.disableALL()
        self.smu1.disableALL()
        print("SNDR")
        print(self.SNDR_Measurements)
        print("SNR")
        print(self.SNR_Measurements)
        print("SFDR")
        print(self.SFDR_Measurements)
        print(self.Measurements)