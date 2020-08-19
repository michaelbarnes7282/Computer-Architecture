"""CPU functionality."""

import sys

LDI = "0b10000010"
PUSH = "0b01000101"
POP = "0b01000110"
PRN = "0b01000111"
HLT = "0b00000001"
MULT = "0b10100010"


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.reg[7] = 0xf4

        self.branchtable = {}
        self.branchtable[LDI] = self.LDI
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[PRN] = self.PRN
        self.branchtable[HLT] = self.HLT
        self.branchtable[MULT] = self.MUL

    def HLT(self):
        self.running = False
        self.pc += 1

    def LDI(self):
        reg_num = int(self.ram[self.pc + 1], 2)
        value = int(self.ram[self.pc + 2], 2)
        self.reg[reg_num] = value
        self.pc += 3

    def PRN(self):
        reg_num = int(self.ram[self.pc + 1], 2)
        print(self.reg[reg_num])
        self.pc += 2

    def MUL(self):
        reg1_num = int(self.ram[self.pc + 1], 2)
        reg2_num = int(self.ram[self.pc + 2] ,2)
        self.reg[reg1_num] *= self.reg[reg2_num]
        self.pc += 3

    def PUSH(self):
        self.reg[7] -= 1
        reg_num = int(self.ram[self.pc + 1], 2)
        value = self.reg[reg_num]

        top_of_stack_addr = self.reg[7]
        self.ram[top_of_stack_addr] = value

        self.pc += 2

    def POP(self):
        reg_num = int(self.ram[self.pc + 1], 2)
        value = self.ram[self.reg[7]]
        self.reg[reg_num] = value
        self.reg[7] += 1
        self.pc += 2

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, value, pc):
        self.ram[pc] = value

    def load(self):
        """Load a program into memory."""

        address = 0

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

        if len(sys.argv) != 2:
            print("usage: cpu.py progname")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()

                    if len(temp) == 0:
                        continue

                    if temp[0][0] == '#':
                        continue

                    try:
                        self.ram[address] = format(int(temp[0], 2), '#010b')

                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)

                    address += 1

        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        if address == 0:
            print("Program was empty!")
            sys.exit(3)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram[self.pc]
            self.branchtable[ir]()
            