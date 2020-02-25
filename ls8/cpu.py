"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg  = [0] * 8
        self.pc = 0
        self.fl = 0
        self.halted = False
        self.ir = 0

    def load(self, filename):
        """Load a program into memory."""

        path = '../asm/' + filename

        program = []

        with open(path) as f:
            for line in f:
                if line == '' or line[0]=='#':
                    continue
                for instruction in line.replace(',', ' ').split():
                    if instruction == 'LDI':
                        program.append(0b10000010)
                    if instruction == 'PRN':
                        program.append(0b01000111)
                    if instruction == 'HLT':
                        program.append(0b00000001)
                    if instruction[0]=='R' and instruction[1].isnumeric():
                        program.append(int(instruction[1]))
                    if instruction.isnumeric():
                        program.append(int(instruction))

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        # print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def hlt(self):
        self.halted = True
    
    def increment_pc(self, value):
        self.pc += value

    def ldi(self, register, value):
        self.reg[register] = value

    def prn(self, register_num):
        # print(f"Register number: {register_num}")
        print(self.reg[register_num])
    
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

            self.pc += ((self.ir >> 6)+1) # use bitshift to incremenet PC past operands