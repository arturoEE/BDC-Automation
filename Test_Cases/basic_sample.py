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
def basic_test(FS_Set, CIC_Set):
    # Configure Test Equipment:
    awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
    smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
    #smu2 = smu.SMU("")

    # Maybe Also use Scope and Monitor Buffer for this...?
    # Need a Second SMU if we want Monitor Buffer

    awg1.disableALL()
    smu1.disableALL()
    # Monitoring Buffer 1uA Reference Current
    smu1.setMode(0,'CURR')
    smu1.configureChannel(0,'CURR', 0.000001, 0.9)

    # Configure CI-Cell Voltage
    smu1.setMode(1,'VOLT')
    smu1.configureChannel(1,'VOLT',0.65,0.0001)
    smu1.enableALL()

    # Clock Waveform 250 Hz and Input VEXC Sinusoid at FS
    awg1.configureChannel(1,'SQU',0.0,0.4,1000)
    awg1.configureChannel(2,'SIN',0.0,FS_Set/2,10)
    awg1.enableALL()

    input("Press Enter after configuring scan chain to continue...")

    # Setup and Configure Logic Analyzer
    LA = saleae_atd.Saleae(devicePort=10430)
    LA.open()

    LA.configureLogic()
    LA.setCaptureDuration(1)
    LA.setupDigitalTriggerCaptureMode(channel=10)

    smu1.configureChannel(1,'VOLT',CIC_Set,0.0001)
    time.sleep(0.5)
    LA.capture()
    LA.exportData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Results")
    DATA = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Results\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 10)
    DATA.loadData() # Load the Data We Just Measured
    DATA.convertDataToHex() # Convert Data to HEX Format
    DATA.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
    DATA.convertSynchHexdataToInt() # Generate an Int Array of Data too.
    #os.remove(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv")
    fig, ax = plt.subplots()
    ax.plot([float(item) for  item in DATA.synchronousDataTimeStamp], DATA.synchronousDataInt)
    plt.show()
    ax.cla()
    LA.closeCapture()
    LA.close()
    awg1.disableALL()
    smu1.disableALL()
