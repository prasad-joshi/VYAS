#!/usr/bin/python

from cpp_check import *
from splint import *
from valgrind import *

from CTool import *

tools = [CppCheck("test.c"), splint(), valgrind()]

b = CTool()

for t in tools:
    b.register_tool(t)

b.analyse()
