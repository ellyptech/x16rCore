from myhdl import block, Signal, intbv, delay, instance, always_comb
from pyhdl.gluelogic.grayCode import bin2gray, gray2bin


@block
def fifo(din, we, inbusy, inclk, rd, rdout, outbusy, dout, outclk, hfull, rst, length,
         DATA= DATA, ADDR=ADDR, UPPER=UPPER, LOWER=LOWER, OFFSET=OFFSET):
    
    mem = [Signal(modbv(0)[DATA:]) for i in range(2**ADDR)]
    in_addr  = Signal(modbv(0)[ADDR+1:])
    out_addr = Signal(modbv(0)[ADDR+1:])
    in_addr_1  = Signal(modbv(0)[ADDR+1:])
    out_addr_1 = Signal(modbv(0)[ADDR+1:])
    in_addr_gray  = Signal(modbv(0)[ADDR+1:])
    out_addr_gray = Signal(modbv(0)[ADDR+1:])
    in_addr_gray_1  = Signal(modbv(0)[ADDR+1:])
    out_addr_gray_1 = Signal(modbv(0)[ADDR+1:])
    in_addr_gray_2  = Signal(modbv(0)[ADDR+1:])
    out_addr_gray_2 = Signal(modbv(0)[ADDR+1:])
    next_in_addr = Signal(modbv(0)[ADDR+1:])
    next_out_addr = Signal(modbv(0)[ADDR+1:])
    in_length   = Signal(modbv(0)[ADDR:])
    out_length   = Signal(modbv(0)[ADDR:])
    canread  = Signal(bool(0))
    inMsbflag  = Signal(bool(0))
    outMsbflag = Signal(bool(0))
    
    bin2gray0_inst = grayCode.bin2gray(in_addr, in_addr_gray, DATA=ADDR+1)
    bin2gray1_inst = grayCode.bin2gray(out_addr, out_addr_gray, DATA=ADDR+1)
    gray2bin0_inst = grayCode.gray2bin(in_addr_gray_2, in_addr_1, DATA = ADDR+1)
    gray2bin1_inst = grayCode.gray2bin(out_addr_gray_2, out_addr_1, DATA = ADDR+1)
    
    
    @always_seq(inclk.posedge, reset = rst)
    def in_addr_two_ff_sync():
        out_addr_gray_1.next = out_addr_gray
        out_addr_gray_2.next = out_addr_gray_1
        
    @always_seq(outclk.posedge, reset = rst)
    def out_addr_two_ff_sync():
        length.next = out_length
        in_addr_gray_1.next = in_addr_gray
        in_addr_gray_2.next = in_addr_gray_1
        
    @always_comb
    def diffLogic():
        in_length.next = in_addr - out_addr_1
        out_length.next = in_addr_1 - out_addr
        
    @always_comb
    def writeLogic():
        inbusy.next = in_length >= UPPER-1
        next_in_addr.next = in_addr
        if we:
            next_in_addr.next = in_addr + 1
    
    @always_comb
    def readLogic2():
        canread.next = (out_length > 0) and rd and not outbusy
        
    @always_comb
    def readLogic():
        next_out_addr.next = out_addr
        hfull.next = out_length >= OFFSET
        if out_length >= LOWER:
            outbusy.next = 0
        elif out_length < 1:
            outbusy.next = 1
        if canread:
            next_out_addr.next = out_addr + 1
            
    @always(inclk.posedge)
    def writemem():
        if we:
            mem[in_addr[ADDR:0]].next = din
            
    @always(outclk.posedge)
    def readmem():
        dout.next  = 0
        rdout.next = 0
        if canread:
            dout.next = mem[out_addr[ADDR:0]]
            rdout.next = 1
            
    @always_seq(inclk.posedge, reset = rst)
    def write():
        in_addr.next = next_in_addr
        outMsbflag.next = outMsbflag
        if not in_addr[ADDR] and not out_addr_1[ADDR]:
            outMsbflag.next = 0
        if out_addr_1[ADDR]:
            outMsbflag.next = 1
        if in_addr[ADDR] and outMsbflag:
            in_addr.next = next_in_addr[ADDR:]
            outMsbflag.next = 0
    
    @always_seq(outclk.posedge, reset = rst)
    def read():
        out_addr.next = next_out_addr
        inMsbflag.next = inMsbflag
        if not in_addr_1[ADDR] and not out_addr[ADDR]:
            inMsbflag.next = 0
        if in_addr_1[ADDR]:
            inMsbflag.next = 1
        if out_addr[ADDR] and inMsbflag:
            out_addr.next = next_out_addr[ADDR:]            
            inMsbflag.next = 0
    
    return instances()

