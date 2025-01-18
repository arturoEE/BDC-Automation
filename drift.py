import re
import matplotlib.pyplot as plt
import numpy as np

def runningMean(x, N):
    y = np.zeros((len(x),))
    for ctr in range(len(x)):
         y[ctr] = np.sum(x[ctr:(ctr+N)])
    return y/N

meanvals = []
samples = []
sample = 0
with open('short_drift.txt', 'r') as file:
    for line in file:
        if re.match(r"Mean \(LSB\): (\d+.\d+)", line):
            m = re.search(r"Mean \(LSB\): (\d+.\d+)",line)
            meanvals.append(float(m.group(1)))
            samples.append(sample)
            sample = sample + 1
            print(m.group(1))
plt.style.use('seaborn-v0_8-deep')
fig, ax = plt.subplots()
plt.grid()
filtered = runningMean(meanvals, 10)
#[10* i for i in samples]
ax.plot(meanvals)
plt.title("Short Term Drift over time")
plt.xlabel("Time (s)")
plt.ylabel("Code")
np.savetxt("short_duration_drift.csv",meanvals,delimiter=',')
plt.show()