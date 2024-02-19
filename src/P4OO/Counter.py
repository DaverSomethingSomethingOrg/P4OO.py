######################################################################
#  Copyright (c)2024, David L. Armstrong
#  Copyright (c)2013, Cisco Systems, Inc.
#
#  P4OO.Counter.py
#
######################################################################

"""
Perforce Counter objects

P4OO.Counter provides common behaviors for all P4OO Counter objects.

Unlike SpecObj objects, we do not cache the values from Perforce for
counters.  Since they are simply name/value pairs, assume the caller
will keep track of them as appropriate, and always query Perforce.

Counters are designed to change frequently, so when queried multiple
times it's likely a use case where the counter is expected to have
changed.
"""

from P4OO._Base import _P4OOBase
from P4OO._Set import _P4OOSet


class P4OOCounter(_P4OOBase):
    """
    Perforce Counter Object

    id Required: Yes

    Forcible: No

    Attributes:
        counter (str): Name of the Counter

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_counter.html
    """
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._getAttr('id'))

    def getValue(self):
        """
        Retrieve the current value of the counter

        Args:
            None

        Returns:
            (int): Current value of the counter
        """

        p4ConnObj = self._getP4Connection()
        return p4ConnObj.readCounter(self._getAttr('id'))

    def setValue(self, newValue):
        """
        Set the new value of the counter

        Args:
            newValue (int): New value for the counter

        Returns:
            (int): New current value for the counter
        """

        p4ConnObj = self._getP4Connection()
        return p4ConnObj.setCounter(self._getAttr('id'), newValue)


class P4OOCounterSet(_P4OOSet):
    """ `P4OOSet` of `P4OOCounter` objects """

    def query(self, maxresults: int=None, namefilter: str=None, **kwargs):
        """
        Executes 'p4 counters' query

        Args:
            maxresults (int, optional): Return only the first <max> results
            namefilter (str, optional): Case-sensitive filter on counter name

        Returns:
            (P4OOCounterSet): `P4OOSet` of `P4OOCounter` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_counters.html
        """
        return self._query(setObjType='counters', maxresults=maxresults,
                           namefilter=namefilter, **kwargs)
