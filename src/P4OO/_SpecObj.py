######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#  Copyright (c)2012-2013, Cisco Systems, Inc.
#
#  P4OO._SpecObj.py
#
######################################################################

"""
Perforce _P4OOSpecObj object

P4OO._SpecObj provides common behaviors for all P4OO Spec-based
objects.
"""

import json
import datetime
from dataclasses import dataclass, field
from P4OO._Base import _P4OOBase
from P4OO.Exceptions import P4OOFatal


class DateTimeJSONEncoder(json.JSONEncoder):
    """ JSON Encoder subclass for _toJSON to leverage """

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return super().default(o)

@dataclass(unsafe_hash=True)
class _P4OOSpecObj(_P4OOBase):

    id: str = field(default=None, compare=True)
    _modifiedSpec: dict = field(default=None, compare=False, repr=False)
    _p4SpecObj: dict = field(default=None, compare=False, repr=False)

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = None

    def _uniqueID(self):
        """ _uniqueID overrides the _Base definition to use
            self._getSpecID() instead
        """

        return self._getSpecID()

    def _getSpecID(self):

        specID = self.id

        if specID is None:
            self.__initialize()
            specID = self.id

        # If specID is still undef, oh well.
        return specID

    def _getSpecAttr(self, attrName):

        self.__initialize()

        modifiedSpec = self._modifiedSpec

        # Allow the caller to use any case for the spec attribute
        lcAttrName = attrName.lower()

        if lcAttrName not in modifiedSpec:
            specType = self._SPECOBJ_TYPE
            raise P4OOFatal("Invalid Spec attribute \"%s\" for type \"%s\"\n"
                            % (lcAttrName, specType))

        return modifiedSpec[lcAttrName]

    def _setSpecAttr(self, attrName, value):
#        self.__initialize()

        # Allow caller to create a new spec this way
        if self._modifiedSpec is None:
            self._modifiedSpec = {}

        modifiedSpec = self._modifiedSpec

        # Allow the caller to use any case for the spec attribute
        lcAttrName = attrName.lower()
        modifiedSpec[lcAttrName] = value
        return value

    def _delSpecAttr(self, attrName):
        self.__initialize()

        modifiedSpec = self._modifiedSpec

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

        return DateTimeJSONEncoder().encode(self._modifiedSpec)

    ######################################################################
    # Internal (private) methods
    #
    def __initialize(self):

        if self._p4SpecObj is None:
            p4ConnObj = self._getP4Connection()

            self._p4SpecObj = p4ConnObj.readSpec(self)

        return self._p4SpecObj
