#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()

# cpu.trace()

# cpu.ram_write(888, 0)

# print(cpu.ram_read(3))


# cpu.ram_write(123, 0)
# cpu.ram_write(72, 3)

# print(cpu.ram)