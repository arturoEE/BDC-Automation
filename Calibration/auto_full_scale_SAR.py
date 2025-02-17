import Keysight.awg as awg
import Keysight.smu as smu
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import time
import os
import numpy as np
import matplotlib.pyplot as plt


# Designed for the Single Ended Use Case

## Auto Full Scale Script:
## SMU: Output Max value of Sine
## The Lower the Bias to CI-Cell is, the larger the LSB.
##
def autoFSSAR(FS_Set):
    # Configure Test Equipment:
    awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
    smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
    #smu2 = smu.SMU("")

    # Maybe Also use Scope and Monitor Buffer for this...?
    # Need a Second SMU if we want Monitor Buffer

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
    awg1.configureChannel(1,'SQU',0.0,0.8,1000)
    awg1.configureChannel(2,'SIN',0.0,FS_Set/2,10)
    awg1.enableALL()

    MaxCode = 1022
    MaxSlope = 200
    V_CIC_max = 0.9
    V_CIC_min = 0.1

    SAR_Depth = 9
    SAR_Offset = 0
    SAR_Offset_Increment = (V_CIC_max-V_CIC_min)/2
    Smaller = False
    V_CIC_Try = None
    last_level_under_MaxCode = None
    last_level_under_MaxSlope = None

    for i in range(SAR_Depth):
        LA = saleae_atd.Saleae(devicePort=10430)
        LA.open()

        LA.configureLogic()
        LA.setCaptureDuration(5)
        LA.setupDigitalTriggerCaptureMode(channel=10)
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
        diff = np.gradient(DATA.synchronousDataInt)
        print("Trying Voltage: "+ str(V_CIC_Try)+" Current Peak Code: "+str(peakCodes) +" Max Slope: " + str(max(diff)))
        #if peakCodes >= MaxCode:
        #    Smaller = True
        #else:
        #    Smaller = False
        #    last_level_under_MaxCode = V_CIC_Try
        if max(diff) >= MaxSlope or peakCodes > MaxCode:
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
    plt.show()
    awg1.disableALL()
    smu1.disableALL()
    return last_level_under_MaxSlope
