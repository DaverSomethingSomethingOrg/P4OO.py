######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO._Base.py
#
######################################################################

"""
Perforce _Base Class

 P4OO._Base provides consistent construction and attribute handling
methods for all P4OO objects.
"""

from P4 import P4
from dataclasses import dataclass, field
import logging


@dataclass(unsafe_hash=True)
class _P4OOBase:
#    _p4Conn: P4 = field(default=None, compare=False, repr=False)
#    p4PythonObj: P4 = field(default=None, compare=False, repr=False)
    _p4Conn: P4 = field(default=None, compare=False, repr=False)
    p4PythonObj: P4 = field(default=None, compare=False, repr=False)

    def _uniqueID(self):
        return id(self)

    def _initialize(self):
        return 1

    def _logError(self, *args):
        logging.error(args)

    def _logWarning(self, *args):
        logging.warning(args)

    def _logDebug(self, *args):
        logging.debug(args)

    def _runCommand(self, cmdName, **kwargs):
        p4Conn = self._getP4Connection()

        return p4Conn.runCommand(cmdName, **kwargs)

    def _getP4Connection(self):
        from P4OO._P4Python import _P4OOP4Python

#        print(self.p4PythonObj)
        if self._p4Conn is None:
#        my $p4SQLDbh = $self->_getAttr( 'p4SQLDbh' );

            if self.p4PythonObj is not None:
                self._p4Conn = _P4OOP4Python(**{"p4PythonObj": self.p4PythonObj})
#        elsif( defined( $p4SQLDbh ) )
#        {
#            require P4::OO::_Connection::P4toDB;
#            $p4Conn = P4::OO::_Connection::P4toDB->new('p4SQLDbh' => $self->_getAttr('p4SQLDbh'));
#        }
            else:
                self._p4Conn = _P4OOP4Python()

        return self._p4Conn
