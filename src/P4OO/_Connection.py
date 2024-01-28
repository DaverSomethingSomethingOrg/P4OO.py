######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#
#  P4OO._Connection.py
#
######################################################################

#NAME / DESCRIPTION
'''
Abstract P4OO Connection interface

P4OO._Connection provides the translation from P4OO
data-object calls into P4 subcommands, and translation of p4
subcommand output back into P4OO data-objects.
'''

######################################################################
# Includes
#
from P4OO._Base import _P4OOBase

######################################################################
# P4Python Class Initialization
#
class _P4OOConnection(_P4OOBase):
    '''
    Empty class, just providing the inheritance path for now.
    '''