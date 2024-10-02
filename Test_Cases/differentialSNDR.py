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

class differentialSNDR(dft.Test):
    samplerate = 1000
    FS_Set = 0.08
    input_freq = 10
    saleae_dev_port = 10430
    trigger_channel = 11
    Nsamples = 2**16
    #[0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12]
    inputRange = [0.045, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12]
    resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results")
    #resultsfolderpath = "C:\\Users\\eecis\\Desktop\\Arturo_Sem_Project\\Automation_git\\Results"
    testname = "DifferentialSNDR"
    note = ""
    #temploggingfolder = r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\TEMPLOG" # TEMPLOG folder holds temp data?
    temploggingfolder = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","TEMPLOG")
    SNDR_Measurements = []
    ENOB_Measurements = []

    def __init__(self, note,freq,vcm):
        self.awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
        self.smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
        self.awg2 = awg.AWG("USB0::0x0957::0x5707::MY53801784::0::INSTR")
        self.input_freq = fftlib.chooseFin(freq, 1000, 2**16)
        #self.scope1 = scope.SCOPE("USB0::0x2A8D::0x1776::MY58032037::0::INSTR")
        self.note = note
        self.VCM = vcm
    def configureInstruments(self):
        self.awg1.disableALL()
        self.awg2.disableALL()
        self.smu1.disableALL()

        # Monitoring Buffer 1uA Reference Current
        self.smu1.setMode(0,'VOLT')
        self.smu1.configureChannel(0,'VOLT', self.VCM, 0.0001)

        # Configure CI-Cell Voltage
        self.smu1.setMode(1,'VOLT')
        self.smu1.configureChannel(1,'VOLT',0.4,0.0001)
        #self.smu1.enableALL()

        # Input Differential Sinusoid
        self.awg2.configureChannelALT(2, 'SIN', 0.12, 0.06+self.VCM, self.input_freq)
        self.awg2.setTracking(2, 'INV')
        #self.awg2.configureChannelALT(1,'SIN',0.12,0.06, self.input_freq)
        #self.awg2.setPhase(1,0)
        #self.awg2.configureChannelALT(2,'SIN',0.12,0.06, self.input_freq)
        #self.awg2.setPhase(2,180)
        #self.awg2.syncPhase(2)
        # Clock
        self.awg1.configureChannel(1,'SQU',0.0,0.4,1000)
        self.awg1.setPhase(1,30)
        self.awg1.configureChannel(2,'SQU',0.0,0.8,1000)
        self.awg1.setPhase(2,0)
        self.awg1.syncPhase(2)
        #self.awg1.enableALL()
        #self.scope1.enableWaveGenClock()

        # Until we have a way of controlling the scan-chain via python
        input("Press Enter after configuring scan chain to continue...")

        self.LA = saleae_atd.Saleae(devicePort=self.saleae_dev_port)
        self.LA.open()

        self.LA.configureLogic()
        self.LA.setCaptureDuration(1/self.samplerate*self.Nsamples)
        self.LA.setupDigitalTriggerCaptureMode(channel=self.trigger_channel)
    def run(self):
        self.input_freq = fftlib.chooseFin(self.input_freq, 1000, 2**16)
        self.generateLoggingFolder()
        for voltage in self.inputRange:
            # First Auto Full Scale
            self.awg2.configureChannelALT(2, 'SIN', voltage, voltage/2+self.VCM, self.input_freq)
            self.awg2.setTracking(2, 'INV')
            self.awg1.enableALL()
            self.awg2.enableALL()
            #self.awg2.setFrequency(2,self.input_freq)
            CIC_Set = afs.autoFS(voltage, self.input_freq, single=False, negative=False)
            #CIC_Set = 0.7
            # Configure SMU CI-Cell Bias
            self.smu1.configureChannel(1,'VOLT',CIC_Set,0.0001)
            self.smu1.enableALL()
            time.sleep(0.5) # Time to Settle
            # Take Measurmement
            self.LA.capture()
            # Save Measurement
            note = "Input_v"+str(voltage)+"_f"+str(self.input_freq)
            self.LA.exportData(self.temploggingfolder)
            new_data_file = self.saveData(self.temploggingfolder,note)
            # Post Process Measurement
            DATA = saleae_utils.SaleaeData(new_data_file+".csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], self.trigger_channel)
            DATA.loadData()
            DATA.convertDataToHex()
            DATA.readHexAtTriggerEdges()
            DATA.convertSynchHexdataToInt()
            waveform_to_save = [[float(item) for  item in DATA.synchronousDataTimeStamp], fftlib.convertCodeToVoltage(10,self.FS_Set, DATA.synchronousDataInt)]
            # Save Post Processed Data
            with open(new_data_file+"_post_processed.csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(waveform_to_save)
            #SNDR Time
            [timestamps, waveform] = fftlib.readWaveformCSV(new_data_file+"_post_processed.csv")
            fs, Ydb, SNDR, Enob, SNR, Enob_noise_only, THD, n = fftlib.convertWaveformToPSD(timestamps, waveform, self.input_freq)
            self.SNDR_Measurements.append(SNDR)
            self.ENOB_Measurements.append(Enob)
            #print(str(binLow) + ", "+str(binHigh))
            print("SNDR: "+ str(SNDR)+" ENOB: "+str(Enob))
            # Save PSD Image Annotated with ENOB and SNDR
            fftlib.savePSD(fs, Ydb, n, SNDR, SNR, Enob, THD,new_data_file+"_SNDR_"+str(CIC_Set)+".png")
            # Clean Up
        self.teardown() # Take Down Simulation Setup
    def teardown(self):
        self.LA.close()
        self.awg2.disableALL()
        self.awg1.disableALL()
        self.smu1.disableALL()
        print(self.SNDR_Measurements)