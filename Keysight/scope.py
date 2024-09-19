import visa_instrument
class SCOPE(visa_instrument.Instrument):
    source = None # BUS1 BUS2 , analog channels?
    points_mode = None
    points = None
    out_format = None
    address = None
    def __init__(self, addr, source="BUS1", points_mode="MAX", points=1, out_format="ASCii"):
        self.address = addr
        self.open()
        self.source = source
        self.points_mode = points_mode
        self.points = points
        self.out_format = out_format
    def setScreen(self, msg):
        self.write('DISP:TEXT "'+ msg +'"')
    def setSource(self,source):
        self.source = source
        self.write('WAVeform:SOURce ' + str(self.source))
    def setPointsMode(self,mode):
        self.points_mode = mode
        self.write('WAVeform:POINts:MODE ' + str(self.mode))
    def setPoints(self,points):
        self.points = points
        self.write('WAVeform:POINts ' + str(self.points))
    def setFormat(self,out_format):
        self.out_format = out_format
        self.write('WAVeform:FORMat ' + str(self.out_format))
    def sampleScope(self):
        data = self.query(':WAV:DATA?')
        return data
