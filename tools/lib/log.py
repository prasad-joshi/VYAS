#!/usr/bin/python

import sys

def log(level=3, message="", file=sys.stdout):
    """ logger
    """
    print >>file, message
