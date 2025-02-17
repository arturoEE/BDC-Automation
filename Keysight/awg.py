from Keysight import visa_instrument
class AWG(visa_instrument.Instrument):
    frequency = [1,1]
    amplitude = [0.001,0.001]
    offset = [0.001,0.001]
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
        self.frequency[channel-1] = f
        self.write('SOURce'+str(channel)+':FREQuency '+str(self.frequency[channel-1]))
        print('SOUR'+str(channel)+':FREQ '+str(self.frequency[channel-1])+' HZ')
    def setAmplitude(self,channel,a):
        self.amplitude[channel-1] = a
        self.write('SOUR'+str(channel)+':VOLT +'+str(a)+' V')
    def setMinMax(self,channel,min,max):
        self.amplitude[channel-1] = max-min
        self.write('SOUR'+str(channel)+':VOLT:LOW +'+str(min)+' V')
        self.write('SOUR'+str(channel)+':VOLT:HIGH +'+str(max)+' V')
    def setPhase(self, channel, phase):
        self.write('SOUR'+str(channel)+':PHAS '+str(phase))
    def syncPhase(self, channel):
        self.write('SOUR'+str(channel)+':PHAS:SYNC')
    def setOffset(self,channel,o):
        self.offset[channel-1] = o
        self.write('SOUR'+str(channel)+':VOLT:OFFS '+str(o))
    def setWaveform(self,channel,w):
        self.waveform[channel-1] = w
        self.write('SOUR'+str(channel)+':FUNC '+self.waveform[channel-1])
    def updateSettings(self): # DO NOT USE
        self.disableALL()
        self.write('SOUR1:APPL:'+self.waveform[0]+' ' +str(self.frequency[0])+ ' HZ, '+str(self.amplitude[0])+' V, '+str(self.offset[0])+' V')
        self.write('SOUR2:APPL:'+self.waveform[1]+' ' +str(self.frequency[1])+ ' HZ, '+str(self.amplitude[1])+' V, '+str(self.offset[1])+' V')
    def configureChannel(self, ch, w, min, max,f):
        self.setWaveform(ch, w)
        self.setMinMax(ch, min, max)
        self.setFrequency(ch, f)
    def configureChannelALT(self, ch, w, ampl, offset,f):
        self.setWaveform(ch, w)
        self.setAmplitude(ch, ampl)
        self.setOffset(ch, offset)
        self.setFrequency(ch, f)
    def setTracking(self,channel, mode): # INV
        self.write('SOUR'+str(channel)+':TRAC '+mode)
    def close(self):
        self.close()