######################################################################
#  Copyright (c)2012, David L. Armstrong.
#
#  P4OO.File.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce File Object

P4OO.File provides ...
'''

######################################################################
# Includes
#
from P4OO._Base import _P4OOBase
from P4OO._Set import _P4OOSet

######################################################################
# P4Python Class Initialization
#
class P4OOFile(_P4OOBase):
    ''' P4OOFile currently implements no custom logic of its own. '''

#    # Subclasses must define SPECOBJ_TYPE
#    _SPECOBJ_TYPE = 'file'


class P4OOFileSet(_P4OOSet):
    ''' P4OOFileSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'files'
