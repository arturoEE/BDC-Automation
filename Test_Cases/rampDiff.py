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
import FFT.noise_lib as noiselib
import csv
import Calibration.auto_full_scale_ramp as afs

class RAMPD(dft.Test):
    samplerate = 1000
    saleae_dev_port = 10430
    trigger_channel = 11
    Nsamples = 2**14
    #0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06,
    inputRange = [0.04, 0.07, 0.08, 0.1]
    resultsfolderpath = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results")
    testname = "RampDifferentialPrompt"
    note = ""
    temploggingfolder = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","TEMPLOG")

    def __init__(self, note,vcm):
        self.awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
        self.smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
        self.smu2 = smu.SMU("USB0::0x2A8D::0x9501::MY61390603::0::INSTR")
        self.note = note
        self.VCM = vcm
    def configureInstruments(self):
        self.awg1.disableALL()
        self.smu1.disableALL()
        #self.smu2.disableALL()

        # Monitoring Buffer 1uA Reference Current
        self.smu1.setMode(0,'CURR')
        self.smu1.configureChannel(0,'CURR', 0.000001, 0.9)

        self.smu2.setMode(0,'VOLT')
        self.smu2.configureChannel(0,'VOLT', self.VCM, 0.0001)
        self.smu2.setMode(1,'VOLT')
        self.smu2.configureChannel(1,'VOLT', self.VCM, 0.0001)

        # Configure CI-Cell Voltage
        self.smu1.setMode(1,'VOLT')
        self.smu1.configureChannel(1,'VOLT',0.4,0.001)
        #self.smu1.enableALL()
        # Clock
        self.awg1.configureChannel(1,'SQU',0.0,0.4,1000)
        self.awg1.setPhase(1,30)
        self.awg1.configureChannel(2,'SQU',0.0,0.8,1000)
        self.awg1.setPhase(2,0)
        self.awg1.syncPhase(2)
        #self.awg1.enableALL()

        # Until we have a way of controlling the scan-chain via python
        #input("Press Enter after configuring scan chain to continue...")

        self.LA = saleae_atd.Saleae(devicePort=self.saleae_dev_port)
        self.LA.open()

        self.LA.configureLogic()
        self.LA.setCaptureDuration(1/self.samplerate*self.Nsamples)
        self.LA.setupDigitalTriggerCaptureMode(channel=self.trigger_channel)
    def run(self):
        self.generateLoggingFolder()
        generalresultsdir = self.resultsdir
        for voltage in self.inputRange:
            os.makedirs(os.path.join(generalresultsdir,str(voltage)), exist_ok=True)
            self.resultsdir = os.path.join(generalresultsdir,str(voltage))
            # let's calculate a set of values to try
            subvoltages = np.linspace(-1.0*voltage, voltage, 10) ### We'll Need to Add the Negative Functionality at some point
            meanCodevalues = []
            sigma1values = []
            sigma2values = []
            sigma3values = []
            SNRvalues = []
            minMaxCodes = []

            self.smu2.configureChannel(1,'VOLT',self.VCM+voltage,0.001)
            self.smu2.configureChannel(0,'VOLT',self.VCM,0.001)
            self.smu2.enableALL()
            time.sleep(0.5)
            # First Auto Full Scale
            self.awg1.enableALL()
            CIC_Set = afs.autoFS()
            #CIC_Set = 0.8234374999999998
            if CIC_Set > 0.77:
                CIC_Set = 0.77
            # Configure SMU CI-Cell Bias
            self.smu1.configureChannel(1,'VOLT',CIC_Set,0.001)
            self.smu1.enableALL()
            time.sleep(0.5) # Time to Settle
            negative = True
            for subvoltage in subvoltages:
                if negative == True:
                    self.smu2.configureChannel(1,'VOLT',self.VCM,0.001)
                    if subvoltage >= 0:
                        negative = False
                        self.smu2.configureChannel(1,'VOLT',self.VCM+subvoltage,0.001)
                        self.smu2.configureChannel(0,'VOLT',self.VCM,0.001)
                    else:
                        subvoltage = subvoltage*-1.0
                        self.smu2.configureChannel(0,'VOLT',self.VCM+subvoltage,0.001)
                else:
                    self.smu2.configureChannel(1,'VOLT',self.VCM+subvoltage,0.001)
                    self.smu2.configureChannel(0,'VOLT',self.VCM,0.001)
                time.sleep(0.5)
                # Take Measurmement
                self.LA.capture()
                # Save Measurement
                if negative:
                    note = "Input_vn"+str(subvoltage)
                else:
                    note = "Input_v"+str(subvoltage)
                self.LA.exportData(self.temploggingfolder)
                new_data_file = self.saveData(self.temploggingfolder,note)
                # Post Process Measurement
                DATA = saleae_utils.SaleaeData(new_data_file+".csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], self.trigger_channel)
                DATA.loadData()
                DATA.convertDataToHex()
                DATA.readHexAtTriggerEdges()
                DATA.convertSynchHexdataToInt()
                if not negative:
                    DATA.synchronousDataInt = [0.96*x+72.46 for x in DATA.synchronousDataInt]
                waveform_to_save = [[float(item) for  item in DATA.synchronousDataTimeStamp], noiselib.convertCodeToVoltage(11,voltage*2, DATA.synchronousDataInt)]
                # Save Post Processed Data
                with open(new_data_file+"_post_processed.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(waveform_to_save)
                # Save Code Data:
                with open(new_data_file+"_post_processed_CODE.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows([[float(item) for  item in DATA.synchronousDataTimeStamp], DATA.synchronousDataInt])
                #Noise Calculation Time
                [timestamps, codes] = noiselib.readWaveformCSV(new_data_file+"_post_processed_CODE.csv")
                mean, s1,s2,s3 = noiselib.findNoiseValue(codes)
                meanCodevalues.append(mean)
                sigma1values.append(s1)
                sigma2values.append(s2)
                sigma3values.append(s3)
                minMaxCodes.append(noiselib.findMinMaxCode(codes))
                SNR = noiselib.calculateSNR(mean,s1)
                SNRvalues.append(SNR)
                print("-------------------------------------------------")
                print("Input Voltage: " + str(subvoltage))
                print("Mean (LSB): "+str(mean) + "1Sigma Noise (LSB): "+ str(s1)+" 3Sigma Noise: "+str(s3))
                print("SNR: " + str(SNR))
                print("-------------------------------------------------")
            #noiselib.plotRamp(subvoltages, meanCodevalues, minMaxCodes,sigma1values)
            noiselib.saveRamp(subvoltages, meanCodevalues, minMaxCodes,sigma1values,new_data_file+"_Ramp_"+str(voltage)+".png")
            with open(new_data_file+"_FinalResults.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows([subvoltages, meanCodevalues, minMaxCodes,sigma1values,SNRvalues])
            # Clean Up
        self.teardown() # Take Down Simulation Setup
    def teardown(self):
        self.LA.close()
        self.smu2.disableALL()
        self.awg1.disableALL()
        self.smu1.disableALL()