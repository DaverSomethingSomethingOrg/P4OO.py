######################################################################
#  Copyright (c)2012, 2015, 2024 David L. Armstrong.
#
#  P4OO.Group.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Group Object

P4OO.Group provides standard P4OO._SpecObj behaviors

Spec Attributes:
      group
      owners
      users
      maxresults
      maxscanrows
      maxlocktime
      timeout
      subgroups

Query Options:
      user:
        type: [ string, P4OOUser ]
        multiplicity: 1
'''

######################################################################
# Includes
#
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet

######################################################################
# P4Python Class Initialization
#
class P4OOGroup(_P4OOSpecObj):
    ''' P4OOGroup currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'group'


class P4OOGroupSet(_P4OOSet):
    ''' P4OOGroupSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'groups'
