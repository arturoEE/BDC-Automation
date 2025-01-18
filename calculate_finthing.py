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
import FFT.jang_fft as fftlib
import csv
import Calibration.auto_full_scale_improved as afs


input_freq = fftlib.chooseFin(10, 1000, 2**20)
print(input_freq)