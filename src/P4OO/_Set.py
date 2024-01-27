######################################################################
#  Copyright (c)2011-2012, David L. Armstrong.
#
#  P4OO._Set.py
#
#  See COPYRIGHT AND LICENSE section in pod text below for usage
#   and distribution rights.
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
# P4OO._Base brings in our Exception hierarchy
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
        return(newCount - oldCount)


#TODO - document this
    def delObjects(self, objectList):
        oldCount = len(self)

        for item in objectList:
            self.discard(item)

        newCount = len(self)
        return(newCount - oldCount)

#TODO - document this
    def listObjectIDs(self):
        return([foo._uniqueID() for foo in self])

    # query() is an instance method, but returns another, possibly unrelated object.
    # Where an instance is not already available, query can be called as follows:
    # p4Changes = P4OO.ChangeSet.ChangeSet().query({"files": changeFileRevRange, "max": 1})
    # Instantiating a _Set object just for this purpose is cheap, but is not free.  So sorry.
    def query(self, **kwargs ):
        p4ConnObj = self._getP4Connection()
        return( p4ConnObj.runCommand(self._SETOBJ_TYPE, **kwargs) )


######################################################################
# Standard authorship and copyright for documentation
#
# AUTHOR
#
#  David L. Armstrong <armstd@cpan.org>
#
# COPYRIGHT AND LICENSE
#
# Copyright (c)2011-2012, David L. Armstrong.
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
