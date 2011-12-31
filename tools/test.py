#!/usr/bin/python

import sys
sys.path.append("lib/")
from cpp_check import *
from splint import *
from valgrind import *

from CTool import *

test_file = "CPrograms/test.c"
exe = "CPrograms/link-list"
tools = [CppCheck(test_file), splint(test_file), valgrind(exe)]

b = CTool()

for t in tools:
    b.register_tool(t)

b.analyse()
