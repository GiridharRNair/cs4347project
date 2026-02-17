/*

iverilog -g2012 -o Cohort0x01.part1 Cohort0x01.part1.v 
vvp Cohort0x01.part1

*/


//-------------------------------------------
//
// Breadboard module
// Class module that represents a board for circuit assembly
// Input and output comes from the testbech. 
// Basic logic equations using operators
//
// & ==> AND
// | ==> OR
// ~ ==> NOT
//
//-------------------------------------------

module Breadboard	(w,x,y,z,r0,r1,r2,r3,r4,r5,r6,r7,r8,r9);  
input w,x,y,z;                        
output r0,r1,r2,r3,r4,r5,r6,r7,r8,r9;                      
wire w,x,y,z;							
reg r0, r1, r2, r3, r4, r5, r6, r7, r8, r9;                    

always @ ( w,x,y,z,r0,r1,r2,r3,r4,r5,r6,r7,r8,r9) begin      

    // f0 = w'x'y'z' + w'x'y'z + w'x'yz' + w'xy'z' + w'xy'z + w'xyz + wx'y'z + wx'yz' + wx'yz + wxy'z' + wxy'z + wxyz
    r0= (~w&~x&~y&~z)|(~w&~x&~y&z)|(~w&~x&y&~z)|(~w&x&~y&~z)|(~w&x&~y&z)|(~w&x&y&z)|(w&~x&~y&z)|(w&~x&y&~z)|(w&~x&y&z)|(w&x&~y&~z)|(w&x&~y&z)|(w&x&y&z);

    // f1 = w'x'y'z + w'x'yz + w'xy'z' + w'xyz' + w'xyz + wxy'z' + wxyz
    r1= (~w&~x&~y&z)|(~w&~x&y&z)|(~w&x&~y&~z)|(~w&x&y&~z)|(~w&x&y&z)|(w&x&~y&~z)|(w&x&y&z);

    // f2 = w'xy'z' + w'xyz + wx'y'z' + wx'yz' + wxy'z'
    r2= (~w&x&~y&~z)|(~w&x&y&z)|(w&~x&~y&~z)|(w&~x&y&~z)|(w&x&~y&~z);

    // f3 = w'x'y'z' + w'x'y'z + w'xy'z' + w'xyz' + wx'y'z' + wx'yz' + wxyz'
    r3= (~w&~x&~y&~z)|(~w&~x&~y&z)|(~w&x&~y&~z)|(~w&x&y&~z)|(w&~x&~y&~z)|(w&~x&y&~z)|(w&x&y&~z);

    // f4 = w'x'y'z' + w'x'y'z + w'x'yz' + w'x'yz + w'xy'z' + w'xyz' + wx'y'z' + wx'y'z + wx'yz' + wx'yz + wxy'z + wxyz' + wxyz
    r4= (~w&~x&~y&~z)|(~w&~x&~y&z)|(~w&~x&y&~z)|(~w&~x&y&z)|(~w&x&~y&~z)|(~w&x&y&~z)|(w&~x&~y&~z)|(w&~x&~y&z)|(w&~x&y&~z)|(w&~x&y&z)|(w&x&~y&z)|(w&x&y&~z)|(w&x&y&z);

    // f5 = w'x'y'z' + w'x'y'z + w'x'yz' + w'xy'z + wx'y'z' + wx'yz + wxyz'
    r5= (~w&~x&~y&~z)|(~w&~x&~y&z)|(~w&~x&y&~z)|(~w&x&~y&z)|(w&~x&~y&~z)|(w&~x&y&z)|(w&x&y&~z);

    // f6 = w'x'y'z' + w'xyz' + wx'y'z' + wx'y'z + wx'yz' + wxy'z' + wxyz' + wxyz
    r6= (~w&~x&~y&~z)|(~w&x&y&~z)|(w&~x&~y&~z)|(w&~x&~y&z)|(w&~x&y&~z)|(w&x&~y&~z)|(w&x&y&~z)|(w&x&y&z);

    // f7 = w'x'y'z' + w'x'y'z + w'x'yz' + w'x'yz + w'xy'z + w'xyz' + w'xyz + wx'y'z + wx'yz + wxy'z + wxyz
    r7= (~w&~x&~y&~z)|(~w&~x&~y&z)|(~w&~x&y&~z)|(~w&~x&y&z)|(~w&x&~y&z)|(~w&x&y&~z)|(~w&x&y&z)|(w&~x&~y&z)|(w&~x&y&z)|(w&x&~y&z)|(w&x&y&z);

    // f8 = w'xyz' + w'xyz + wx'y'z' + wx'y'z + wx'yz + wxy'z
    r8= (~w&x&y&~z)|(~w&x&y&z)|(w&~x&~y&~z)|(w&~x&~y&z)|(w&~x&y&z)|(w&x&~y&z);

    // f9 = w'x'y'z' + w'x'yz + w'xy'z + w'xyz' + wx'y'z + wx'yz + wxy'z + wxyz' + wxyz
    r9= (~w&~x&~y&~z)|(~w&~x&y&z)|(~w&x&~y&z)|(~w&x&y&~z)|(w&~x&~y&z)|(w&~x&y&z)|(w&x&~y&z)|(w&x&y&~z)|(w&x&y&z);

    end                              

endmodule                           

//-------------------------------------------
//
// Testbench module
// Class module that represents the main 
// Must have the "Initial" keyword to begin thread
// 
// Generate four inputs for a truth table (a,b,c,d)
// Link the breadboard module (not a call) to run in parallel
// 
// Use a for loop to generate each line of the truth table.
// 
// Goals:
// Have example of the wire/reg parameter passing
// Have examples of errors
//
//-------------------------------------------
module testbench();

	reg [4:0] i; //A loop control for 16 rows of a truth table.
	reg  a;//Value of 2^3
	reg  b;//Value of 2^2
	reg  c;//Value of 2^1
	reg  d;//Value of 2^0
  
	wire  f0,f1,f2,f3,f4,f5,f6,f7,f8,f9; //Outputs of the breadboard module, which are wires.
  

	Breadboard bb8(a,b,c,d,f0,f1,f2,f3,f4,f5,f6,f7,f8,f9); 
 	 
	initial begin
   	
		//$display acts like a java System.println command.
		$display ("|##|A|B|C|D|F0|F1|F2|F3|F4|F5|F6|F7|F8|F9|");
		$display ("|==+=+=+=+=+==+==+==+==+==+==+==+==+==+==|");
  
		for (i = 0; i <16; i = i + 1) 
		begin										
			a=(i/8);//High bit
			b=(i/4);
			c=(i/2);
			d=(i/1);//Low bit	
		 
			// Time delay to allow the breadboard module to process the new inputs and update the outputs before we display them. 
			#12;

			//Display one row of the truth table
			$display ("|%2d|%1d|%1d|%1d|%1d| %1d| %1d| %1d| %1d| %1d| %1d| %1d| %1d| %1d| %1d|",i,a,b,c,d,f0,f1,f2,f3,f4,f5,f6,f7,f8,f9);
			
			//Every fourth row of the table, put in a marker for easier reading.
			if(i%4==3) 
			begin 								
				$write ("|--+-+-+-+-+--+--+--+--+--+--+--+--+--+--|\n");	
			end 								

		end										
 
		//A time delay of 10 time units. 
		#10; 
		
		$finish;
		
	end  
  
endmodule