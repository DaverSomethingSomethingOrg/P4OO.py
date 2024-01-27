######################################################################
#  Copyright (c)2011-2012, David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO._Base.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
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

######################################################################
# P4Python Class Initialization

class _P4OOBase(object):
    def __init__(self, **kwargs ):
        self._objAttrs = kwargs

    def _uniqueID(self):
        return id(self)

    def _initialize(self):
        return 1

    def _getAttr(self, name):
        if name not in self._objAttrs:
            return
        return self._objAttrs[name]

    def _setAttr(self, name, value):
        self._objAttrs[name] = value
#        print("Setting: ", self, " name: ", name, " value: ", value)
        return value

    def _delAttr(self, name):
        if name not in self._objAttrs:
            return
        else:
            value = self._objAttrs[name]
            del(self._objAttrs[name])
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

            from P4OO._P4Python import _P4OOP4Python
            if p4PythonObj is not None:
                p4Conn = _P4OOP4Python(**{"p4PythonObj": p4PythonObj})
#        elsif( defined( $p4SQLDbh ) )
#        {
#            require P4::OO::_Connection::P4toDB;
#            $p4Conn = P4::OO::_Connection::P4toDB->new( 'p4SQLDbh' => $self->_getAttr( 'p4SQLDbh' ) );
#        }
            else:
                p4Conn = _P4OOP4Python()

            self._setAttr('_p4Conn', p4Conn)

        return p4Conn


class _P4OOError(Exception):
    '''
    Base class for all P4OO Exceptions
    '''
    pass

class _P4OOFatal(_P4OOError):
    '''Generic Error - Fatal'''
    pass

class _P4OOWarning(_P4OOError):
    '''Generic Error - nonFatal'''
    pass

class _P4OOBadSubClass(_P4OOFatal):
    '''Subclass does not comform to interface spec or cannot be found'''
    pass

class _P4Error(_P4OOError):
    pass

class _P4Fatal(_P4OOFatal):
    '''Generic Internal Error'''
    pass

class _P4Warning(_P4OOWarning):
    '''Generic Internal Warning'''
    pass


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
# Copyright (c)2012, Cisco Systems, Inc.
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
