######################################################################
#  Copyright (c)2011-2012, David L. Armstrong.
#
#  P4OO._Connection.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
#
######################################################################

#NAME / DESCRIPTION
'''
Abstract P4OO Connection interface

P4OO._Connection provides the translation from P4OO
data-object calls into P4 subcommands, and translation of p4
subcommand output back into P4OO data-objects.
'''

######################################################################
# Includes
#
# P4OO._Base brings in our Exception hierarchy
#import P4OO._Base
# P4OO._Base is also our parent class
from P4OO._Base import _P4OOBase

######################################################################
# P4Python Class Initialization
#
class _P4OOConnection(_P4OOBase):
    '''
    Empty class, just providing the inheritance path for now.
    '''
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
