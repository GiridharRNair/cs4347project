//===========================================
//
// BrokenEasy v2026
// Dr. Eric Becker
// Spring 2026
//
// First Program Example
// Demonstrate common mistakes in Verilog
//
//===========================================

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
module Breadboard	(w,x,y,z,r1,r2,r3);  //Module Header/Module Begin
input w,x,y,z;                           //Specify inputs
output r1, r2, r3;                       //Specify outputs
wire w,x,y,z;							 //Input is a source, must be of type wire
reg r1,r2,r3;                            //Output is a memory area, must be of type reg

always @ ( w,x,y,z,r1,r2,r3) begin       //with no time constraints (Always)
										 //Create a block of code  (begin)
                                         //when all of these variables are used ( w,x,y,z,r1,r2,r3) 

	//x+y'z                              //The Formula for R1
	r1= (x)|((~y)&z);                    //Bitwise operation of the formula r1

	//Demorgan's						 //Apply Demorgan's Laws to R1
	r2= ~(~(~y&z)&(~x));                 //Bitwise operation of the formula r2

	//wxyz+w'x'y'z'                      //The Formula R3
    r3= (w&x&y&z)|(~w&~x&~y&~z);

    end                                  // Finish the Always block

endmodule                                //Module End

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

	//Registers act like local variables
	reg [4:0] i; //A loop control for 16 rows of a truth table.
	reg  a;//Value of 2^3
	reg  b;//Value of 2^2
	reg  c;//Value of 2^1
	reg  d;//Value of 2^0
  
	//A wire can hold the return of a function
	wire  f1,f2,f3;
  
	//Modules can be either functions, or model chips. 
	//They are instantiated like an object of a class, 
	//with a constructor with parameters.  They are not invoked,
	//but operate like a thread.
	Breadboard bb8(a,b,c,d,f1,f2,f3);
 	 
	//Initial means "start," like a Main() function.
	//Begin denotes the start of a block of code.	
	initial begin
   	
		//$display acts like a java System.println command.
		$display ("|##|A|B|C|D|F1|F2|F3|");
		$display ("|==+=+=+=+=+==+==+==|");
  
		//A for loop, with register i being the loop control variable.
		for (i = 0; i <16; i = i + 1) 
		begin										//Open the code block of the for loop
			a=(i/8);//High bit
			b=(i/4);
			c=(i/2);
			d=(i/1);//Low bit	
		 
			//Oh, Dr. Becker, do you remember what belongs here?
			#12;

			//Display one row of the truth table
			$display ("|%2d|%1d|%1d|%1d|%1d| %1d| %1d| %1d|",i,a,b,c,d,f1,f2,f3);
			
			//Every fourth row of the table, put in a marker for easier reading.
			if(i%4==3) 
			begin 									//Open block for If statement
				$write ("|--+-+-+-+-+--+--+--|\n");	//Write acts a bit like a java System.print
			end 									//Close block for if statement.

		end											//End of the for loop code block
 
		//A time delay of 10 time units. Hashtag Delay
		#10; 
		
		//The finish command, like System.exit(0) in Java.
		$finish;
		
	end  //End the code block of the main thread (initial)
  
endmodule //Close the testbench module