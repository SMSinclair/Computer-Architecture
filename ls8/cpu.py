"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg  = [0] * 8 
        self.reg[7] = 244 # R7 is the SP
        self.pc = 0
        self.fl = 0
        self.halted = False
        self.ir = 0

    def load(self, filename):
        """Load an ls8 program into memory."""

        path = 'examples/' + filename
        address = 0

        with open(path) as f:
            for line in f:
                # skip empty lines and comments
                if line[0].isnumeric()==False:
                    continue
                self.ram[address] = int(line[0:8], 2)
                address += 1

    def add(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]
    
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def call(self, operand_a):
        '''
        Calls a subroutine (function) at the address stored in the register.

        Machine code:

        01010000 00000rrr
        50 0r
        '''
        
        # The address of the ***instruction*** _directly after_ `CALL` is pushed onto 
        # the stack. This allows us to return to where we left off when the subroutine 
        # finishes executing.
        
        # decrement the SP
        self.reg[7] -= 1
        # put the value in the specified register in address pointed to by SP
        self.ram[self.reg[7]] = self.pc + 2
        
        # The PC is set to the address stored in the given register. We jump to that 
        # location in RAM and execute the first instruction in the subroutine. The PC 
        # can move forward or backwards from its current location.
        self.pc = self.reg[operand_a]
    
    def ret(self):
        '''
        Return from subroutine.

        Machine Code:
        00010001
        11
        '''

        # Pop the value from the top of the stack and store it in the `PC`.

        #Copy the value from the address pointed to by `SP` to the given register.
        self.pc = self.ram[self.reg[7]]
        # Increment `SP`.
        self.reg[7] += 1

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: {self.pc+1} | {self.ram_read(self.pc)} {self.ram_read(self.pc + 1)} {self.ram_read(self.pc + 2)} | ", end = '')

        for i in range(8):
            print(f" {self.reg[i]} ", end = '')

        print()

    def hlt(self):
        self.halted = True
    
    def increment_pc(self, value):
        self.pc += value

    def ldi(self, register, value):
        self.reg[register] = value

    def mul(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

    def prn(self, register_num):
        # print(f"Register number: {register_num}")
        print(self.reg[register_num])
    
    def push(self, register):
        '''
        Push the value in the given register on the stack.
        '''
        # decrement the SP
        self.reg[7] -= 1
        # put the value in the specified register in address pointed to by SP
        self.ram[self.reg[7]] = self.reg[register]
        # print(f"Top of the stack is {self.ram[self.reg[7]]} at address {self.reg[7]}")

    def pop(self, register):
        '''
        Pop the value at the top of the stack into the given register.
        '''
        #Copy the value from the address pointed to by `SP` to the given register.
        self.reg[register] = self.ram[self.reg[7]]
        # Increment `SP`.
        self.reg[7] += 1

    def ram_read(self, address):
        # address = self.pc
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        while self.halted == False:
            self.ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            # self.trace()

            if self.ir == 130:
                self.ldi(operand_a, operand_b)
            
            if self.ir == 71:
                self.prn(operand_a)

            if self.ir == 1:
                self.hlt()

            if self.ir == 162:
                self.mul(operand_a, operand_b)

            if self.ir == 69:
                self.push(operand_a)

            if self.ir == 70:
                self.pop(operand_a)

            if self.ir == 80:
                self.call(operand_a)

            if self.ir == 17:
                self.ret()
            
            if self.ir == 160:
                self.add(operand_a, operand_b)

            if self.ir !=80 and self.ir != 17:
                self.pc += ((self.ir >> 6)+1) # use bitshift to incremenet PC past operands