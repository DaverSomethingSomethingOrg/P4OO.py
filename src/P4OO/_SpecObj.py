######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#  Copyright (c)2012-2013, Cisco Systems, Inc.
#
#  P4OO._SpecObj.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce _P4OOSpecObj object

P4OO._SpecObj provides common behaviors for all P4OO Spec-based
objects.
'''

######################################################################
# Includes
#
import json
import datetime
from P4OO._Base import _P4OOBase, _P4OOFatal


######################################################################
# JSON Encoder subclass for _toJSON to leverage
#
class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return super(DateTimeJSONEncoder, self).default(o)


######################################################################
# SpecObj Class Initialization
#
class _P4OOSpecObj(_P4OOBase):

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = None


######################################################################
# Methods
#
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._getSpecID())

    # _uniqueID overrides the _Base definition to use self._getSpecID instead
    def _uniqueID(self):
        return self._getSpecID()


    def _getSpecID(self):
        specID = self._getAttr('id')

        if specID is None:
            self.__initialize()
            specID = self._getAttr('id')

        # If specID is still undef, oh well.
        return specID


    def _getSpecAttr(self, attrName):
        self.__initialize()

        modifiedSpec = self._getAttr('modifiedSpec')

        # Allow the caller to use any case for the spec attribute
        lcAttrName = attrName.lower()

        if lcAttrName not in modifiedSpec:
            specType = self._SPECOBJ_TYPE
            raise _P4OOFatal("Invalid Spec attribute \"%s\" for type \"%s\"\n" % (lcAttrName, specType))

        return modifiedSpec[lcAttrName]


    def _setSpecAttr(self, attrName, value):
#        self.__initialize()

        modifiedSpec = self._getAttr('modifiedSpec')

        # Allow caller to create a new spec this way
        if modifiedSpec is None:
            modifiedSpec = self._setAttr('modifiedSpec', {})

        # Allow the caller to use any case for the spec attribute
        lcAttrName = attrName.lower()
        modifiedSpec[lcAttrName] = value
        return value


    def _delSpecAttr(self, attrName):
        self.__initialize()

        modifiedSpec = self._getAttr('modifiedSpec')

        # Allow the caller to use any case for the spec attribute
        lcAttrName = attrName.lower()

        value = None
        if lcAttrName in modifiedSpec:
            value = modifiedSpec[lcAttrName]
            modifiedSpec[lcAttrName] = None

        return value


    def saveSpec(self, force=False):
        p4ConnObj = self._getP4Connection()
        return p4ConnObj.saveSpec(self, force)

    def deleteSpec(self, force=False):
        p4ConnObj = self._getP4Connection()
        return p4ConnObj.deleteSpec(self, force)


    def _toJSON(self):
        self.__initialize()
        modifiedSpec = self._getAttr('modifiedSpec')

        return DateTimeJSONEncoder().encode(modifiedSpec)


######################################################################
# Internal (private) methods
#

    def __initialize(self):
        p4SpecObj = self._getAttr('p4SpecObj')

        if p4SpecObj is None:
            p4ConnObj = self._getP4Connection()
            p4SpecObj = p4ConnObj.readSpec(self) # We don't save this attribute because _P4Python does that for us

        return p4SpecObj
