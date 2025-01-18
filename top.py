import Test_Cases.inputSweepSNDR as sndrsweep
#import Test_Cases.singleSNDR_2AWG as sndrsingle
import Test_Cases.singleSNDR_imroved as sndrsingle
import Test_Cases.differentialSNDR as sndrdiff
import Test_Cases.ramp as ramp
import Test_Cases.rampDiffPrompt as rampp
import Test_Cases.rampDiff as rampd
import Test_Cases.Resistor as res
import Test_Cases.spine as spine
import time
import Test_Cases.differentialSNDR_1awg as sndrdiff2
import Test_Cases.singleSNDR_new as sndrsingle
import Test_Cases.singleSNDR_new_moving_mean2awg as sndrsingle_mm
#TEST = sndrdiff.differentialSNDR("SNDR_AD8_3FF_FIA_"+str(10)+""+str(0)+"VCM",10, 0.0)

#while True:
#for freq in [1, 10, 100, 200, 300, 400, 499]:
#TEST = sndrsingle.singleSNDR("new3FF_FT_"+str(10)+"HZ_VEXVC_hiz_AD7_"+str(0)+"VCM_really_zero_os",10, -0.0005) # -0.001 for 1 code
freq = 10
#TEST = sndrsingle_mm.singleSNDR_mm("ResCIC_PeakSNDR_new3FF_FT_"+str(freq)+"HZ_VEXVC_hiz_4Really_"+str(0),freq, -0.0018) # -0.001 for 1 code
for vcm in [ 0.0]:
    TEST = sndrdiff.differentialSNDR("FIA_2p_10G_"+str(vcm)+"VCM",10, vcm)
    TEST.configureInstruments()
    TEST.run()