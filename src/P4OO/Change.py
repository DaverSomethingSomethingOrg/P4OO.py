######################################################################
#  Copyright (c)2011-2012, 2015, 2024 David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO.Change.py
#
######################################################################

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
      maxresults:
        type: [ integer ]
        multiplicity: 1
      longoutput:
        multiplicity: 0
      files:
        type: [ string, P4OOFile, P4OOFileSet ]
'''


from P4OO.Exceptions import P4Fatal
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOChange(_P4OOSpecObj):
    ''' P4OOChange currently implements no custom logic of its own. '''

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'change'

    def getChangesFromChangeNums(self, otherChange, client):
        ''' Fetch the list of changes from this change to another one.

            ASSUMPTIONS:
            - self represents the lower of the two changes.  If the other
              direction is desired, then make the call against the other
              change instead.
        '''

        if not isinstance(otherChange, P4OOChange):
            raise TypeError(otherChange)

        # +1 to not include the from change
        firstChange = int(self._getSpecID()) + 1
        lastChange = int(otherChange._getSpecID())

        aggregatedChanges = P4OOChangeSet()
        view = client._getSpecAttr('View')
        for viewLine in view:
            viewSpec = viewLine.split(" ", 2)

            fileChangeRange = '%s@%d,%d' % (viewSpec[0], firstChange,
                                            lastChange)
            viewChanges = self.query(P4OOChangeSet, files=fileChangeRange,
                                     longOutput=1)
            aggregatedChanges |= viewChanges

        return aggregatedChanges

#    def reopenFiles(self):
#        return self._runCommand('reopen',
#                                change=self,
#                                files="//%s/..." %
#                                self._getSpecAttr('client'),
#                                p4client=self._getSpecAttr('client')
#                               )

    def revertOpenedFiles(self):
#        self.reopenFiles()
        return self._runCommand('revert',
                                change=self,
                                noclientrefresh=True,
                                files="//%s/..." % self._getSpecAttr('client'),
                                p4client=self._getSpecAttr('client'))
#        try:
#            return self._runCommand('revert',
#                                    change=self,
#                                    noclientrefresh=True,
#                                    files="//%s/..." %
#                                    self._getSpecAttr('client'),
#                                    p4client=self._getSpecAttr('client')
#                                   )
#        except P4Fatal:

    def deleteShelf(self):
        try:
            return self._runCommand('shelve',
                                    delete=True,
                                    change=self,
                                    force=True,
                                    p4client=self._getSpecAttr('client'))
        except P4Fatal:
            return True

    def deleteWithVengeance(self):
#        self.revertOpenedFiles()
        self.deleteShelf()
        self.deleteSpec(force=True)

        return True


class P4OOChangeSet(_P4OOSet):
    ''' P4OOChangeSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'changes'
