import csv
import numpy as np

class SaleaeData():
    def __init__(self,datafile, channelLabels, trigger, triggerType="FALLING"):
        self.filepath = ""
        self.channelLabel = {} # Dictionary Corresponding physical channel addresses to their labels. Ordered.
        self.triggerChannel = None # Channel to subsample our data on event.
        self.data = None # Store Data
        self.dataHEX = []
        self.synchronousDataHex = []
        self.synchronousDataInt = []
        self.synchronousSignBit = []
        self.synchronousDataTimeStamp = []
        self.triggerType = None # Rising, Falling
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
        for idx, val in enumerate([i[3] for i in self.dataHEX]):
            if val_last == None:
                val_last = val
                continue
            if val != val_last:
                if self.triggerType == "RISING" and val > val_last:
                    #if self.dataHEX[idx][1] != "0x0": ## Remove
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
            self.synchronousSignBit.append(self.dataHEX[point][2]) # Sign Bit
    def readHexAtFirstTriggerEdge(self):
        val_last = None
        trigger_point = None
        for idx, val in enumerate([i[3] for i in self.dataHEX]): ## Dont Hard Code in the Future --- also this wont work because the list is the other direction
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
        tempint = [int(x,0) for x in self.synchronousDataHex]
        for idx, val in enumerate(tempint):
            val_to_append = None
            polarity = 1
            if int(self.synchronousSignBit[idx]) == 1:
                val_to_append = val+1 # +1 so not 2 zero codes?
                polarity = 1
            elif int(self.synchronousSignBit[idx]) == 0:
                val_to_append = 1023-val
                polarity = -1
            else:
                print("SIGN ERROR")
            self.synchronousDataInt.append(val_to_append*polarity)
    def convertDataToHex(self):
        for i, dataline in enumerate(self.data):
            if i == 0:
                continue ## Skip the Header line
            binstr = ""
            for element in dataline[1:11]: ## hwo 2 handle the negative data?
                binstr = binstr+str(element)
            binstr = binstr[::-1]
            signbit = dataline[11]
            hexstr = hex(int(binstr,2))
            self.dataHEX.append([dataline[0], hexstr,signbit, dataline[self.triggerChannel+1]])
    def convertDataToHex9b(self):
        for i, dataline in enumerate(self.data):
            if i == 0:
                continue ## Skip the Header line
            binstr = ""
            #print(dataline)
            #print(dataline[1:11])
            for j, element in enumerate(dataline[1:11]): ## hwo 2 handle the negative data?
                #if j > 0:
                binstr = binstr+str(element)
            #print(binstr)
            binstr = binstr[::-2]
            signbit = dataline[11]
            hexstr = hex(int(binstr,2))
            #break
            self.dataHEX.append([dataline[0], hexstr,signbit, dataline[self.triggerChannel+1]])
    def convertDataToHex8b(self):
        for i, dataline in enumerate(self.data):
            if i == 0:
                continue ## Skip the Header line
            binstr = ""
            for element in dataline[3:11]: ## hwo 2 handle the negative data?
                binstr = binstr+str(element)
            binstr = binstr[::-1]
            signbit = dataline[11]
            hexstr = hex(int(binstr,2))
            self.dataHEX.append([dataline[0], hexstr,signbit, dataline[self.triggerChannel+1]])
    def importConfigFromInst(self, instance):
        pass
    def returnMeanValueSynchData(self):
        pass
    def returnMaxValueSynchData(self):
        pass