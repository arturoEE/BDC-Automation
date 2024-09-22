import Calibration.auto_full_scale_SAR as afs
import Test_Cases.sndr_sample as sndr
import csv

print(afs.autoFSSAR(0.06))
#exit()
#a = sndr.sndr_sample(0.05, 0.598,1000)

#with open('out_0v5.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerows(a)