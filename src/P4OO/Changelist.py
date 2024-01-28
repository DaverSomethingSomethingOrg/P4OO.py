######################################################################
#  Copyright (c)2012,2024 David L. Armstrong.
#
#  P4OO.Changelist.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Changelist Object

P4OO.Changelist provides ...
'''

######################################################################
# Includes
#
from P4OO.Change import P4OOChange, P4OOChangeSet

######################################################################
# P4Python Class Initialization
#
class P4OOChangelist(P4OOChange):
    ''' P4OOChangelist currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'change'

class P4OOChangelistSet(P4OOChangeSet):
    ''' P4OOChangeSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'changes'
