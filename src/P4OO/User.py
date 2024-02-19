######################################################################
#  Copyright (c)2012,2015,2024 David L. Armstrong.
#
#  P4OO.User.py
#
######################################################################


from P4OO.Client import P4OOClientSet
from P4OO.Change import P4OOChangeSet
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOUser(_P4OOSpecObj):
    """
    Perforce User Spec Object

    id Required: No

    Forcible: Yes

    Attributes:
        user (str): Username of the user
        type (str): [service|operator|standard] Type of user
        fullname (str): Full name of the user
        email (str): Email address of the user
        jobview (str): Jobs to include in changelist creation
        password (str): P4PASSWD setting is required?
        authmethod (str): [`perforce`|`perforce+2fa`|`ldap`|`ldap+2fa`]
        reviews (str): Depot files to be reviewed by user
        update (datetime): Time of last update to the spec
        access (datetime): Time of last access of the spec

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_user.html
    """
    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'user'

    def listOpenedFiles(self, client=None):
        """ Return a P4OOFileSet of files opened by this user in the
            specified client workspace.
        """

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
    """ `P4OOSet` of `P4OOUser` objects """

    def query(self, allusers: bool=None, longoutput: bool=None,
              maxresults: int=None, users: str=None, **kwargs):
        """
        Executes 'p4 users' query

        Args:
            allusers (bool, optional): include service users in results
            longoutput (bool, optional): include the full changelist
                descriptions
            maxresults (int, optional): Return only the first <max> results
            users (P4OOUserSet | P4OOUserFile | str, optional): The set of
                users to query

        Returns:
            (P4OOUserSet): `P4OOSet` of `P4OOUser` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_users.html
        """
        return self._query(setObjType='users', allusers=allusers,
                           longoutput=longoutput, maxresults=maxresults,
                           users=users, **kwargs)
