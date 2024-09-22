import Test_Cases.inputSweepSNDR as sndrtest

TEST = sndrtest.inputSweepSNDR("debugging")
TEST.configureInstruments()
TEST.run()

# Notes:
# AFC Really needs to be a method of test i think..
# Variables need to be carefully considered...