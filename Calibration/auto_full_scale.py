import awg
import smu
import saleae_atd
import time
import numpy as np

# Designed for the Single Ended Use Case

## Auto Full Scale Script:
## SMU: Output Max value of Sine
## The Lower the Bias to CI-Cell is, the larger the LSB.
##
def autoFS(FS_Set):
    # Configure Test Equipment:
    awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
    smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
    smu2 = smu.SMU("")

    # Maybe Also use Scope and Monitor Buffer for this...?
    # Need a Second SMU if we want Monitor Buffer

    # Clock Waveform 250 Hz.
    awg1.configureChannel(0,'SQU',0.4,0.2,250)
    awg1.enableCH1()
    awg1.setScreen("Clock")

    # Monitoring Buffer 1uA Reference Current
    smu1.configureChannel(0,'CURR', 0.000001, 1.8)
    smu1.enableCH1()
    smu1.setScreen("EXC/IBUF")

    # FS Voltage Default
    smu1.configureChannel(1,'VOLT', 0, 0.001)
    smu1.enableCH2()

    smu2.configureChannel(0,'VOLT',FS_Set, 0.001)
    smu2.enableCH1()

    # Setup and Configure Logic Analyzer
    LA = saleae_atd.Saleae(devicePort=10430)
    LA.open()

    LA.configureLogic()
    LA.setCaptureDuration(0.1)
    LA.setupDigitalTriggerCaptureMode(channel=10)


    V_CIC = np.linspace(1.2,0.1,100)
    averageCodes = np.zeros(100,1)

    MaxCode = 1023
    V_CIC_Range = 1.2 # or some default

    for i,voltage in enumerate(V_CIC):
        smu1.setForce(1,V_CIC)
        time.sleep(0.5)
        LA.capture()
        LA.saveCapture(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Python_Automation\est.sal")
        ## Do Post Processing Here!
        averageCode = 1024
        if averageCode == MaxCode-1:
            V_CIC_Range = voltage
            break
        LA.closeCapture()
    LA.close()
    awg1.disableALL()
    smu1.disableALL()
    smu2.disableALL()
    return V_CIC_Range
