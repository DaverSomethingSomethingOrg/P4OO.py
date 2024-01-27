######################################################################
#  Copyright (c)2012, 2015, David L. Armstrong.
#
#  P4OO.User.py
#
#  See COPYRIGHT AND LICENSE section below for usage
#   and distribution rights.
#
######################################################################

#NAME / DESCRIPTION
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
      max:
        type: [ string ]
        multiplicity: 1
      allusers:
        multiplicity: 0
      longoutput:
        multiplicity: 0
      users:
        type: [ string, User, UserSet ]
'''

######################################################################
# Includes
#
from P4OO._Base import _P4Warning, _P4Fatal, _P4OOFatal
from P4OO.Client import P4OOClientSet
from P4OO.Change import P4OOChangeSet

######################################################################
# P4Python Class Initialization
#
from P4OO._SpecObj import _P4OOSpecObj
class P4OOUser(_P4OOSpecObj):
    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'user'

    def listOpenedFiles(self, client=None):
        ''' Return a P4OOFileSet of files opened by this user.'''
        return(self._runCommand('opened', user=self, client=client))

    def listClients(self):
        return self.query(P4OOClientSet, user=self)

    def listChanges(self, status=None, max=None):
        return self.query(P4OOChangeSet, user=self, status=status, max=max)

    def deleteWithVengeance(self):
        # First reopen/revert files in all clients to be sure we can remove any changes
        clients = self.listClients()
        for client in clients:
            client.revertOpenedFiles()

        # Next remove all Pending changes now that the files have been reopened
        changes = self.listChanges(status="pending")
        for change in changes:
            change.deleteWithVengeance()

        # Next remove all of user's clients to cleanup db.have table where possible.
        for client in clients:
            client.deleteWithVengeance()

        # Finally, remove the user spec
        self.deleteSpec(force=True)

        return True


from P4OO._Set import _P4OOSet
class P4OOUserSet(_P4OOSet):
    ''' P4OOUserSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'users'


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
