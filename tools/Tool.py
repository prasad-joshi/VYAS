#!/usr/bin/python

from abc import ABCMeta, abstractmethod

class Tools:
    __metaclass__ = ABCMeta     # this is Abstract Base Class (ABC)
    def __init__(self):
        """ intialize ABC
        """
        self.tools = []     # list of registered tools

    def _add_tool(self, tool):
        """ internal method to add a new tool
        """
        self.tools.append(tool)

    def register_tool(self, tool):
        """ add a new tool
        """
        self.tools.append(tool)
        self.add_tool(tool)

    def analyse(self):
        """ analyse source code
        """
        for t in self.tools:
            t.analyse()

