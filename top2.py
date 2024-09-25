import Calibration.auto_full_scale_improved as afs
import Test_Cases.sndr_sample as sndr
import Test_Cases.basic_samplev2_triggerExp as bs2
import csv

#bs2.basic_test(0.5)
#input()
print(afs.autoFS(0.06, single=False))
#exit()
#a = sndr.sndr_sample(0.05, 0.598,1000)

#with open('out_0v5.csv', 'w', newline='') as f:
#    writer = csv.writer(f)
#    writer.writerows(a)