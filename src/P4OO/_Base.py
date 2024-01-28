######################################################################
#  Copyright (c)2011-2012,2024 David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO._Base.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce _Base Class

 P4OO._Base provides consistent construction and attribute handling
methods for all P4OO objects.
'''

######################################################################
# Includes
#
import logging
from P4OO._P4Python import _P4OOP4Python

######################################################################
# P4Python Class Initialization

class _P4OOBase():
    def __init__(self, **kwargs ):
        self._objAttrs = kwargs

    def _uniqueID(self):
        return id(self)

    def _initialize(self):
        return 1

    def _getAttr(self, name):
        if name not in self._objAttrs:
            return None
        return self._objAttrs[name]

    def _setAttr(self, name, value):
        self._objAttrs[name] = value
#        print("Setting: ", self, " name: ", name, " value: ", value)
        return value

    def _delAttr(self, name):
        if name not in self._objAttrs:
            return None

        value = self._objAttrs[name]
        del self._objAttrs[name]
        return value

    def _logError(self, *args):
        logging.error(args)

    def _logWarning(self, *args):
        logging.warning(args)

    def _logDebug(self, *args):
        logging.debug(args)


    def _runCommand(self, cmdName, **kwargs):
        p4Conn = self._getP4Connection()

        return p4Conn.runCommand(cmdName, **kwargs)


    def query(self, setClass, **kwargs ):
        p4ConnObj = self._getP4Connection()

        # Inject our connection, but let the class's object method do the work for us.
        return setClass(**{'_p4Conn': p4ConnObj}).query(**kwargs)


    def _getP4Connection(self):
        p4Conn = self._getAttr('_p4Conn')

        if p4Conn is None:
            p4PythonObj = self._getAttr('p4PythonObj')
#        my $p4SQLDbh = $self->_getAttr( 'p4SQLDbh' );

            if p4PythonObj is not None:
                p4Conn = _P4OOP4Python(**{"p4PythonObj": p4PythonObj})
#        elsif( defined( $p4SQLDbh ) )
#        {
#            require P4::OO::_Connection::P4toDB;
#            $p4Conn = P4::OO::_Connection::P4toDB->new('p4SQLDbh' => $self->_getAttr('p4SQLDbh'));
#        }
            else:
                p4Conn = _P4OOP4Python()

            self._setAttr('_p4Conn', p4Conn)

        return p4Conn


class _P4OOError(Exception):
    '''
    Base class for all P4OO Exceptions
    '''

class _P4OOFatal(_P4OOError):
    '''Generic Error - Fatal'''

class _P4OOWarning(_P4OOError):
    '''Generic Error - nonFatal'''

class _P4OOBadSubClass(_P4OOFatal):
    '''Subclass does not comform to interface spec or cannot be found'''

class _P4Error(_P4OOError):
    '''Generic Internal Error'''

class _P4Fatal(_P4OOFatal):
    '''Generic Internal Error'''

class _P4Warning(_P4OOWarning):
    '''Generic Internal Warning'''
