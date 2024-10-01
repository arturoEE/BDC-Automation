import Test_Cases.inputSweepSNDR as sndrsweep
#import Test_Cases.singleSNDR_2AWG as sndrsingle
import Test_Cases.singleSNDR_imroved as sndrsingle
import Test_Cases.differentialSNDR as sndrdiff

#TEST = sndrsweep.inputSweepSNDR("debugging")
#TEST = sndrsingle.singleSNDR(1,"debuggingVpnoise")
TEST = sndrdiff.differentialSNDR("1F_FIA_6PEG_AD2", 0.5)
TEST.configureInstruments()
TEST.run()

# Notes:
# AFC Really needs to be a method of test i think..
# Variables need to be carefully considered...