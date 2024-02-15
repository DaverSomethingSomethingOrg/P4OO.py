######################################################################
#  Copyright (c)2012,2015,2024 David L. Armstrong.
#
#  P4OO.Job.py
#
######################################################################

'''
Perforce Job Object

P4OO.Job provides standard P4OO._SpecObj behaviors

Spec Attributes:
      job
      description
      user
      status
  datetime Attributes:
      date

Query Options:
      jobview:
        type: [ string ]
        multiplicity: 1
      files:
        type: [ string, P4OOFile, P4OOFileSet ]
'''

from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOJob(_P4OOSpecObj):
    ''' P4OOJob currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'job'


class P4OOJobSet(_P4OOSet):
    ''' P4OOJobSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'jobs'
