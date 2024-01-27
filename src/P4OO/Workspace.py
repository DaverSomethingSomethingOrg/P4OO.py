######################################################################
#  Copyright (c)2012, David L. Armstrong.
#
#  P4OO.Workspace.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
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


######################################################################
# Standard authorship and copyright for documentation
#
# AUTHOR
#
#  David L. Armstrong <armstd@cpan.org>
#
# COPYRIGHT AND LICENSE
#
# Copyright (c)2012, David L. Armstrong.
#
#   This module is distributed under the terms of the Artistic License
# 2.0.  For more details, see the full text of the license in the file
# LICENSE.
#
# SUPPORT AND WARRANTY
#
#   This program is distributed in the hope that it will be
# useful, but it is provided "as is" and without any expressed
# or implied warranties.
#