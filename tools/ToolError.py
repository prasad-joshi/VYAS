#!/usr/bin/python

from Error import *

def get_EID(tool, tool_id, tool_error):
    """ return EID from database
    """
    pass

def cppcheck_error(id, line, column, file_name, tool_error):
    eid = get_EID("cppcheck", id, tool_error)
    return Error(eid, line, column, file_name, tool_error)

def splint_error(id, line, column, file_name, tool_error):
    eid = get_EID("splint", id, tool_error)
    return Error(eid, line, column, file_name, tool_error)
