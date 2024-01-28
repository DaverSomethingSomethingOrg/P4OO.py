######################################################################
#  Copyright (c)2012, David L. Armstrong.
#
#  P4OO.Workspace.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Workspace Object

P4OO.Workspace provides ...
'''

######################################################################
# Includes
#

######################################################################
# P4Python Class Initialization
#
from P4OO.Client import P4OOClient, P4OOClientSet
class P4OOWorkspace(P4OOClient):
    ''' P4OOWorkspace currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'client'

class P4OOWorkspaceSet(P4OOClientSet):
    ''' P4OOWorkspaceSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'clients'
