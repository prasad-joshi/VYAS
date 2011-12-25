#!/usr/bin/python

class Error(object):
    def __init__(self, eid, line, column, file_name, tool_error):
        self.EID        = eid           # error ID in database
        self.line       = line          # error line number
        self.column     = column        # column number
        self.file_name  = file_name     # source file name
        self.tool_error = tool_error    # error as displayed by tool

    def __str__(self):
        s  = "{fn} ({l}:{c}): {te}"
        l  = self.get_line_number()
        c  = self.get_column()
        te = self.get_error()
        fn = self.get_file_name()

        return s.format(fn=fn, l=l, c=c, te=te)

    def __repr__(self):
        return str(self)

    def get_line_number(self):
        """ return line number
        """
        return self.line

    def get_column(self):
        """ return column number
        """
        return self.column

    def get_file_name(self):
        """ return file name
        """
        return self.file_name

    def get_tool_error(self):
        """ return error string returned by tool
        """
        return self.tool_error

    def get_error(self):
        """ error to be displayed by web GUI.
        """
        # at the moment we do not have mapping from error displayed by tool to
        # the error we would like to display on Web GUI. Return tool_error
        return self.get_tool_error()
