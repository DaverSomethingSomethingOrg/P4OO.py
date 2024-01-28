######################################################################
#  Copyright (c)2024, David L. Armstrong
#  Copyright (c)2013, Cisco Systems, Inc.
#
#  P4OO.Counter.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Counter object

P4OO.Counter provides common behaviors for all P4OO Counter objects.

Unlike SpecObj objects, we do not cache the values from Perforce for
counters.  Since they are simply name/value pairs, assume the caller
will keep track of them as appropriate, and always query Perforce.

Counters are designed to change frequently, so when queried multiple
times it's likely a use case where the counter is expected to have
changed.

'''

######################################################################
# Includes
#
from P4OO._Base import _P4OOBase
from P4OO._Set import _P4OOSet


######################################################################
# SpecObj Class Initialization
#
class P4OOCounter(_P4OOBase):
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._getAttr('id'))


######################################################################
# Methods
#
    def getValue(self):
        p4ConnObj = self._getP4Connection()
        return p4ConnObj.readCounter(self._getAttr('id'))

    def setValue(self, newValue):
        p4ConnObj = self._getP4Connection()
        return p4ConnObj.setCounter(self._getAttr('id'), newValue)


class P4OOCounterSet(_P4OOSet):
    ''' P4OOCounterSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'counters'
