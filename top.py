import Test_Cases.inputSweepSNDR as sndrsweep
import Test_Cases.singleSNDR as sndrsingle

#TEST = sndrsweep.inputSweepSNDR("debugging")
TEST = sndrsingle.singleSNDR("noisedebug_timbrd")
TEST.configureInstruments()
TEST.run()

# Notes:
# AFC Really needs to be a method of test i think..
# Variables need to be carefully considered...