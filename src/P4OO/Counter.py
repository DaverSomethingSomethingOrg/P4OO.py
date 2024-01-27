######################################################################
#  Copyright (c)2013, Cisco Systems, Inc.
#
#  P4OO.Counter.py
#
#  See COPYRIGHT AND LICENSE section in pod text below for usage
#   and distribution rights.
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
from P4OO._Base import _P4OOBase, _P4OOFatal


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


from P4OO._Set import _P4OOSet
class P4OOCounterSet(_P4OOSet):
    ''' P4OOCounterSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'counters'


######################################################################
# Internal (private) methods
#


######################################################################
# Standard authorship and copyright for documentation
#
# AUTHOR
#
#  David L. Armstrong <armstd@cpan.org>
#
# COPYRIGHT AND LICENSE
#
# Copyright (c)2013, Cisco Systems, Inc.
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
