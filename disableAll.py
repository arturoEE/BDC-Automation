from Keysight import awg
from Keysight import smu
import Keysight.scope as scope
awg1 = awg.AWG("USB0::0x0957::0x5707::MY59004759::0::INSTR")
smu1 = smu.SMU("USB0::0x2A8D::0x9501::MY61390158::0::INSTR")
scope1 = scope.SCOPE("USB0::0x2A8D::0x1776::MY58032037::0::INSTR")
scope1.disableWaveGenClock()
awg1.disableALL()
smu1.disableALL()
