######################################################################
#  Copyright (c)2011-2012,2015,2024 David L. Armstrong.
#
#  P4OO.Branch.py
#
######################################################################

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

from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOBranch(_P4OOSpecObj):
    # P4OOBranch currently implements no custom logic of its own.

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'branch'


class P4OOBranchSet(_P4OOSet):
    # P4OOBranchSet currently implements no custom logic of its own.
    pass
