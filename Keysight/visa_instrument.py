import pyvisa
import time
class Instrument:
    address = None
    rm = None
    inst = None
    def __init__(self, addr):
        self.address = addr
    def open(self):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(self.address)
        time.sleep(1)
    def query(self, msg):
        return self.inst.query(msg)
    def write(self, msg):
        self.inst.write(msg)
        time.sleep(0.3)