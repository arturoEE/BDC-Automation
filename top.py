import Test_Cases.inputSweepSNDR as sndrsweep
import Test_Cases.singleSNDR_2AWG as sndrsingle
import Test_Cases.differentialSNDR as sndrdiff

#TEST = sndrsweep.inputSweepSNDR("debugging")
TEST = sndrsingle.singleSNDR("dualAWGcheck")
#TEST = sndrdiff.differentialSNDR("arturodiffdebug")
TEST.configureInstruments()
TEST.run()

# Notes:
# AFC Really needs to be a method of test i think..
# Variables need to be carefully considered...