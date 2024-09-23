import Keysight.scope as scope
import time
scope1 = scope.SCOPE("USB0::0x2A8D::0x1776::MY58032037::0::INSTR")
scope1.createWavGenClock(255)
scope1.enableWaveGenClock()
time.sleep(20)
scope1.disableWaveGenClock()