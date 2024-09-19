import visa_instrument
class AWG(visa_instrument.Instrument):
    frequency = [0,0]
    amplitude = [0,0]
    offset = [0,0]
    enable = [0,0]
    waveform = ["SIN","SIN"] # SIN, SQU
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
    def setFrequency(self,channel,f):
        self.frequency[channel] = f
        self.updateSettings()
    def setAmplitude(self,channel,a):
        self.amplitude[channel] = a
        self.updateSettings()
    def setOffset(self,channel,o):
        self.offset[channel] = o
        self.updateSettings()
    def setWaveform(self,channel,w):
        self.waveform[channel] = w
        self.updateSettings()
    def updateSettings(self):
        self.write('SOUR1:APPL:'+self.waveform[0]+' ' +str(self.frequency[0])+ ' HZ, '+str(self.amplitude[0])+' V, '+str(self.offset[0])+' V')
        self.write('SOUR2:APPL:'+self.waveform[1]+' ' +str(self.frequency[1])+ ' HZ, '+str(self.amplitude[1])+' V, '+str(self.offset[1])+' V')
    def configureChannel(self, ch, w, a, o ,f):
        self.setWaveform(ch, w)
        self.setAmplitude(ch, a)
        self.setOffset(ch, o)
        self.setFrequency(ch, f)