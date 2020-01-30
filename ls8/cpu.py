"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU.
        Add list properties to the `CPU` class to hold 256 bytes of memory and 8
        general-purpose registers.
        add properties for any internal registers you need, e.g. `PC`.
        """
        self.reg = [0] * 8         #register
        self.ram = [0] * 256        
        self.pc = 0                #Program Counter, address of the currently executing instruction
        self.branchtable = {}
        self.branchtable[0b00000001] = self.handle_HLT
        self.branchtable[0b10000010] = self.handle_LDI
        self.branchtable[0b01000111] = self.handle_PRN
        self.branchtable[0b10100010] = self.handle_MUL
        self.branchtable[0b01000101] = self.handle_PUSH
        self.branchtable[0b01000110] = self.handle_POP

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        with open(filename) as f:
            for line in f:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == "":
                    continue
                val = int(num, 2)
                self.ram[address] = val
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def handle_HLT(self):
        self.pc = 0
        return 'HLT'

    def handle_LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3 

    def handle_PRN(self):
        index = self.ram_read(self.ram[self.pc] +1)
        print(self.reg[index])
        self.pc += 2

    def handle_MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('MUL', (operand_a), (operand_b))
        self.pc += 3

    def handle_PUSH(self):
        """
        Push the value in the given register on the stack.
        1. Decrement the `SP`.
        2. Copy the value in the given register to the address pointed to by`SP`.
        """
        SP = 7
        address = self.ram_read(self.pc + 1)
        value = self.reg[address]
        # Decrement the SP.
        self.reg[SP] -= 1
        # Copy the value in the given register to the address pointed to by SP.
        self.ram[self.reg[SP]] = value
        # Increment PC by 2
        self.pc += 2

    def handle_POP(self):
        """
        Pop the value at the top of the stack into the given register.
        1. Copy the value from the address pointed to by `SP` to the given register.
        2. Increment `SP`.
        """
        SP = 7
        address = self.ram[self.pc + 1]
        # Copy the value from the address pointed to by SP to the given register.
        value = self.ram[self.reg[SP]]
        self.reg[address] = value
        # Increment SP.
        self.reg[SP] += 1
        # Increment PC by 2
        self.pc += 2

    def run(self):
        """Run the CPU.
        """

        running = True
        while running:

            IR = self.ram_read(self.pc) 
            try:
                return_command = self.branchtable[IR]()
                if return_command == 'HLT':
                    running = False
            except KeyError:
                print(f'Error: Unknow command: {IR}')
                sys.exit(1)

            

    def ram_read(self, address):
        """
        should accept the address to read and return the value stored there.
        """
        return self.ram[address]

    def ram_write(self, value, address):
        """should accept a value to write, and the address to write it to."""
        self.ram[address] = value