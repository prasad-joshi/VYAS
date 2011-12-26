#!/usr/bin/python

import sys
import commands
import log

WHICH = "/usr/bin/which"

def run_command(cmd):
    """ execute a command
    """
    return commands.getstatusoutput(cmd)

def run_log_command(cmd, file=sys.stdout):
    """ execute and log the command
    """
    r, o = run_command(cmd)
    log.log(3, cmd, file)
    log.log(3, "Output " + o, file)
    return r, o

def _is_installed(tool):
    """
    """
    cmd = "{which} {tool}"
    return run_command(cmd.format(which=WHICH, tool=tool))

def is_installed(tool):
    """ check if given utility is installd
    """
    r, o = _is_installed(tool)
    if r != 0:
        return 0
    return 1

def get_installed_path(tool):
    """ returns path of tool's executable
    """
    r, o = _is_installed(tool)
    if r != 0:
        return None
    return o
