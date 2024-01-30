######################################################################
#  Copyright (c)2024 David L. Armstrong.
#
#  P4OO._Exceptions.py
#
######################################################################

#NAME / DESCRIPTION
'''
P4OO Error Classes to help distinguish Warning/Error/Fatal issues

'''

######################################################################
# Includes
#


class _P4OOError(Exception):
    '''
    Base class for all P4OO Exceptions
    '''

class _P4OOFatal(_P4OOError):
    '''Generic Error - Fatal'''

class _P4OOWarning(_P4OOError):
    '''Generic Error - nonFatal'''

class _P4OOBadSubClass(_P4OOFatal):
    '''Subclass does not comform to interface spec or cannot be found'''

class _P4Error(_P4OOError):
    '''Generic Internal Error'''

class _P4Fatal(_P4OOFatal):
    '''Generic Internal Error'''

class _P4Warning(_P4OOWarning):
    '''Generic Internal Warning'''
