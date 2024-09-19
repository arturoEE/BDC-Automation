import csv
import numpy as np

class SaleaeData():
    filepath = ""
    channelLabel = {} # Dictionary Corresponding physical channel addresses to their labels. Ordered.
    triggerChannel = None # Channel to subsample our data on event.
    data = None # Store Data
    triggerType = None # Rising, Falling
    def __init__(self,datafile, channelLabels, trigger, triggerType="RISING"):
        self.filepath = datafile
        self.channelLabel = channelLabels # Maybe make an alternative input of lists?
        self.triggerChannel = trigger
        self.triggerType = triggerType
    def loadData(self,):
        with open(self.filepath, newline='') as csvfile:
            data_reader = csv.reader(csvfile, delimiter =',')
            for row in data_reader:
                pass # Sort and write to Data Variable
    def readHexAtTriggerEdges(self,):
        val_last = None
        trigger_points = [] # List of Rising Edges
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
    def importConfigFromInst(self, instance):
        pass
