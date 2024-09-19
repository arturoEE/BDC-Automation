import awg
import smu
import saleae_atd
import time
import numpy as np

# Single Ended Gain Measurement

# Configure Test Equipment:
awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")

# Clock Waveform 250 Hz.
awg1.configureChannel(0,'SQU',0.4,0.2,250)
awg1.enableCH1()
awg1.setScreen("Clock")

# Monitoring Buffer 1uA Reference Current
smu1.configureChannel(0,'CURR', 0.000001, 1.8)
smu1.enableCH1()
smu1.setScreen("EXC/IBUF")

# Excitation Voltage Default = 0
smu1.configureChannel(1,'VOLT', 0, 0.001)
smu1.enableCH2()

# Setup and Configure Logic Analyzer
LA = saleae_atd.Saleae(devicePort=10430)
LA.open()

LA.configureLogic()
LA.setCaptureDuration(0.1)
LA.setupDigitalTriggerCaptureMode(channel=10)


VEXC = np.linspace(0,0.1,10)
averageCode = np.zeros(10,1)

for i,voltage in enumerate(VEXC):
    smu1.setForce(1,VEXC)
    time.sleep(0.5)
    LA.capture()
    LA.saveCapture(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Python_Automation\est.sal")
    ## Do Post Processing Here!
    LA.closeCapture()
LA.close()

