######################################################################
#  Copyright (c)2012,2015,2024 David L. Armstrong.
#
#  P4OO.User.py
#
######################################################################

'''
Perforce User Object

P4OO.User provides standard P4OO._SpecObj behaviors

Spec Attributes:
      user
      fullname
      email
      jobview
      password
      reviews

datetime Attributes:
      update
      access


Query Options:
      maxresults:
        type: [ string ]
        multiplicity: 1
      allusers:
        multiplicity: 0
      longoutput:
        multiplicity: 0
      users:
        type: [ string, User, UserSet ]
'''

from P4OO.Client import P4OOClientSet
from P4OO.Change import P4OOChangeSet
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOUser(_P4OOSpecObj):
    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'user'

    def listOpenedFiles(self, client=None):
        ''' Return a P4OOFileSet of files opened by this user in the
            specified client workspace.
        '''

        return self._runCommand('opened', user=self, client=client)

    def listClients(self):
        return P4OOClientSet(_p4Conn=self._getP4Connection()).query(user=self)

    def listChanges(self, status=None, maxresults=None):
        changeSet = P4OOChangeSet(_p4Conn=self._getP4Connection())
        return changeSet.query(user=self, status=status, maxresults=maxresults)

    def deleteWithVengeance(self):
        # First reopen/revert files in all clients to be sure we can
        # remove any changes
        clients = self.listClients()
        for client in clients:
            client.revertOpenedFiles()

        # Next remove all Pending changes now that the files have been
        # reopened
        changes = self.listChanges(status="pending")
        for change in changes:
            change.deleteWithVengeance()

        # Next remove all of user's clients to cleanup db.have table
        # where possible.
        for client in clients:
            client.deleteWithVengeance()

        # Finally, remove the user spec
        self.deleteSpec(force=True)

        return True


class P4OOUserSet(_P4OOSet):
    ''' P4OOUserSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'users'
