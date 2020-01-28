#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
print(cpu.run())

# cpu.trace()

# cpu.ram_write(888, 0)

# result = cpu.ram_read(3)


# cpu.ram_write(123, 0)
# cpu.ram_write(72, 3)

# print(cpu.ram)