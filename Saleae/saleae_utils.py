import csv
import numpy as np

class SaleaeData():
    filepath = ""
    channelLabel = {} # Dictionary Corresponding physical channel addresses to their labels. Ordered.
    triggerChannel = None # Channel to subsample our data on event.
    data = None # Store Data
    dataHEX = []
    synchronousDataHex = []
    synchronousDataInt = []
    synchronousDataTimeStamp = []
    triggerType = None # Rising, Falling
    def __init__(self,datafile, channelLabels, trigger, triggerType="FALLING"):
        self.filepath = datafile
        self.channelLabel = channelLabels # Maybe make an alternative input of lists?
        self.triggerChannel = trigger
        self.triggerType = triggerType
    def loadData(self):
        with open(self.filepath,'r') as datafile:
            data_iter = csv.reader(datafile,
                delimiter = ",",
                quotechar = '"')
            self.data = [data for data in data_iter]
    def readHexAtTriggerEdges(self):
        val_last = None
        trigger_points = [] # List of Rising Edges
        for idx, val in enumerate([i[2] for i in self.dataHEX]):
            if val_last == None:
                val_last = val
                continue
            if val != val_last:
                if self.triggerType == "RISING" and val > val_last:
                    trigger_points.append(idx)
                    val_last = val
                    continue
                elif self.triggerType == "FALLING" and val < val_last:
                    trigger_points.append(idx)
                    val_last = val
                    continue
                else:
                    val_last = val
                    continue ## Change in the Polarity we dont care about
            else:
                val_last = val
        for point in trigger_points:
            self.synchronousDataHex.append(self.dataHEX[point][1]) # 
            self.synchronousDataTimeStamp.append(self.dataHEX[point][0]) # Saleae Logged relative time stamp
    def readHexAtFirstTriggerEdge(self):
        val_last = None
        trigger_point = None
        for idx, val in enumerate([i[2] for i in self.dataHEX]): ## Dont Hard Code in the Future --- also this wont work because the list is the other direction
            if val_last == None:
                val_last = val
                continue
            if val != val_last:
                if self.triggerType == "RISING" and val > val_last:
                    trigger_point = idx
                    break
                elif self.triggerType == "FALLING" and val < val_last:
                    trigger_point = idx
                    break
                else:
                    val = val_last
                    continue ## Change in the Polarity we dont care about
        return self.dataHEX[idx][1]
    def readHexAtIndex(self):
        pass
    def convertSynchHexdataToInt(self):
        self.synchronousDataInt = [int(x,0) for x in self.synchronousDataHex]
    def convertDataToHex(self):
        for i, dataline in enumerate(self.data):
            if i == 0:
                continue ## Skip the Header line
            binstr = ""
            for element in dataline[1:10]:
                binstr = binstr+str(element)
            binstr = binstr[::-1]
            hexstr = hex(int(binstr,2))
            self.dataHEX.append([dataline[0], hexstr, dataline[self.triggerChannel+1]])
    def importConfigFromInst(self, instance):
        pass
    def returnMeanValueSynchData(self):
        pass
    def returnMaxValueSynchData(self):
        pass