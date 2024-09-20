import numpy as np

def convertCodeToVoltage(nbit, inputfs, codes):
    lsb = inputfs/(2**nbit)
    return [code*lsb for code in codes]
