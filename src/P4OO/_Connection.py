######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#
#  P4OO._Connection.py
#
######################################################################

from P4OO._Base import _P4OOBase

class _P4OOConnection(_P4OOBase):
    """
    Mostly Empty class, providing the inheritance path to _Base.
    """
    def __init__(self, **kwargs ):
        super().__init__(**kwargs)
        self._p4PythonSchema = None
