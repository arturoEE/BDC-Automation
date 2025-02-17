import Keysight.awg as awg
import Keysight.smu as smu
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

class singleSNDR(dft.Test):
    samplerate = 1000
    FS_Set = 0.08
    input_freq = 9.963989257812500
    saleae_dev_port = 10430
    trigger_channel = 11
    Nsamples = 2**16
    inputRange = [0.07]
    resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results")
    #resultsfolderpath = "C:\\Users\\eecis\\Desktop\\Arturo_Sem_Project\\Automation_git\\Results"
    testname = "SingleSNDR"
    note = ""
    #temploggingfolder = r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\TEMPLOG" # TEMPLOG folder holds temp data?
    temploggingfolder = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","TEMPLOG")
    SNDR_Measurements = []
    ENOB_Measurements = []

    def __init__(self, freq, note, vcm):
        self.awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
        self.awg2 = awg.AWG("USB0::0x0957::0x5707::MY53801784::0::INSTR")
        self.smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
        self.smu2 = smu.SMU("USB0::0x2A8D::0x9501::MY61390603::0::INSTR")
        self.input_freq = fftlib.chooseFin(freq, 1000, 2**16)
        self.note = note
        self.VCM = vcm
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

        self.smu2.setMode(0,'VOLT')
        self.smu2.configureChannel(0,'VOLT',0.0,0.001)
        self.smu2.enableCH1()

        # Clock Waveform 250 Hz and Input VEXC Sinusoid at FS
        self.awg2.configureChannelALT(2, 'SIN', self.FS_Set, self.FS_Set/2+self.VCM, self.input_freq)
        #self.awg2.configureChannel(1,'SIN',0.0,self.FS_Set/2,self.input_freq)
        self.awg1.configureChannel(1,'SQU',0.0,0.4,self.samplerate)
        self.awg1.setPhase(1,30)
        self.awg1.configureChannel(2,'SQU',0.0,0.8,self.samplerate)
        self.awg1.setPhase(2,0)
        self.awg1.syncPhase(2)
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
            self.awg2.configureChannelALT(1, 'SIN', voltage, voltage/2+self.VCM, self.input_freq)
            CIC_Set = afs.autoFS(voltage, self.input_freq,single=True, negative=False)
            #CIC_Set = 0.7
            # Configure SMU CI-Cell Bias
            #CIC_Set = 0.7482421875
            self.smu1.configureChannel(1,'VOLT',CIC_Set,0.0001)
            self.awg1.enableALL()
            self.awg2.enableALL()
            self.smu1.enableALL()
            time.sleep(0.5) # Time to Settle
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
            fs, Ydb, SNDR, Enob, SNR, Enob_noise_only, THD, n = fftlib.convertWaveformToPSD(timestamps, waveform, self.input_freq)
            self.SNDR_Measurements.append(SNDR)
            self.ENOB_Measurements.append(Enob)
            # Save PSD Image Annotated with ENOB and SNDR
            fftlib.savePSD(fs, Ydb, n, SNDR, SNR, Enob, THD,new_data_file+"_SNDR_"+str(CIC_Set)+".png")
            #fftlib.plotPSD(f, PyydB, Nmax, binLow, binHigh)
            # Clean Up
        self.teardown() # Take Down Simulation Setup
    def teardown(self):
        self.LA.close()
        self.awg1.disableALL()
        self.smu1.disableALL()
        self.awg2.disableALL()