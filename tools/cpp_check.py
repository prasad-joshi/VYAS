#!/usr/bin/python

import commands

import log

class CppCheck(object):

    CPPCHECK_PATH = None
    WHICH = "/usr/bin/which"

    def __init__(self, file_name):
        """ initialization
        """
        self.file_name = file_name      # source file to analyse

        if not self.CPPCHECK_PATH:
            self.__cpp_check_path__()
        pass

    def _run_command(self, cmd):
        """ run a command
        """
        return commands.getstatusoutput(cmd)

    def __cpp_check_path__(self):
        """ find cppcheck path
        """
        r, o = self._run_command(self.WHICH + " cppcheck")
        if r != 0:
            assert(0)
        self.CPPCHECK_PATH = o
        return r

    def is_installed(self):
        """ check if cppcheck tool is installed
        """
        r = self.__cpp_check_path__()
        if r == 0:
            return 0
        return 1

    def run_cpp_check(self, args):
        """ run cppcheck
        """
        # for now let's assume --enable=style argument, we might decide to
        # change it latter on
        default_args = " --enable=style "
        return self._run_command(self.CPPCHECK_PATH + default_args + args)

    def analyse(self):
        """ analyse source code using cppcheck
        """
        log.log(3, "analysing cpp code using cppcheck")
        r, o = self.run_cpp_check(self.file_name)
        log.log(3, o)
