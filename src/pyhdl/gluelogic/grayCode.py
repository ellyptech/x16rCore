import os
from myhdl import block, Signal, intbv, delay, instance, always_comb, instances, always_seq, Cosimulation
from random import randrange
from pyhdl import hdlcfg

@block
def bin2gray(B, G, DATA = 8):
    """ Gray encoder.

    B -- input intbv signal, binary encoded
    G -- output intbv signal, gray encoded
    DATA -- bit width default = 8
    """
    @always_comb
    def logic():
        Bext = intbv(0)[DATA+1:]
        Bext[:] = B
        for i in range(DATA):
            G.next[i] = Bext[i+1] ^ Bext[i]

    return logic

@block
def gray2bin(G, B, DATA = 8):
    """ Gray decoder.

    G -- input intbv signal, gray encoded
    B -- output intbv signal, binary encoded
    DATA -- bit width default = 8
    """
    @always_comb
    def logic():
        Gext = intbv(0)[DATA:]
        Gext[:] = G
        for i in range(DATA):
            x = 0
            for j in range(i, DATA):
                x = x ^ Gext[j]
            B.next[i] = x

    return logic

def bin2grayCoSim(B, G, DATA = 8):
    bin2gray_inst = bin2gray(B, G, DATA = DATA)
    name='bin2gray_' + str(DATA)
    bin2gray_inst.convert(hdl='Verilog', header=hdlcfg.header, name=name)
    bin2gray_inst.convert(hdl='Verilog', header=hdlcfg.header, directory=hdlcfg.hdl_path, name=name)
    os.system("iverilog -o bin2gray.o " + \
              "{0}.v ".format(name) + \
              "{0}.v ".format('tb_' + name))
    print("#########")
    return Cosimulation("vvp -m myhdl bin2gray.o -vcd test.vcd", B=B, G=G)

@block
def signalSync(clk, rst, dIn, dOut, DATA = 8):
    """ Gray decoder.
    clk -- clock domain for dOut
    rst -- Reset signal
    dIn -- input intbv signal, belong to different clock domain
    dOut -- output intbv signal, belong to clock domain clk
    DATA -- bit width default = 8
    """
    dInGray, dInGrayCrossed, dOutGray = [Signal(intbv(0)[DATA:]) for i in range(3)]
    
    bin2gray_inst = bin2gray(dIn, dInGray, DATA)
    gray2bin_inst = gray2bin(dOutGray, dOut, DATA)

    @always_seq(clk.posedge, reset = rst)
    def two_ff_sync():
        dInGrayCrossed.next = dInGray
        dOutGray.next = dInGrayCrossed

    return instances()
