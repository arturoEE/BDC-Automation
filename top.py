import awg
import smu
import saleae_atd
import time
#awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
#awg1.configureChannel(0,'SQU',1,0.5,1000)
#awg1.enableCH1()
#awg1.setScreen(str(awg1.frequency))
#smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
#smu1.configureChannel(0,'VOLT', 1, 0.001)
#smu1.enableCH1()
#smu1.setScreen("SMU")
dev = saleae_atd.Saleae(devicePort=10430)
dev.open()
dev.configureLogic()
dev.setCaptureDuration(0.1)
dev.setupDigitalTriggerCaptureMode(channel=10)
time.sleep(1)
dev.capture()
time.sleep(1)
dev.saveCapture(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Python_Automation\est.sal")
dev.closeCapture()
dev.close()