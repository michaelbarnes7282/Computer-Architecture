"""CPU functionality."""

import sys

LDI = "0b10000010"
PUSH = "0b01000101"
POP = "0b01000110"
PRN = "0b01000111"
HLT = "0b00000001"
MULT = "0b10100010"
CALL = "0b01010000"
RET = '0b00010001'
ADD = "0b10100000"
CMP = "0b10100111"
JEQ = "0b01010101"
JNE = "0b01010110"
JMP = '0b01010100'
AND = "0b10101000"
ST = "0b10000100"
PRA = "0b01001000"


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.SP = 7
        self.FL = "00000000"
        self.ET = "00000001"
        self.GT = "00000010"
        self.LT = "00000100"
        self.reg[self.SP] = 0xf4


        self.branchtable = {}
        self.branchtable[LDI] = self.LDI
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[PRN] = self.PRN
        self.branchtable[HLT] = self.HLT
        self.branchtable[MULT] = self.MUL
        self.branchtable[CALL] = self.CALL
        self.branchtable[RET] = self.RET
        self.branchtable[ADD] = self.ADD
        self.branchtable[CMP] = self.CMP
        self.branchtable[JEQ] = self.JEQ
        self.branchtable[JNE] = self.JNE
        self.branchtable[JMP] = self.JMP
        self.branchtable[AND] = self.AND
        self.branchtable[ST] = self.ST
        self.branchtable[PRA] = self.PRA

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
        self.reg[self.SP] -= 1
        reg_num = int(self.ram[self.pc + 1], 2)
        value = self.reg[reg_num]

        top_of_stack_addr = self.reg[self.SP]
        self.ram[top_of_stack_addr] = value

        self.pc += 2

    def POP(self):
        reg_num = int(self.ram[self.pc + 1], 2)
        value = self.ram[self.reg[7]]
        self.reg[reg_num] = value
        self.reg[self.SP] += 1
        self.pc += 2

    def CALL(self):
        ret_address = self.pc + 2
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = ret_address

        reg_num = int(self.ram[self.pc + 1], 2)
        self.pc = self.reg[reg_num]

    def RET(self):
        ret_addr = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

        self.pc = ret_addr
    
    def ADD(self):
        reg1_num = int(self.ram[self.pc + 1], 2)
        reg2_num = int(self.ram[self.pc + 2] ,2)
        self.alu("ADD", reg1_num, reg2_num)
        self.pc += 3

    def CMP(self):
        reg1_num = int(self.ram[self.pc + 1], 2)
        reg2_num = int(self.ram[self.pc + 2] ,2)
        self.alu("CMP", reg1_num, reg2_num)
        self.pc += 3
    
    def JEQ(self):
        if self.FL == self.ET:
            reg_num = int(self.ram[self.pc + 1], 2)
            value = self.reg[reg_num]
            self.pc = value
        else: self.pc += 2
    
    def JNE(self):
        if self.FL != self.ET:
            reg_num = int(self.ram[self.pc + 1], 2)
            value = self.reg[reg_num]
            self.pc = value
        else: self.pc += 2

    def JMP(self):
        reg_num = int(self.ram[self.pc + 1], 2)
        value = self.reg[reg_num]
        self.pc = value
    
    def AND(self):
        reg1_num = int(self.ram[self.pc + 1], 2)
        reg2_num = int(self.ram[self.pc + 2] ,2)
        self.alu("AND", reg1_num, reg2_num)
        self.pc += 3

    def ST(self):
        addr = self.reg[self.pc + 1]
        value = self.reg[int(self.ram[self.pc + 2] ,2)]
        self.ram[addr] = value
        self.pc += 3
    
    def PRA(self):
        reg_num = int(self.ram[self.pc + 1], 2)
        num = self.reg[reg_num]
        print(chr(num))

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
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = self.ET
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = self.LT
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = self.GT
        elif op == "AND":
            str1 = self.reg[reg_a]
            str2 = self.reg[reg_b]
            res = ""
            for i in range(len()):
                res = res + str(int(str1[i]) & int(str2[i]))

            self.reg[reg_a] = res
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
            int(self.ram_read(self.pc), 2),
            int(self.ram_read(self.pc + 1), 2),
            int(self.ram_read(self.pc + 2), 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram[self.pc]
            self.branchtable[ir]()
            