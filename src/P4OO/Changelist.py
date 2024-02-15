######################################################################
#  Copyright (c)2012,2024 David L. Armstrong.
#
#  P4OO.Changelist.py
#
######################################################################

'''
Perforce Changelist Object

P4OO.Changelist provides ...
'''

from P4OO.Change import P4OOChange, P4OOChangeSet


class P4OOChangelist(P4OOChange):
    ''' P4OOChangelist is just a pseudonym for P4OOChange. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'change'


class P4OOChangelistSet(P4OOChangeSet):
    ''' P4OOChangelistSet is just a pseudonym for P4OOChangeSet. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'changes'
