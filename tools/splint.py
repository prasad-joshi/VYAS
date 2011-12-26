#!/usr/bin/python

import re

import utils
import log
import ToolError
from Error import *

class splint(object):

    SPLINT_PATH = None
    SPLINT_NAME = "splint"

    def __init__(self, file_name):
        """ initialization
        """
        self.file_name = file_name      # source file to analyse
        self.errors    = []
        self.output    = "/tmp/splint_out"

        if not self.SPLINT_PATH:
            self.__splint_path__()
        pass

    def __splint_path__(self):
        """ find cppcheck path
        """
        p = utils.get_installed_path(self.SPLINT_NAME)
        if p:
            self.SPLINT_PATH = p
        else:
            log.log(3, self.SPLINT_NAME + " is not installed.")

    def run_splint(self, args):
        """ invoke splint on the source code
        """
        return utils.run_log_command(self.SPLINT_PATH + " " + args)

    def add_error(self, error):
        """ append an error in list of errors
        """
        self.errors.append(error)

    def parse(self):
        """ parse the output of splint.
        
        Format of splint output is:
            [<file>:<line> (in <context>)]
            <file>:<line>[,<column>]: message
             [hint]
              <file>:<line>,<column>: extra location information, if appropriate

        Typical output looks like this

            test.c: (in function main)
            test.c:6:11: Fresh storage f not released before return
              A memory leak has been detected. Storage allocated locally is
              not released before the last reference to it is lost. (Use
              -mustfreefresh to inhibit warning)
               test.c:5:23: Fresh storage f created
            test.c:5:8: Variable f declared but not used
              A variable is declared but never used. Use /*@unused@*/ in front
              of declaration to suppress message. (Use -varuse to inhibit
              warning)
        """
        # err_begin = re.compile("^([^\s]*):(\d+):(\d+):(.*)$")
        err_begin = re.compile("^([\w\.\/]+):(\d+):(\d+):(.*)$")
        context   = re.compile("^[\w\.\/]+:\s+\(in\s+function\s+\w+\s*\)$")
        for line in open(self.output):
            m = context.match(line)
            if m:
                # skipe the function context message
                continue

            m = err_begin.match(line)
            if m:
                f  = m.group(1)
                l  = m.group(2)
                c  = m.group(3)
                te  = m.group(4)
                id = 0          # splint does not give his own error id :(

                e = ToolError.splint_error(id, l, c, f, te)

                self.add_error(e)
            else:
                # we might want to store these extra messages displayed by
                # splint. Let's skip them for some time.
                continue
        return 0


    def analyse(self):
        """ analyse source code using splint
        """
        args = "{sf} >{of} 2>/dev/null".format(sf=self.file_name, of=self.output)

        log.log(3, "analysing cpp code using splint")
        r, o = self.run_splint(args)

        self.parse()

        for e in self.errors:
            print e
