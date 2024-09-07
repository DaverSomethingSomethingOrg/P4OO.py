######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#
#  P4OO._Connection.py
#
######################################################################

from dataclasses import dataclass, field
from P4OO._Base import _P4OOBase

@dataclass
class _P4OOConnection(_P4OOBase):
    """
    Mostly Empty class, providing the inheritance path to _Base.
    """
    def __post_init__(self):
        self._p4PythonSchema = None
