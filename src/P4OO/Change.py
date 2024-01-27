######################################################################
#  Copyright (c)2011-2012, 2015, David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO.Change.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Change Object

P4OO.Change provides standard P4OO._SpecObj behaviors

Spec Attributes:
      change
      description
      client
      user
      status
      type
      jobs
      files
  datetime Attributes:
      date

Query Options:
      user:
        type: [ string, P4OOUser ]
        multiplicity: 1
      owner: (interchangeable with user)
      client:
        type: [ string, P4OOClient ]
        multiplicity: 1
      status:
        type: [ string ]
        multiplicity: 1
      max:
        type: [ integer ]
        multiplicity: 1
      longoutput:
        multiplicity: 0
      files:
        type: [ string, P4OOFile, P4OOFileSet ]
'''


######################################################################
# Includes
#
from P4OO._Base import _P4Warning, _P4Fatal, _P4OOFatal

######################################################################
# P4Python Class Initialization
#
from P4OO._SpecObj import _P4OOSpecObj
class P4OOChange(_P4OOSpecObj):
    ''' P4OOChange currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'change'

    ######################################################################
    # getChangesFromChangeNums()
    #  - Fetch the list of changes from this change to another one.
    #
    # ASSUMPTIONS:
    # - self represents the lower of the two changes.  If the other
    #   direction is desired, then make the call against the other
    #   change instead.
    #
    def getChangesFromChangeNums(self, otherChange, client):
        ''' Fetch the list of changes from this change to another one. '''

        if not isinstance(otherChange, P4OOChange):
            raise TypeError(otherChange)

        firstChange = int(self._getSpecID()) + 1 # +1 to not include the from change
        lastChange = int(otherChange._getSpecID())

        aggregatedChanges = P4OOChangeSet()
        view = client._getSpecAttr('View')
        for viewLine in view:
            viewSpec = viewLine.split(" ",2)

            fileChangeRange = '%s@%d,%d' % (viewSpec[0], firstChange, lastChange)
            viewChanges = self.query(P4OOChangeSet, files=fileChangeRange, longOutput=1)
            aggregatedChanges |= viewChanges

        return(aggregatedChanges)


#    def reopenFiles(self):
#        return self._runCommand('reopen', change=self, files="//%s/..." % self._getSpecAttr('client'), p4client=self._getSpecAttr('client'))

    def revertOpenedFiles(self):
#        self.reopenFiles()
        return self._runCommand('revert', change=self, noclientrefresh=True, files="//%s/..." % self._getSpecAttr('client'), p4client=self._getSpecAttr('client'))
#        try:
#            return self._runCommand('revert', change=self, noclientrefresh=True, files="//%s/..." % self._getSpecAttr('client'), p4client=self._getSpecAttr('client'))
#        except _P4Fatal:

    def deleteShelf(self):
        try:
            return self._runCommand('shelve', delete=True, change=self, force=True, p4client=self._getSpecAttr('client'))
        except _P4Fatal:
            return True

    def deleteWithVengeance(self):
#        self.revertOpenedFiles()
        self.deleteShelf()
        self.deleteSpec(force=True)

        return True


from P4OO._Set import _P4OOSet
class P4OOChangeSet(_P4OOSet):
    ''' P4OOChangeSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'changes'


######################################################################
# Standard authorship and copyright for documentation
#
# AUTHOR
#
#  David L. Armstrong <armstd@cpan.org>
#
# COPYRIGHT AND LICENSE
#
# Copyright (c)2011-2012, 2015, David L. Armstrong.
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
