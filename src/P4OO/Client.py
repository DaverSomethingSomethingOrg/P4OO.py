######################################################################
#  Copyright (c)2011-2012,2015,2024 David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO.Client.py
#
######################################################################


import re
from P4OO.Exceptions import P4Warning, P4Fatal
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet
from P4OO.Change import P4OOChangeSet


class P4OOClient(_P4OOSpecObj):
    """
    Perforce Client Spec Object

    id Required: No

    Forcible: Yes

    Attributes:
        client (str): Name of the client
        owner (P4OOUser): User that created the client spec
        description (str): Description field
        host (str): Name of the host where this client root exists
        root (str): Root directory on <host> where client exists
        altroots (str): Alternate directories to locate root
        options (str): Client options (see Command Reference for details)
        submitoptions (str): How `submit` should handle unchanged files
        lineend (str): [`local`|`unix`|`mac`|`win`|`share`] CRLF handling
        view (str): View spec mappings
        update (datetime): Time of last update to the spec
        access (datetime): Time of last access of the spec

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_client.html
    """

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'client'

    def addFiles(self, *fileSpec, **kwargs):
        """ Add the specified files as new """

        p4Output = None
        p4Output = self._runCommand('add', p4client=self, files=fileSpec,
                                    **kwargs)

# TODO error checking
#        try:
#            p4Output = self._runCommand('add', p4client=self, files=fileSpec,
#                                        **kwargs)
#        except P4Warning as e:
#            if re.search(r"\nWARNING: File\(s\) up-to-date\.$", str(e)):
#                pass
#            else:
#                raise(e)

        return p4Output

    def editFiles(self, *fileSpec, **kwargs):
        """ Open the specified files for edit """

        p4Output = None
        p4Output = self._runCommand('edit', p4client=self, files=fileSpec,
                                    **kwargs)

# TODO error checking
#        try:
#            p4Output = self._runCommand('add', p4client=self, files=fileSpec,
#                                        **kwargs)
#        except P4Warning as e:
#            if re.search(r"\nWARNING: File\(s\) up-to-date\.$", str(e)):
#                pass
#            else:
#                raise(e)

        return p4Output

    def getChanges(self, status=None):
        """ Find all changes this client "has" sync'd """

        # Asking a Client for its changes is implemented as querying
        # Changes filtered by Client
        changeSet = P4OOChangeSet(_p4Conn=self._getP4Connection())
        return changeSet.query(client=self, status=status)

    def getLatestChange(self):
        """ find the latest change this client "has" """

        # Asking a Client for its latest change is just querying the first
        # change record.  Nifty.
        changeSet = P4OOChangeSet(_p4Conn=self._getP4Connection())
        p4Changes = changeSet.query(files="#have", maxresults=1, client=self)

        # We only expect one result, we only return one result.
        return p4Changes[0]

    def getOpenedFiles(self, user=None):
        """ Return a P4OOFileSet of files opened in this client. """

        return self._runCommand('opened', user=user, client=self)

    def submitChange(self, *fileSpec, **kwargs):
        """ Add the specified files as new """

        p4Output = None
        p4Output = self._runCommand('submit', p4client=self, files=fileSpec,
                                    **kwargs)

# TODO error checking
#        try:
#            p4Output = self._runCommand('add', p4client=self,
#                                        files=fileSpec, **kwargs)
#        except P4Warning as e:
#            if re.search(r"\nWARNING: File\(s\) up-to-date\.$", str(e)):
#                pass
#            else:
#                raise(e)

        return p4Output

    def sync(self, *fileSpec, **kwargs):
        """ Sync the client (p4 sync) using the optional supplied
            fileSpec(s)
        """

        p4Output = None
        try:
            p4Output = self._runCommand('sync', p4client=self,
                                        files=fileSpec, **kwargs)
        except P4Warning as e:
            if re.search(r"\nWARNING: File\(s\) up-to-date\.$", str(e)):
                pass
            else:
                raise e

        return p4Output

    def reopenFiles(self):
        self._delSpecAttr('host')
        self.saveSpec()
        try:
            return self._runCommand('reopen', files="//%s/..."
                                    % self._getSpecID(), p4client=self)
        except P4Warning:
            return True

    def revertOpenedFiles(self):
        self.reopenFiles()
        try:
            return self._runCommand('revert', noclientrefresh=True,
                                    files="//%s/..." % self._getSpecID(),
                                    p4client=self)
        except P4Warning:
            return True

    def deleteWithVengeance(self):
        try:
            self.deleteSpec(force=True)
        except P4Fatal:
            # First, simplify things by removing any Host spec attr for
            # this client
            self._delSpecAttr('host')
            self.saveSpec()

            # Next try removing pending changes, then try spec again
            changes = self.getChanges(status="pending")
            for change in changes:
                change.deleteWithVengeance()
            self.deleteSpec(force=True)

        return True


class P4OOClientSet(_P4OOSet):
    """ `P4OOSet` of `P4OOClient` objects """

    def query(self, user: str=None, maxresults: int=None,
              namefilter: str=None, **kwargs):
        """
        Executes 'p4 clients' query

        Args:
            user (P4OOUser | str, optional): The user that created the change
            maxresults (int, optional): Return only the first <max> results
            namefilter (str, optional): Case-sensitive filter on client name

        Returns:
            (P4OOClientSet): `P4OOSet` of `P4OOClient` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_clients.html
        """
        return self._query(setObjType='clients', user=user,
                           maxresults=maxresults, namefilter=namefilter,
                           **kwargs)
