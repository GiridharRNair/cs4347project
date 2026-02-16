module NAND_tb();

logic a, b, y;
int error=0;

NAND dut(a, b, y); // device under test i.e. the gate we want to test

    initial 
        begin
            $dumpfile("nand.vcd");
            $dumpvars(0, NAND_tb);
            
            a=0; b=0;   #10;
            assert(y===1) else error=1;
            
            b=1;        #10;
            assert(y===1) else error=1;
            
            a=1; b=0;   #10;
            assert(y===1) else error=1;
            
            b=1;        #10;
            assert(y===0) else error=1;
        end
    
    always@(a, b, y, error)
        if(!error) $display("Time=%Dt inputs:a=%b\t b=%b\t output:y=%b", $time, a, b, y);            
        
        else
            begin
                $error("Test fail at time=%Dt inputs:a=%b\t b=%b\t output:y=%b", $time, a, b, y);
                error=0;      
            end
    
endmodule