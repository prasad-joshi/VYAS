#!/usr/bin/python

import log
import utils
import ToolError
from Error import *

from xml.etree.ElementTree import parse

class ValgrindXMLParser(object):
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.errors = []

    def parse(self):
        """
        """

        tree = parse(self.xml_file)
        for e in tree.findall("error"):
            id = e.findtext("kind")
            for xw in e.findall("xwhat"):
                bytes = xw.findtext("leakedbytes")
                msg = "leakedbytes " + bytes
                error = {}
                error["id"]  = id
                error["msg"] = msg
                self.errors.append(error)

        return self.errors

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
        return utils.run_log_command(self.VALGRIND_PATH + args)

    def add_error(self, error):
        """
        """
        self.errors.append(error)

    def analyse(self):
        """ analyse source code using valgrind
        """
        xml_file = "/tmp/valgrind.xml"
        log_file = "/tmp/valgrind.log"

        lc  = "--leak-check=full"
        xml = "--xml=yes"
        fds = "--track-fds=yes"
        lf  = "--log-file={lf}".format(lf=log_file)
        xf  = "--xml-file={xf}".format(xf=xml_file)

        """ Arguments to valgrind --leak-check=full
            --log-file=/tmp/valgrind.log  --xml=yes
            --xml-file=/tmp/valgrind.xml --track-fds=yes
        """
        args = " {lc} {x} {f} {lf} {xf} {e} ".format(lc=lc, x=xml, f=fds,
                            lf=lf, xf=xf, e=self.executable)

        print "analysing cpp code using valgrind", args
        self.run_valgrind(args)

        errors = ValgrindXMLParser(xml_file).parse()
        for e in errors:
            id = e["id"]
            msg = e["msg"]

            error = ToolError.valgrind_error(id, self.executable, msg)
            self.add_error(error)

        for e in self.errors:
            print e
