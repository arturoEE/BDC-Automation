import Test_Cases.inputSweepSNDR as sndrsweep
#import Test_Cases.singleSNDR_2AWG as sndrsingle
import Test_Cases.singleSNDR_imroved as sndrsingle
import Test_Cases.differentialSNDR as sndrdiff

#TEST = sndrsweep.inputSweepSNDR("debugging")
#TEST = sndrsingle.singleSNDR(1,"sanitychecknew")
TEST = sndrdiff.differentialSNDR("3FF_FIA_2P_AD2", 10)
TEST.configureInstruments()
TEST.run()

# Notes:
# AFC Really needs to be a method of test i think..
# Variables need to be carefully considered...