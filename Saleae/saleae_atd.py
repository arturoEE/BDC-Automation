from saleae import automation

class Saleae():
    deviceID = None
    port = None
    config = None
    manager = None
    captureConfig = None
    captureDuration = None
    capture = None
    def __init__(self, devicePort,deviceID=None):
        self.deviceID = deviceID
        self.port = devicePort
    def open(self):
        self.manager = automation.Manager.connect(port=self.port)
    def configureLogic(self, channels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], sampleRate=1_000_000, threshold=1.2):
        self.config = automation.LogicDeviceConfiguration(enabled_digital_channels=channels, digital_sample_rate=sampleRate, digital_threshold_volts=threshold)
    def close(self):
        self.manager.close()
    def capture(self):
        self.capture = self.manager.start_capture(device_configuration=self.config,device_id=self.deviceID,capture_configuration=self.captureConfig)
        self.capture.wait()
    def createAnalyzer(self):
        pass
    def setCaptureDuration(self, t):
        self.captureDuration = t
    def setupDigitalTriggerCaptureMode(self,channel):
        self.captureConfig = automation.CaptureConfiguration(capture_mode=automation.DigitalTriggerCaptureMode(trigger_type=automation.DigitalTriggerType(1), trigger_channel_index=channel, after_trigger_seconds=self.captureDuration))
    def saveCapture(self,savepath):
        self.capture.save_capture(filepath=savepath)
    def exportData(self,savedir):
        self.capture.export_raw_data_csv(directory=savedir, digital_channels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def closeCapture(self):
        self.capture.close()
