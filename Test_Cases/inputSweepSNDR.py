import Keysight.awg as awg
import Keysight.smu as smu
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import Test_Cases.defaultTest as dft
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import FFT.sndr_fft as fftlib
import csv
import Calibration.auto_full_scale_SAR as afs

class inputSweepSNDR(dft.Test):
    samplerate = 1000
    FS_Set = 0.08
    input_freq = 10
    saleae_dev_port = 10430
    trigger_channel = 11
    Nsamples = 2**16
    inputRange = [0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results")
    #resultsfolderpath = "C:\\Users\\eecis\\Desktop\\Arturo_Sem_Project\\Automation_git\\Results"
    testname = "InputSweepSNDR"
    note = ""
    #temploggingfolder = r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\TEMPLOG" # TEMPLOG folder holds temp data?
    temploggingfolder = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","TEMPLOG")
    SNDR_Measurements = []
    ENOB_Measurements = []

    def __init__(self, note):
        self.awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
        self.smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
        self.note = note
    def configureInstruments(self):
        self.awg1.disableALL()
        self.smu1.disableALL()
        # Monitoring Buffer 1uA Reference Current
        self.smu1.setMode(0,'CURR')
        self.smu1.configureChannel(0,'CURR', 0.000001, 0.9)

        # Configure CI-Cell Voltage
        self.smu1.setMode(1,'VOLT')
        self.smu1.configureChannel(1,'VOLT',0.4,0.0001)
        #self.smu1.enableALL()

        # Clock Waveform 250 Hz and Input VEXC Sinusoid at FS
        self.awg1.configureChannel(1,'SQU',0.0,0.4,self.samplerate)
        self.awg1.configureChannel(2,'SIN',0.0,self.FS_Set/2,self.input_freq)
        #self.awg1.enableALL()

        # Until we have a way of controlling the scan-chain via python
        input("Press Enter after configuring scan chain to continue...")

        self.LA = saleae_atd.Saleae(devicePort=self.saleae_dev_port)
        self.LA.open()

        self.LA.configureLogic()
        self.LA.setCaptureDuration(1/self.samplerate*self.Nsamples)
        self.LA.setupDigitalTriggerCaptureMode(channel=self.trigger_channel)
    def run(self):
        self.generateLoggingFolder()
        for voltage in self.inputRange:
            # First Auto Full Scale

            CIC_Set = afs.autoFSSAR(voltage)
            # Configure SMU CI-Cell Bias
            self.smu1.configureChannel(1,'VOLT',CIC_Set,0.0001)
            self.awg1.enableALL()
            self.smu1.enableALL()
            time.sleep(2) # Time to Settle
            # Take Measurmement
            self.LA.capture()
            # Save Measurement
            note = "Input_v"+str(voltage)+"_f"+str(self.input_freq)
            self.LA.exportData(self.temploggingfolder)
            new_data_file = self.saveData(self.temploggingfolder,note)
            # Post Process Measurement
            DATA = saleae_utils.SaleaeData(new_data_file+".csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], self.trigger_channel)
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
            f, Pyy, PyydB, Nmax = fftlib.convertWaveformToPSD(timestamps, waveform)
            binLow, binHigh = fftlib.getSignalPowerBins(f, PyydB, 10)
            SNDR, ENOB = fftlib.caculateSNDRFromPSD(Pyy, Nmax, binLow, binHigh)
            self.SNDR_Measurements.append(SNDR)
            self.ENOB_Measurements.append(ENOB)
            #print(str(binLow) + ", "+str(binHigh))
            print("SNDR: "+ str(SNDR)+" ENOB: "+str(ENOB))
            # Save PSD Image Annotated with ENOB and SNDR
            fftlib.savePSD(f, PyydB, Nmax, binLow, binHigh,new_data_file+"_SNDR.png",SNDR)
            # Clean Up
        self.teardown() # Take Down Simulation Setup
    def teardown(self):
        self.LA.close()
        self.awg1.disableALL()
        self.smu1.disableALL()