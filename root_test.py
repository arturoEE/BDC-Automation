import ROOT
import requests
import numpy as np
import matplotlib.pyplot as plt
# Gauss with plateau
fs = "[0]*TMath::Exp(-0.5*((x-[2])/[3])^2)+[1]*(1-TMath::Erf((x-[2])/([3]*sqrt(2))))/2 "

#Draw the function
height = 4000
plateau = 1000
center = 300
width = 20
c = ROOT.TCanvas(f"func_canvas", "c0 Title")
par = np.array((height,plateau,center, width))
func = ROOT.TF1("func", fs, 100., 500., 4)
for i,p in enumerate(par):
    func.SetParameter(i, p)
func.Draw()
c.Draw()