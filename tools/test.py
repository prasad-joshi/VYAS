#!/usr/bin/python

import sys
sys.path.append("lib/")
from cpp_check import *
from splint import *
from valgrind import *

from CTool import *

tools = [CppCheck("CPrograms/test.c"), splint(), valgrind()]

b = CTool()

for t in tools:
    b.register_tool(t)

b.analyse()
