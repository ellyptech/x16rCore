module tb_bin2gray_8;

reg [7:0] B;
wire [7:0] G;

initial begin
    $from_myhdl(
        B
    );
    $to_myhdl(
        G
    );
end

bin2gray_8 dut(
    B,
    G
);

endmodule
