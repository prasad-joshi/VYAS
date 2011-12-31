#!/usr/bin/python

import log
import utils
import ToolError
from Error import *
import re

class ValgrindLogParser(object):
    def __init__(self, log_file):
        """ initialization
        """
        self.log_file = log_file
        self.no_open_files = 0   # number of open files
        self.open_files = []     # list of open files if self.no_open_files > 4
        self.no_allocs  = 0      # number of allocations
        self.no_free    = 0      # number of frees
        self.allocated  = 0      # number of bytes allocated
        self.definitely = 0      # number of bytes definitely lost
        self.indirectly = 0      # number of bytes indirectly lost
        self.possibly   = 0      # number of bytes possibly lost

    def __str__(self):
        lost = self.definitely + self.indirectly + self.possibly
        r  = "Allocations = {alloc}\n".format(alloc=self.no_allocs)
        r += "Frees = {free}\n".format(free=self.no_free)
        r += "Bytes allocated = {alloc}\n".format(alloc=self.allocated)
        r += "Bytes lost = {lost}\n".format(lost=lost)

        if len(self.open_files) > 0:
            r += "Number of opened but not closed files = {c}\n".format(c=len(self.open_files))
            for (fd, file) in self.open_files:
                r += "\tFile = {f}\n".format(f=file)
        return r

    def __repr__(self):
        return str(self)

    def file_descriptiors(self, line):
        """ parse file descrptor section line by line
        """

        if self.no_open_files == 0:
            """ Format of beging of file descriptor section
            ==3409== FILE DESCRIPTORS: 4 open at exit.
            """
            m = re.match("==\d+== FILE DESCRIPTORS:\s+(\d+).*$", line)
            if m:
                self.no_open_files = m.group(1)
            return
        else:
            """ Valgrind reports minimum 4 open files:
                    3 standard files: stdin, stdout, stderr
                    1 log file which we use to redirect all logs
            """
            if self.no_open_files <= 4:
                # no unclosed file
                return

        """ the process has opened few files which are never closed. Get the
        list of open but unclosed files along with the descriptor allocated
        to it.

        Valgrind reports each open file in following format

        ==3729== Open file descriptor 3: ./test
        ==3729==    at 0x4F02840: __open_nocancel (syscall-template.S:82)
        ==3729==    by 0x400587: main (in /home/prasad/vyas/VYAS/tools/CPrograms/test)
        """

        m = re.match("==\d+== Open file descriptor (\d+):\s*(.*$)", line)
        if m:
            fd = int(m.group(1))
            if fd >= 4:
                """ fd 0 --> stdin
                    fd 1 --> stdout
                    fd 2 --> stderr
                    fd 3 --> log file
                """
                self.open_files.append(m.groups())

    def heap_summary(self, line):
        """ parse heap summary section line by line
            ==4468== HEAP SUMMARY:
            ==4468==     in use at exit: 144 bytes in 9 blocks
            ==4468==   total heap usage: 10 allocs, 1 frees, 160 bytes allocated
        """

        m = re.match("^==\d+==(?:\s+\w+){3}:\s+(\d+)\s+\w+,\s+(\d+)\s+\w+,\s+(\d+).*$", line)
        if m:
            self.no_allocs = int(m.group(1))
            self.no_free = int(m.group(2))
            self.allocated = int(m.group(3))

    def leak_summary(self, line):
        """ parse the leak summary section
            ==4468== LEAK SUMMARY:
            ==4468==    definitely lost: 16 bytes in 1 blocks
            ==4468==    indirectly lost: 128 bytes in 8 blocks
            ==4468==      possibly lost: 0 bytes in 0 blocks
            ==4468==    still reachable: 0 bytes in 0 blocks
            ==4468==         suppressed: 0 bytes in 0 blocks
        """
        m = re.match("^==\d+==\s+((?:\w+\s*){2}):\s+(\d+).*$", line)
        if m:
            g1 = m.group(1)
            if g1 == "definitely lost":
                self.definitely = int(m.group(2))
            elif g1 == "indirectly lost":
                self.indirectly = int(m.group(2))
            elif g1 == "possibly lost":
                self.possibly = int(m.group(2))

    def parse(self):
        """ parse the log file
        """
        sect_funcs = {
            "FILE DESCRIPTORS": self.file_descriptiors,
            "HEAP SUMMARY": self.heap_summary,
            "LEAK SUMMARY": self.leak_summary,
            "ERROR SUMMARY": None,
            "Parent PID": None
        }
        sections = list(sect_funcs.keys())

        fd = open(self.log_file)

        cur_sec = None
        sect_re = re.compile("==\d+==\s+(\w+\s+\w+)\s*:.*$")
        for l in fd.read().split("\n"):
            m = sect_re.match(l)
            if m:
                # section might have changed
                sec = m.group(1)
                if sec in sections:
                    cur_sec = sec

            if cur_sec and sect_funcs[cur_sec]:
                sect_funcs[cur_sec](l)
        fd.close()

class valgrind(object):

    VALGRIND_NAME = "valgrind"
    VALGRIND_PATH = None

    def __init__(self, executable):
        """
        """
        self.executable = executable
        self.errors     = []

        if not valgrind.VALGRIND_PATH:
            self.__valgrind_path__()
        pass

    def __valgrind_path__(self):
        """
        """
        p = utils.get_installed_path(valgrind.VALGRIND_NAME)
        if p:
            valgrind.VALGRIND_PATH = p
        else:
            log.log(3, VALGRIND_NAME + " is not installed.")

    def run_valgrind(self, args):
        """
        """
        return utils.run_command(self.VALGRIND_PATH + args)

    def add_error(self, error):
        """
        """
        self.errors.append(error)

    def analyse(self):
        """ analyse source code using valgrind
        """
        log_file = "/tmp/valgrind.log"

        lc  = "--leak-check=full"
        fds = "--track-fds=yes"
        lf  = "--log-file={lf}".format(lf=log_file)

        """ Arguments to valgrind --leak-check=summary --track-fds=yes
        --log-file=/tmp/valgrind.log CPrograms/link-list
        """
        args = " {lc} {tfd} {lf} {e} ".format(lc=lc, tfd=fds, lf=lf,
                            e=self.executable)

        log.log(3, "\nAnalysing cpp code using valgrind\n")
        self.run_valgrind(args)
        p = ValgrindLogParser(log_file)
        p.parse()
        log.log(3, str(p))
