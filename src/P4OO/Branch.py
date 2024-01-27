######################################################################
#  Copyright (c)2011-2012, 2015, David L. Armstrong.
#
#  P4OO.Branch.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Branch Object

P4OO.Branch provides standard P4OO._SpecObj behaviors

Spec Attributes:
      branch
      description
      owner
      options
      view
  datetime Attributes:
      update
      access

Query Options:
      user:
        type: [ string, P4OOUser ]
        multiplicity: 1
      owner: (interchangeable with user)
'''


######################################################################
# Includes
#

######################################################################
# P4Python Class Initialization
#
from P4OO._SpecObj import _P4OOSpecObj
class P4OOBranch(_P4OOSpecObj):
    # P4OOBranch currently implements no custom logic of its own.

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'branch'


from P4OO._Set import _P4OOSet
class P4OOBranchSet(_P4OOSet):
    # P4OOBranchSet currently implements no custom logic of its own.
    pass

######################################################################
# Standard authorship and copyright for documentation
#
# AUTHOR
#
#  David L. Armstrong <armstd@cpan.org>
#
# COPYRIGHT AND LICENSE
#
# Copyright (c)2011-2012, 2015, David L. Armstrong.
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
