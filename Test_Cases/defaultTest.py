import Keysight.awg as awg
import Keysight.smu as smu
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import time
import shutil
import os
from datetime import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

class Test():
    resultsfolderpath = None
    testname = ""
    date = ""
    note = ""
    resultsdir = None
    saleaedataname = "digital.csv"
    # Format \resultsfolderpath\testname-note-date\subtest?
    def __init__(self):
        pass
    def generateLoggingFolder(self):
        self.date = dt.now().isoformat()
        #resultdirnorm = self.resultsfolderpath+"\\"+self.testname+"\\"+self.note+"-"#+self.date)
        self.resultsdir = os.path.join(self.resultsfolderpath, self.testname,self.note+dt.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(self.resultsdir, exist_ok=True)
    def saveData(self, templogdir,note):
        # First We copy the data
        fullTempPath = os.path.join(templogdir,self.saleaedataname)
        fullResultPath = os.path.join(self.resultsdir,note)
        try:
            os.mkdir(fullResultPath)
        except:
            pass
        csvFullResultPath = os.path.join(fullResultPath,note+".csv")
        shutil.copy(fullTempPath, csvFullResultPath)
        return os.path.join(fullResultPath,note)