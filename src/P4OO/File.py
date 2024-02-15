######################################################################
#  Copyright (c)2012, David L. Armstrong.
#
#  P4OO.File.py
#
######################################################################

'''
Perforce File Object

P4OO.File provides ... not much really
'''

from P4OO._Base import _P4OOBase
from P4OO._Set import _P4OOSet


class P4OOFile(_P4OOBase):
    ''' P4OOFile currently implements no custom logic of its own. '''

# TODO File are not Spec Objects, but...
#    # Subclasses must define SPECOBJ_TYPE
#    _SPECOBJ_TYPE = 'file'

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._getAttr('id'))


class P4OOFileSet(_P4OOSet):
    ''' P4OOFileSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'files'
