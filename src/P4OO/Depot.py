######################################################################
#  Copyright (c)2012, 2015, David L. Armstrong.
#
#  P4OO.Depot.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Depot Object

P4OO.Depot provides standard P4OO._SpecObj behaviors

Spec Attributes:
      depot
      description
      owner
      type
      address
      suffix
      map
  datetime Attributes:
      date

Query Options:
      <none>
'''

######################################################################
# Includes
#
# P4OO._Base brings in our Exception hierarchy
#import P4OO._Base

######################################################################
# P4Python Class Initialization
#
from P4OO._SpecObj import _P4OOSpecObj
class P4OODepot(_P4OOSpecObj):
    ''' P4OODepot currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'depot'    


from P4OO._Set import _P4OOSet
class P4OODepotSet(_P4OOSet):
    ''' P4OOChangeSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'depots'    


######################################################################
# Standard authorship and copyright for documentation
#
# AUTHOR
#
#  David L. Armstrong <armstd@cpan.org>
#
# COPYRIGHT AND LICENSE
#
# Copyright (c)2012, 2015, David L. Armstrong.
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
