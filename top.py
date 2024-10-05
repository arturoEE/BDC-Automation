import Test_Cases.inputSweepSNDR as sndrsweep
#import Test_Cases.singleSNDR_2AWG as sndrsingle
import Test_Cases.singleSNDR_imroved as sndrsingle
import Test_Cases.differentialSNDR as sndrdiff
import Test_Cases.ramp as ramp

#TEST = sndrsweep.inputSweepSNDR("debugging")
#TEST = sndrsingle.singleSNDR(0.5,"Test_1KVCM_FIXEDCIC",0.02)
TEST = ramp.RAMP("Ramp_FT_10G_0OFF_SRS0_1Hz_5kHzThor",0.0)
#for vcm in [0]:
#TEST = sndrdiff.differentialSNDR("3FF_FIA_6PEG_AD2_NEW", 301, 0)
TEST.configureInstruments()
TEST.run()

# Notes:
# AFC Really needs to be a method of test i think..
# Variables need to be carefully considered...