import time

from .helper import reconnectInstructions, checkExpReqInstruments

requiredEquipment = {
    "LCR Meter": [
                    {"purpose": "Capacitance", "var": "lcr"}
                ],
    "Multimeter": [
                      {"purpose": "Temperature", "var": "mm"}
                  ],
}


def setup(instruments=None, lcr=0, mm=0, inGui=False):
    if instruments is None:
        instruments = []

    serials = {}
    if lcr != 0:
        serials["lcr"] = str(lcr)
    if mm != 0:
        serials["mm"] = str(mm)

    if len(instruments) == 0:
        print("\x1b[;43m No instruments could be recognised / contacted \x1b[m")
        print("")
        reconnectInstructions(inGui)
        raise Exception("No instruments could be recognised / contacted")

    foundReqInstruments = checkExpReqInstruments(requiredEquipment, instruments, serials, inGui)

    foundReqInstruments["mm"]["res"].write("CONF:TCO")
    time.sleep(0.2)
    foundReqInstruments["mm"]["res"].wite("TCO:TYPE T")

    print("\x1b[;42m Instruments ready to use for Curie Weiss experiment \x1b[m")
    print("Proceed as shown:")
    if inGui:
        print("   1 | insts = HallPy_Teach()")
        print("   2 | data = placeHolderExperimentFunction(insts)")
    else:
        print("   1 | cwInsts = hp.curieWeiss.setup(instruments, lcr='XXXXXXXXX', mm='XXXXXXX')")
        print("   2 | data = placeHolderExperimentFunction(insts)")
    print(' ')
    print("\x1b[;43m NOTE : If any instruments are disconnected or turned off after     \x1b[m")
    print("\x1b[;43m        this point you will have to restart and reconnect them      \x1b[m")
    if inGui:
        print("\x1b[;43m        to the PC and rerun the `HallPy_Tech()` function            \x1b[m")
    else:
        print("\x1b[;43m        to the PC and rerun 'initInstruments()' and setupCW()       \x1b[m")

    return foundReqInstruments