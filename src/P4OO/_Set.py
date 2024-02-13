######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#
#  P4OO._Set.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce _Set object

P4OO._Set provides common behaviors for grouping of all P4OO Spec-based
objects.
'''

######################################################################
# Includes
#
from P4OO._Base import _P4OOBase
from P4OO._OrderedSet import OrderedSet

######################################################################
# P4OOSet Class Initialization
#
class _P4OOSet(_P4OOBase, OrderedSet):

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = None

# We want _P4OOBase-like attribute handling, but Orderedset repr and operators
    def __init__(self, iterable=None, **kwargs):
#        self._objAttrs = kwargs
        _P4OOBase.__init__(self, **kwargs)
        OrderedSet.__init__(self, iterable)

#TODO - document this
    def addObjects(self, objectsToAdd):
        oldCount = len(self)

        self |= objectsToAdd

        newCount = len(self)
        return newCount - oldCount


#TODO - document this
    def delObjects(self, objectList):
        oldCount = len(self)

        for item in objectList:
            self.discard(item)

        newCount = len(self)
        return newCount - oldCount

#TODO - document this
    def listObjectIDs(self):
        ''' Method to help convert a set of objects into a list of the
            names of the objects.
        '''

        return([item._uniqueID() for item in self])

    # query() is an instance method, but returns another, possibly unrelated object.
    # Where an instance is not already available, query can be called as follows:
    # p4Changes = P4OO.ChangeSet.ChangeSet().query({"files": changeFileRevRange, "maxresults": 1})
    # Instantiating a _Set object just for this purpose is cheap, but is not free.  So sorry.
    def query(self, **kwargs):
        p4ConnObj = self._getP4Connection()
        return p4ConnObj.runCommand(self._SETOBJ_TYPE, **kwargs)
