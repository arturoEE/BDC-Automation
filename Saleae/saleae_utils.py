import csv

class SaleaeData():
    filepath = ""
    channelLabel = {}
    triggerChannel = None
    data = None
    def __init__(self,datafile, channelLabels, trigger):
        self.filepath = datafile
        self.channelLabel = channelLabels # Maybe make an alternative input of lists?
        self.triggerChannel = trigger
    def loadData(self,):
        with open(self.filepath, newline='') as csvfile:
            data_reader = csv.reader(csvfile, delimiter =',')
            for row in data_reader:
                pass # Sort and write to Data Variable
    def readHexAtTriggerEdges(self,):
        val_last = None
        trigger_points = []
        for idx, val in enumerate(self.data[self.channelLabel[self.triggerChannel]]):
            if val_last == None:
                val_last = val
                continue
            if val != val_last:
                trigger_points.append(idx)

    def readHexAtFirstTriggerEdge(self,):
        val_last = None
        trigger_point = None
        for idx, val in enumerate(self.data[self.channelLabel[self.triggerChannel]]):
            if val_last == None:
                val_last = val
                continue
            if val != val_last:
                trigger_point = idx
                break
    def readHexAtIndex(self,):
        pass
