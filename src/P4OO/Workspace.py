######################################################################
#  Copyright (c)2012, David L. Armstrong.
#
#  P4OO.Workspace.py
#
######################################################################

'''
Perforce Workspace Object

P4OO.Workspace provides ...
'''

from P4OO.Client import P4OOClient, P4OOClientSet


class P4OOWorkspace(P4OOClient):
    ''' P4OOWorkspace is just a pseudonym for P4OOClient. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'client'


class P4OOWorkspaceSet(P4OOClientSet):
    ''' P4OOWorkspaceSet is just a pseudonym for P4OOClientSet. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'clients'
