import Keysight.awg as awg
import Keysight.smu as smu
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import statistics

def autoFS(FS_Set, single=True):
    frequency = 10
    # Configure Test Equipment:
    awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
    smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
    awg2 = awg.AWG("USB0::0x0957::0x5707::MY53801784::0::INSTR")

    awg1.disableALL()
    smu1.disableALL()
    # Monitoring Buffer 1uA Reference Current
    #smu1.setMode(0,'CURR')
    #smu1.configureChannel(0,'CURR', 0.000001, 0.9)

    # Configure CI-Cell Voltage
    smu1.setMode(1,'VOLT')
    smu1.configureChannel(1,'VOLT',0.65,0.0001)
    smu1.enableALL()

    # Clock Waveform 250 Hz and Input VEXC Sinusoid at FS
    awg2.configureChannelALT(1,'SIN',FS_Set/2,FS_Set/4, frequency)
    awg2.setPhase(1,0)
    awg2.configureChannelALT(2,'SIN',FS_Set/2,FS_Set/3.5, frequency)
    awg2.setPhase(2,180)
    awg2.syncPhase(2)
    awg1.configureChannel(1,'SQU',0.0,0.8,1000)
    awg1.setPhase(1,30)
    awg1.configureChannel(2,'SQU',0.0,0.8,1000)
    awg1.setPhase(2,0)
    awg1.syncPhase(2)
    awg1.enableALL()
    awg2.enableCH2()


    LA = saleae_atd.Saleae(devicePort=10430)
    LA.open()

    LA.configureLogic()
    LA.setCaptureDuration(5)
    LA.setupDigitalTriggerCaptureMode(channel=10)
    

    if single:
        MaxCode = 1022
        MaxSlope = 200
        MinCode = 1
    else:
        MaxCode = 1022
        MaxSlope = 1000
        MinCode = -1022
    V_CIC_max = 0.9
    V_CIC_min = 0.1

    if single:
        offset = FS_Set/4
        last = None
        shiftAmount = 0.00005
        while(1):
            smu1.configureChannel(1,'VOLT',0.7,0.0001)
            time.sleep(0.5)
            LA.capture()
            LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
            DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
            DATA.loadData() # Load the Data We Just Measured
            DATA.convertDataToHex() # Convert Data to HEX Format
            DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
            DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
            minCodes = min(DATA.synchronousDataInt)
            print("Adjusting Sine Minimum. Current Min Code: " + str(minCodes))
            if minCodes < 1: # We need to check if we are above or below?
                if last == "DOWN":
                    offset = offset + shiftAmount
                    break
                offset = offset + shiftAmount # add 10 microvolt
                last = "UP"
            elif minCodes > 1:
                if last == "UP":
                    break
                offset = offset - shiftAmount # sub 10 microvolt
                last = "DOWN"
            else:
                break
            awg2.configureChannelALT(1,'SIN',FS_Set/2,offset, frequency)
        awg2.configureChannelALT(1,'SIN',FS_Set/2,offset, frequency)
    else:
        offset = FS_Set/4
        deltaOffset = 0
        last = None
        shiftAmount = 0.00005
        threshold = 2 # Code threshold
        while(1):
            smu1.configureChannel(1,'VOLT',0.7,0.0001)
            time.sleep(0.5)
            LA.capture()
            LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
            DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
            DATA.loadData() # Load the Data We Just Measured
            DATA.convertDataToHex() # Convert Data to HEX Format
            DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
            DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
            avCode = statistics.mean(DATA.synchronousDataInt)
            print("Adjusting Sine Minimum. Current av Code: " + str(avCode))
            if avCode < -1*threshold: # We need to check if we are above or below?
                if last == "DOWN":
                    deltaOffset = deltaOffset - shiftAmount
                    break
                deltaOffset = deltaOffset - shiftAmount # add 10 microvolt
                last = "UP"
            elif avCode > threshold:
                if last == "UP":
                    break
                deltaOffset = deltaOffset + shiftAmount # sub 10 microvolt
                last = "DOWN"
            else:
                break
            awg2.configureChannelALT(1,'SIN',FS_Set/2,offset-deltaOffset, frequency)
            awg2.configureChannelALT(2,'SIN',FS_Set/2,offset+deltaOffset, frequency)
            break
        awg2.configureChannelALT(1,'SIN',FS_Set/2,offset-deltaOffset, frequency)
        awg2.configureChannelALT(2,'SIN',FS_Set/2,offset+deltaOffset, frequency)


    SAR_Depth = 9
    SAR_Offset = 0
    SAR_Offset_Increment = (V_CIC_max-V_CIC_min)/2
    Smaller = False
    V_CIC_Try = None
    last_level_under_MaxCode = None
    last_level_under_MaxSlope = None

    for i in range(SAR_Depth):
        continue
        try:
            os.remove(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv")
        except:
            pass
        if Smaller == False:
            SAR_Offset = SAR_Offset + SAR_Offset_Increment
        else:
            SAR_Offset = SAR_Offset - SAR_Offset_Increment
        V_CIC_Try = V_CIC_min + SAR_Offset
        smu1.configureChannel(1,'VOLT',V_CIC_Try,0.0001)
        time.sleep(0.5)
        LA.capture()
        LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
        DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
        DATA.loadData() # Load the Data We Just Measured
        DATA.convertDataToHex() # Convert Data to HEX Format
        DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
        DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
        peakCodes = max(DATA.synchronousDataInt)
        minCodes = min(DATA.synchronousDataInt)
        diff = np.gradient(DATA.synchronousDataInt)
        print("Trying Voltage: "+ str(V_CIC_Try)+" Current Peak Code: "+str(peakCodes) +" Max Slope: " + str(max(diff)))
        if max(diff) >= MaxSlope or peakCodes > MaxCode or minCodes < MinCode:
            Smaller = True
        else:
            Smaller = False
            last_level_under_MaxSlope = V_CIC_Try
        LA.closeCapture()
        SAR_Offset_Increment = SAR_Offset_Increment/2
    LA.close()
    DATA2 = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
    DATA2.loadData() # Load the Data We Just Measured
    DATA2.convertDataToHex() # Convert Data to HEX Format
    DATA2.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
    DATA2.convertSynchHexdataToInt() # Generate an Int Array of Data too.
    fig, ax = plt.subplots()
    ax.plot([float(item) for  item in DATA2.synchronousDataTimeStamp], DATA2.synchronousDataInt)
    plt.show()
    awg1.disableALL()
    awg2.disableALL()
    smu1.disableALL()
    return last_level_under_MaxSlope
