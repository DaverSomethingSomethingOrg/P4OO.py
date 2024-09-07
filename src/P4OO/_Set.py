######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#
#  P4OO._Set.py
#
######################################################################

"""
    _P4OOSet objects are primarily used for querying.  We want to
    encourage use cases that take advantage of set operations operating
    on multiple objects at once, rather than iterating through individual
    objects.
"""

from dataclasses import dataclass, field, InitVar
from P4OO._Base import _P4OOBase
from P4OO._OrderedSet import OrderedSet

#@dataclass(repr=False, eq=False, order=False)
@dataclass(repr=False, eq=False, order=False, init=False)
class _P4OOSet(OrderedSet, _P4OOBase):
    """ _P4OOSet provides common behaviors for grouping of all P4OO Spec-based
        objects.

    """
#    iterable: list = field(default_factory=list, compare=False)
    iterable: InitVar[list] = field(default=None)

#    def __init__(self, iterable=None, **kwargs):
#        _P4OOBase.__init__(self)
#        OrderedSet.__init__(self, iterable)

    def __post_init__(self, iterable):
        """ We want _P4OOBase-like attribute handling, but Orderedset
            repr and operators
        """
#        _P4OOBase.__init__(self)
        OrderedSet.__init__(self, iterable)

# TODO - document this
    def addObjects(self, objectsToAdd):

        oldCount = len(self)

        self |= objectsToAdd

        newCount = len(self)
        return newCount - oldCount

# TODO - document this
    def delObjects(self, objectList):
        oldCount = len(self)

        for item in objectList:
            self.discard(item)

        newCount = len(self)
        return newCount - oldCount

# TODO - document this
    def listObjectIDs(self):
        """ Method to help convert a set of objects into a list of the
            names of the objects.
        """

        return [item._uniqueID() for item in self]

    def _query(self, setObjType=None, **kwargs):
        """ _query() is an instance method, but returns another, possibly
            unrelated object.

            Where an instance is not already available, query can be
            called as follows:

            p4Changes = P4OO.ChangeSet.ChangeSet().query(
                         {"files": changeFileRevRange, "maxresults": 1})

            Instantiating a _Set object just for this purpose is cheap,
            but is not free.  So sorry.
        """

        p4ConnObj = self._getP4Connection()
        return p4ConnObj.runCommand(setObjType, **kwargs)
