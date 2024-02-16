######################################################################
#  Copyright (c)2024 David L. Armstrong.
#
#  P4OO._Exceptions.py
#
######################################################################

'''
P4OO Error Classes to help distinguish Warning/Error/Fatal issues

'''


class P4OOError(Exception):
    '''
    Base class for all P4OO Exceptions
    '''


class P4OOFatal(P4OOError):
    '''Generic Error - Fatal'''


class P4OOWarning(P4OOError):
    '''Generic Error - nonFatal'''


class P4OOBadSubClass(P4OOFatal):
    '''Subclass does not comform to interface spec or cannot be found'''


class P4Error(P4OOError):
    '''Generic Internal Error'''


class P4Fatal(P4OOFatal):
    '''Generic Internal Error - P4Python did something we didn't expect.'''


class P4Warning(P4OOWarning):
    '''Generic Internal Warning - P4Python did something we didn't expect.'''
