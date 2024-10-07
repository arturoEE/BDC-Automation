import Test_Cases.inputSweepSNDR as sndrsweep
#import Test_Cases.singleSNDR_2AWG as sndrsingle
import Test_Cases.singleSNDR_imroved as sndrsingle
import Test_Cases.differentialSNDR as sndrdiff
import Test_Cases.ramp as ramp
import Test_Cases.rampDiffPrompt as rampp
import Test_Cases.rampDiff as rampd

#TEST = sndrsweep.inputSweepSNDR("debugging")
TEST = sndrsingle.singleSNDR(10,"3FF_FIA_0VCM_Debug",0.0)
#TEST = ramp.RAMP("Ramp_Debg",0.0)
#for vcm in [0]:
#vcms = [0.01, 0.02, 0.03, 0.04, 0.05]
#for vcm in vcms:
#TEST = sndrdiff.differentialSNDR("6PEG_AD2_FILT_"+str(vcm)+"VCM_", 10, vcm)
    #TEST = rampd.RAMPD("3FF_6PEG_FIA_VCM_"+str(vcm)+"_",0.02)
TEST.configureInstruments()
TEST.run()
#input("Next Case: "+case+". Press ENTER to continue")


# Notes:
# AFC Really needs to be a method of test i think..
# Variables need to be carefully considered...