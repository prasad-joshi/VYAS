#!/usr/bin/python

from cpp_check import *
from splint import *
from valgrind import *

from CTool import *

tools = [CppCheck(), splint(), valgrind()]

b = CTool()

for t in tools:
    b.register_tool(t)

b.analyse()
