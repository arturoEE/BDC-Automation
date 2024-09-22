import Keysight.awg as awg
import Keysight.smu as smu
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import time
import os
import numpy as np
import matplotlib.pyplot as plt
DATA2 = saleae_utils.SaleaeData(r"C:\Users\eecis\Desktop\Arturo_Sem_Project\Automation_git\BDC-Automation\Calibration\FSLOG\digital.csv", ["D0","D1","D2","D3","D4","D5","D6","D7","D8","D9","CLK"], 10)
DATA2.loadData() # Load the Data We Just Measured
DATA2.convertDataToHex() # Convert Data to HEX Format
DATA2.readHexAtTriggerEdges() # Read the data at trigger edges (FALLING is default)
DATA2.convertSynchHexdataToInt() # Generate an Int Array of Data too.
print(max(DATA2.synchronousDataInt))
fig, ax = plt.subplots()
ax.plot([float(item) for  item in DATA2.synchronousDataTimeStamp], DATA2.synchronousDataInt)
plt.show()