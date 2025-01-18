import Keysight.awg as awg
import Keysight.smu as smu
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import time
import os
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots()
rootdir = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","singleSNDR_new","new3FF_FT_10HZ_VEXVC_hiz_AD2_0VCM2024-11-05_17-34-10")
name1 = "Input_v0.12Sub_v0.022000000000000002_f9.9639892578125"
file1 = os.path.join(rootdir,name1, name1+".csv")
DATA2 = saleae_utils.SaleaeData(file1, ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], 11)
DATA2.loadData() # Load the Data We Just Measured
DATA2.convertDataToHex() # Convert Data to HEX Format
DATA2.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
DATA2.convertSynchHexdataToInt() # Generate an Int Array of Data too.
print(max(DATA2.synchronousDataInt))
ax.plot([float(item) for  item in DATA2.synchronousDataTimeStamp], DATA2.synchronousDataInt)

name1 = "Input_v0.12Sub_v0.030555555555555555_f9.9639892578125"
file1 = os.path.join(rootdir,name1, name1+".csv")
DATA2 = saleae_utils.SaleaeData(file1, ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], 11)
DATA2.loadData() # Load the Data We Just Measured
DATA2.convertDataToHex() # Convert Data to HEX Format
DATA2.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
DATA2.convertSynchHexdataToInt() # Generate an Int Array of Data too.
print(max(DATA2.synchronousDataInt))
#ax.plot([float(item) for  item in DATA2.synchronousDataTimeStamp], DATA2.synchronousDataInt)

name1 = "Input_v0.12Sub_v0.04333333333333333_f9.9639892578125"
file1 = os.path.join(rootdir,name1, name1+".csv")
DATA2 = saleae_utils.SaleaeData(file1, ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK", "D10"], 11)
DATA2.loadData() # Load the Data We Just Measured
DATA2.convertDataToHex() # Convert Data to HEX Format
DATA2.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
DATA2.convertSynchHexdataToInt() # Generate an Int Array of Data too.
print(max(DATA2.synchronousDataInt))
#ax.plot([float(item) for  item in DATA2.synchronousDataTimeStamp], DATA2.synchronousDataInt)
plt.show()