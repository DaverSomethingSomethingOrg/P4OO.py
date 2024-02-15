######################################################################
#  Copyright (c)2012,2015,2024 David L. Armstrong.
#
#  P4OO.Depot.py
#
######################################################################

'''
Perforce Depot Object

P4OO.Depot provides standard P4OO._SpecObj behaviors

Spec Attributes:
      depot
      description
      owner
      type
      address
      suffix
      map
  datetime Attributes:
      date

Query Options:
      <none>
'''

from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OODepot(_P4OOSpecObj):
    ''' P4OODepot currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'depot'


class P4OODepotSet(_P4OOSet):
    ''' P4OOChangeSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'depots'
