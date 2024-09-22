from Keysight import visa_instrument
class SMU(visa_instrument.Instrument):
    force = [0,0]
    limit = [0,0]
    mode = ["VOLT","VOLT"] # CURR, VOLT
    def __init__(self, addr):
        self.address = addr
        self.open()
    def enableCH1(self):
        self.write('OUTP1 1')
    def enableCH2(self):
        self.write('OUTP2 1')
    def enableALL(self):
        self.write('OUTP1 1')
        self.write('OUTP2 1')
    def disableCH1(self):
        self.write('OUTP1 0')
    def disableCH2(self):
        self.write('OUTP2 0')
    def disableALL(self):
        self.write('OUTP1 0')
        self.write('OUTP2 0')
    def setScreen(self, msg):
        self.write('DISP:TEXT "'+ msg +'"')
    def setMode(self,channel,m):
        self.mode[channel] = m
        self.write(':SOUR'+str(channel+1)+':FUNC:MODE '+m)
    def setForce(self,channel,f):
        self.force[channel] = f
        self.updateSettings()
    def setLimit(self,channel,l):
        self.limit[channel] = l
        self.updateSettings()
    def getSns(self, channel):
        if self.mode[channel] == "VOLT":
            return "CURR"
        elif self.mode[channel] == "CURR":
            return "VOLT"
        else:
            return None
    def updateSettings(self):
        self.write(':SOUR1:'+str(self.mode[0])+':LEV:IMM:AMPL '+str(self.force[0]))
        self.write(':SENS1:'+str(self.getSns(0))+':PROT '+str(self.limit[0]))
        self.write(':SOUR2:'+str(self.mode[1])+':LEV:IMM:AMPL '+str(self.force[1]))
        self.write(':SENS2:'+str(self.getSns(1))+':PROT '+str(self.limit[1]))
    def configureChannel(self, ch, m, f, l):
        self.setMode(ch, m)
        self.setForce(ch, f)
        self.setLimit(ch, l)
    def close(self):
        self.close()