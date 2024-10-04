import Keysight.awg as awg
import Keysight.smu as smu
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import time
import os
import matplotlib.pyplot as plt

def autoFS():
    # Configure Test Equipment:
    awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
    #smu1 = #smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
    #smu2 = #smu.SMU("USB0::0x2A8D::0x9501::MY61390603::0::INSTR")

    awg1.disableALL()
    #smu1.disableALL()

    # Configure CI-Cell Voltage
    #smu1.setMode(1,'VOLT')
    #smu1.configureChannel(1,'VOLT',0.3,0.0001)
    #smu1.enableALL()

    awg1.configureChannel(1,'SQU',0.0,0.8,1000)
    awg1.setPhase(1,30)
    awg1.configureChannel(2,'SQU',0.0,0.8,1000)
    awg1.setPhase(2,0)
    awg1.syncPhase(2)
    awg1.enableALL()

    LA = saleae_atd.Saleae(devicePort=10430)
    MaxCode = 1021
    V_CIC_max = 0.9
    V_CIC_min = 0.2

    LA.open()
    LA.configureLogic()
    LA.setCaptureDuration(1)
    LA.setupDigitalTriggerCaptureMode(channel=10)
    #smu1.configureChannel(1,'VOLT',0.7,0.0001)
    SAR_Depth = 10
    SAR_Offset = 0
    SAR_Offset_Increment = (V_CIC_max-V_CIC_min)/2
    Smaller = False
    V_CIC_Try = None
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
        #smu1.configureChannel(1,'VOLT',V_CIC_Try,0.0001)
        time.sleep(2)
        LA = saleae_atd.Saleae(devicePort=10430)
        LA.open()

        LA.configureLogic()
        LA.setCaptureDuration(1)
        LA.setupDigitalTriggerCaptureMode(channel=11)
    
        LA.capture()
        LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG")
        DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
        DATA.loadData() # Load the Data We Just Measured
        DATA.convertDataToHex() # Convert Data to HEX Format
        DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
        DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
        peakCodes = max(DATA.synchronousDataInt)
        maxd = max(DATA.synchronousDataInt)
        mind = min(DATA.synchronousDataInt)
        peakCodes = max([abs(maxd),abs(mind)])
        print("Trying Voltage: "+ str(V_CIC_Try)+" Current Peak Code: "+str(peakCodes))
        if abs(peakCodes) > MaxCode:
            Smaller = True
        else:
            Smaller = False
            last_level_under_MaxSlope = V_CIC_Try
        LA.closeCapture()
        LA.close()
        SAR_Offset_Increment = SAR_Offset_Increment/2
    DATA2 = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 11)
    DATA2.loadData() # Load the Data We Just Measured
    DATA2.convertDataToHex() # Convert Data to HEX Format
    DATA2.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
    DATA2.convertSynchHexdataToInt() # Generate an Int Array of Data too.
    fig, ax = plt.subplots()
    ax.plot([float(item) for  item in DATA2.synchronousDataTimeStamp], DATA2.synchronousDataInt)
    #plt.show()
    return last_level_under_MaxSlope
