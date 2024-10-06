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

def autoFS(FS_Set, frequency, single=True, negative=False):
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
    smu1.configureChannel(1,'VOLT',0.3,0.0001)
    smu1.enableALL()

    # Clock Waveform 250 Hz and Input VEXC Sinusoid at FS
    #awg2.configureChannelALT(1,'SIN',FS_Set/2,FS_Set/4, frequency)
    #awg2.setPhase(1,0)
    #awg2.configureChannelALT(2,'SIN',FS_Set/2,FS_Set/4, frequency)
    #awg2.setPhase(2,180)
    #awg2.syncPhase(2)
    awg1.configureChannel(1,'SQU',0.0,0.8,1000)
    awg1.setPhase(1,30)
    awg1.configureChannel(2,'SQU',0.0,0.8,1000)
    awg1.setPhase(2,0)
    awg1.syncPhase(2)
    awg1.enableALL()
    awg2.enableALL()


    LA = saleae_atd.Saleae(devicePort=10430)
    LA.open()

    LA.configureLogic()
    LA.setCaptureDuration(3/frequency)
    LA.setupDigitalTriggerCaptureMode(channel=10)
    

    if single:
        MaxCode = 1021
        MaxSlope = 10000
        MinCode = 1
    else:
        MaxCode = 1021
        MaxSlope = 10000
        MinCode = -1022
    V_CIC_max = 0.9
    V_CIC_min = 0.2

    if single:
        if negative==False:
            offset = FS_Set/2
            last = None
            shiftAmount = 0.005
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
                if minCodes < 4: # We need to check if we are above or below?
                    offset = offset + shiftAmount # add 10 microvolt
                    last = "UP"
                elif minCodes > 4:
                    if last == "UP" and minCodes < 15:
                        break
                    offset = offset - shiftAmount # sub 10 microvolt
                    last = "DOWN"
                else:
                    break
                shiftAmount = shiftAmount/1.5
                awg2.configureChannelALT(1,'SIN',FS_Set,offset, frequency)
            awg2.configureChannelALT(1,'SIN',FS_Set,offset, frequency)
        else:
            offset = FS_Set/4+0.002
            last = None
            shiftAmount = 0.0001
            while(1):
                LA.open()

                LA.configureLogic()
                LA.setCaptureDuration(5)
                LA.setupDigitalTriggerCaptureMode(channel=10)
                smu1.configureChannel(1,'VOLT',0.7,0.0001)
                time.sleep(0.5)
                LA.capture()
                LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
                DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
                DATA.loadData() # Load the Data We Just Measured
                DATA.convertDataToHex() # Convert Data to HEX Format
                DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
                DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
                minCodes = max(DATA.synchronousDataInt)
                print("Adjusting Sine Maximum. Current Max Code: " + str(minCodes))
                if minCodes == 0:
                    break
                if minCodes > -1: # We need to check if we are above or below?
                    if last == "DOWN":
                        pass
                        #offset = offset + shiftAmount
                        #break
                    offset = offset + shiftAmount # add 10 microvolt
                    last = "UP"
                elif minCodes < -1:
                    if last == "UP":
                        pass
                        #break
                    offset = offset - shiftAmount # sub 10 microvolt
                    last = "DOWN"
                else:
                    break
                awg2.configureChannelALT(1,'SIN',FS_Set/2,offset, frequency)
                LA.close()
            awg2.configureChannelALT(1,'SIN',FS_Set/2,offset, frequency)
    else:
        pass
        # First, let's grab the max and min values for the sinusoid
        # smu1.configureChannel(1,'VOLT',0.3,0.0001)
        # time.sleep(0.5)
        # LA.capture()
        # LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
        # DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
        # DATA.loadData() # Load the Data We Just Measured
        # DATA.convertDataToHex() # Convert Data to HEX Format
        # DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
        # DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
        # minimum = min(DATA.synchronousDataInt)
        # maximum = max(DATA.synchronousDataInt)
        # difference = abs(maximum) - abs(minimum)
        # print("Adjusting Offset. Min: " + str(minimum) + " Max: " + str(maximum) + " Diff: " + str(difference))
        # # Now it's time to adjust the offset.
        # up = False
        # SAR_Offset = 0
        # V_off_max = 0.01
        # V_off_min = -0.01
        # SAR_Offset_Increment = (V_off_max-V_off_min)/2
        # if difference < 1:
        #     up = True
        # SAR_Depth = 7
        # for i in range(SAR_Depth):
        #     try:
        #         os.remove(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv")
        #     except:
        #         pass
        #     if up == True:
        #         SAR_Offset = SAR_Offset + SAR_Offset_Increment
        #     else:
        #         SAR_Offset = SAR_Offset - SAR_Offset_Increment
        #     V_off_Tryp = FS_Set/4 + SAR_Offset
        #     V_off_Tryn = FS_Set/4 - SAR_Offset
        #     awg2.configureChannelALT(2, 'SIN', FS_Set/2, V_off_Tryn, frequency)
        #     awg2.configureChannelALT(2, 'SIN', FS_Set/2, V_off_Tryp, frequency)
        #     awg2.setPhase(1,0)
        #     awg2.setPhase(2,180)
        #     awg2.syncPhase(2)
        #     time.sleep(0.5)
        #     LA = saleae_atd.Saleae(devicePort=10430)
        #     LA.open()

        #     LA.configureLogic()
        #     LA.setCaptureDuration(5)
        #     LA.setupDigitalTriggerCaptureMode(channel=10)
        
        #     LA.capture()
        #     LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
        #     DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
        #     DATA.loadData() # Load the Data We Just Measured
        #     DATA.convertDataToHex() # Convert Data to HEX Format
        #     DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
        #     DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
        #     minimum = min(DATA.synchronousDataInt)
        #     maximum = max(DATA.synchronousDataInt)
        #     difference = abs(maximum) - abs(minimum)
        #     print("Adjusting Offset. Min: " + str(minimum) + " Max: " + str(maximum) + " Diff: " + str(difference)+ " Try: " + str(V_off_Tryp))
        #     if difference < 1:
        #         up = True
        #     else:
        #         up = False
        #     LA.closeCapture()
        #     LA.close()
        #     SAR_Offset_Increment = SAR_Offset_Increment/2

        # offset = FS_Set/4
        # last = None
        # shiftAmount = 0.00005
        # while(1):
        #     smu1.configureChannel(1,'VOLT',0.7,0.0001)
        #     time.sleep(0.5)
        #     LA.capture()
        #     LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
        #     DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
        #     DATA.loadData() # Load the Data We Just Measured
        #     DATA.convertDataToHex() # Convert Data to HEX Format
        #     DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
        #     DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
        #     minCodes = min(DATA.synchronousDataInt)
        #     print("Adjusting Sine Minimum. Current Min Code: " + str(minCodes))
        #     if minCodes < 1: # We need to check if we are above or below?
        #         if last == "DOWN":
        #             offset = offset + shiftAmount
        #             break
        #         offset = offset + shiftAmount # add 10 microvolt
        #         last = "UP"
        #     elif minCodes > 1:
        #         if last == "UP":
        #             break
        #         offset = offset - shiftAmount # sub 10 microvolt
        #         last = "DOWN"
        #     else:
        #         break
        #     awg2.configureChannelALT(1,'SIN',FS_Set/2,offset, frequency)
        # awg2.configureChannelALT(1,'SIN',FS_Set/2,offset, frequency)
        # awg2.setAmplitude(1,0)
        # awg2.setAmplitude(2,FS_Set/2)
        # offset = FS_Set/4+0.002
        # last = None
        # shiftAmount = 0.0001
        # while(1):
        #     LA.open()

        #     LA.configureLogic()
        #     LA.setCaptureDuration(5)
        #     LA.setupDigitalTriggerCaptureMode(channel=10)
        #     smu1.configureChannel(1,'VOLT',0.7,0.0001)
        #     time.sleep(0.5)
        #     LA.capture()
        #     LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
        #     DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
        #     DATA.loadData() # Load the Data We Just Measured
        #     DATA.convertDataToHex() # Convert Data to HEX Format
        #     DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
        #     DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
        #     minCodes = max(DATA.synchronousDataInt)
        #     print("Adjusting Sine Maximum. Current Max Code: " + str(minCodes))
        #     if minCodes == 0:
        #         break
        #     if minCodes > -1: # We need to check if we are above or below?
        #         if last == "DOWN":
        #             pass
        #             #offset = offset + shiftAmount
        #             #break
        #         offset = offset + shiftAmount # add 10 microvolt
        #         last = "UP"
        #     elif minCodes < -1:
        #         if last == "UP":
        #             pass
        #             #break
        #         offset = offset - shiftAmount # sub 10 microvolt
        #         last = "DOWN"
        #     else:
        #         break
        #     awg2.configureChannelALT(2,'SIN',FS_Set/2,offset, frequency)
        #     LA.close()
        # awg2.configureChannelALT(2,'SIN',FS_Set/2,offset, frequency)
        # awg2.setAmplitude(1,FS_Set/2)
    LA.open()
    LA.configureLogic()
    LA.setCaptureDuration(3/frequency)
    LA.setupDigitalTriggerCaptureMode(channel=10)
    smu1.configureChannel(1,'VOLT',0.7,0.0001)
    SAR_Depth = 9
    SAR_Offset = 0
    SAR_Offset_Increment = (V_CIC_max-V_CIC_min)/2
    Smaller = False
    V_CIC_Try = None
    last_level_under_MaxCode = None
    last_level_under_MaxSlope = None

    for i in range(SAR_Depth):
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
        time.sleep(2)
        LA = saleae_atd.Saleae(devicePort=10430)
        LA.open()

        LA.configureLogic()
        LA.setCaptureDuration(3/frequency)
        LA.setupDigitalTriggerCaptureMode(channel=10)
    
        LA.capture()
        LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
        DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
        DATA.loadData() # Load the Data We Just Measured
        DATA.convertDataToHex() # Convert Data to HEX Format
        DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
        DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
        if negative == False:
            peakCodes = max(DATA.synchronousDataInt)
        else:
            peakCodes = min(DATA.synchronousDataInt)
        maxd = max(DATA.synchronousDataInt)
        mind = min(DATA.synchronousDataInt)
        peakCodes = max([abs(maxd),abs(mind)])
        diff = np.gradient(DATA.synchronousDataInt)
        print("Trying Voltage: "+ str(V_CIC_Try)+" Current Peak Code: "+str(peakCodes) +" Max Slope: " + str(max(diff)))
        if max(diff) >= MaxSlope or abs(peakCodes) > MaxCode:
            Smaller = True
        else:
            Smaller = False
            last_level_under_MaxSlope = V_CIC_Try
        LA.closeCapture()
        LA.close()
        SAR_Offset_Increment = SAR_Offset_Increment/2
    #LA.close()
    DATA2 = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
    DATA2.loadData() # Load the Data We Just Measured
    DATA2.convertDataToHex() # Convert Data to HEX Format
    DATA2.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
    DATA2.convertSynchHexdataToInt() # Generate an Int Array of Data too.
    fig, ax = plt.subplots()
    ax.plot([float(item) for  item in DATA2.synchronousDataTimeStamp], DATA2.synchronousDataInt)
    #plt.show()
    return last_level_under_MaxSlope
