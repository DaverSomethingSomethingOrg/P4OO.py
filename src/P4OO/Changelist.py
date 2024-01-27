######################################################################
#  Copyright (c)2012, David L. Armstrong.
#
#  P4OO.Changelist.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
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

######################################################################
# P4Python Class Initialization
#
from P4OO.Change import P4OOChange, P4OOChangeSet
class P4OOChangelist(P4OOChange):
    ''' P4OOChangelist currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'change'    

class P4OOChangelistSet(P4OOChangeSet):
    ''' P4OOChangeSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'changes'    


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