import os
import Keysight.awg as awg
import Keysight.smu as smu
import Keysight.scope as scope
import Saleae.saleae_utils as saleae_utils
import Saleae.saleae_atd as saleae_atd
import Test_Cases.defaultTest as dft
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import FFT.noise_lib as noiselib
import csv
import Calibration.auto_full_scale_ramp as afs

rootdir = os.path.join("c:"+os.sep,"Users","eecis","Desktop","Arturo_Sem_Project","Automation_git","BDC-Automation","Results","Resistor")
matchflag = False
for subdir, dirs, files in os.walk(rootdir):
    if matchflag:
        break
    for file in files:
        if "_post_processed_CODE" in file:
            #print(os.path.join(subdir, file))
            new_data_file = os.path.join(subdir, file)
            try:
                [timestamps, codes] = noiselib.readWaveformCSV(new_data_file)
                mean, s1,s2,s3 = noiselib.findNoiseValue(codes)
                print(str(mean)+" "+str(s1))
                if mean >905.31 and mean < 905.32:
                    print("Found Match:"+new_data_file)
                    matchflag = True
                    break
            except:
                print("Skipped: "+new_data_file)
