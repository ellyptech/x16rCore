from myhdl import block, delay, instance

@block
def clockDriver(clk, DELAY = 5):
    """ Clock driver

    clk -- output signal, 50% duty cycle drived clock
    DELAY -- nano second delay for derived clock
    """
    @instance
    def clkgen():
        while(1):
            yield delay(DELAY)   
            clk.next = not clk
    return clkgen