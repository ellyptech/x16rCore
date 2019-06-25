import os
from myhdl import block, Signal, intbv, delay, instance, always_comb, instances, ResetSignal, StopSimulation, always
from random import randrange
from pyhdl import gluelogic
from pyhdl.gluelogic.grayCode import bin2gray, gray2bin, signalSync, bin2grayCoSim
from pyhdl.gluelogic.clock import clockDriver


@block
def bin2grayBench(bin2gray = bin2gray, DATA = 8):

    B = Signal(intbv(0)[DATA:])
    G = Signal(intbv(0)[DATA:])
    B2 = Signal(intbv(0)[DATA:])

    bin2gray_inst = bin2gray(B, G, DATA)
    gray2bin_inst = gray2bin(G, B2, DATA)

    n = 2**DATA

    @instance
    def stimulus():
        for i in range(n):
            B.next = i
            yield delay(10)
            #print "B: " + bin(B, width) + "| G_v: " + bin(G_v, width)
            #print bin(G, width)
            #print bin(G_v, width)
            #print("%d" % G)
            print("%d" % B, "%d" % G, "%d" % B2)
            assert B == B2, "Error occured !!"

    return instances()


@block
def signalSyncBench(DATA = 8):

    n = 2**DATA
    
    dIn, dOut     = [Signal(intbv(0)[DATA:]) for i in range(2)]
    clkIn, clkOut = [Signal(bool(0))         for i in range(2)]
    rst = ResetSignal(0, active=1, isasync=False)
    
    clockDriver0_inst = clockDriver(clkIn , DELAY = 5)
    clockDriver1_inst = clockDriver(clkOut, DELAY = 7)
    signalSync_inst   = signalSync(clkOut, rst, dIn, dOut, DATA = 8)
    
    @instance
    def ResetStimulus():
        yield delay(15)
        rst.next = rst.active
        yield delay(10)
        rst.next = not rst.active
        
        for i in range(n):
            dIn.next = i
            yield clkIn.posedge
            print("%d" % dIn, "%d" % dOut)
            assert B == B2, "Error occured !!"
        #assert False, "Error occured !!"
        raise StopSimulation()

    return instances()


def test0(tmpdir):
    os.chdir(tmpdir)
    assert bin2grayBench(bin2gray = bin2gray, DATA = 8).verify_convert() == 0
    
    
#def test1(tmpdir):
#    os.chdir(tmpdir)
#    assert signalSyncBench().verify_convert() == 0
    
def test1(tmpdir):
    os.chdir(tmpdir)
    tb = bin2grayBench(bin2gray = bin2grayCoSim, DATA = 8)
    tb.run_sim(duration=500000)
