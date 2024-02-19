######################################################################
#  Copyright (c)2011-2012, 2015, 2024 David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO.Change.py
#
######################################################################


from P4OO.Exceptions import P4Fatal
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOChange(_P4OOSpecObj):
    """
    Perforce Change Spec Object

    id Required: Yes

    Forcible: Yes

    Attributes:
        change (int): Change #
        user (P4OOUser): User that created the change spec
        description (str): Description field
        client (P4OOClient | str): Current client workspace
        status (str): [`pending`|`shelved`|`submitted`|`new`]
        type (str): [`restricted`|`public`]
        jobs (P4OOJobSet | P4OOJob | str): List of jobs that are fixed by this change
        date (datetime): Time of last update to the spec

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_change.html
    """

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'change'

    def getChangesFromChangeNums(self, otherChange, client):
        """ Fetch the list of changes from this change to another one.

            ASSUMPTIONS:
            - self represents the lower of the two changes.  If the other
              direction is desired, then make the call against the other
              change instead.
        """

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

            changeSet = P4OOChangeSet(_p4Conn=self._getP4Connection())
            viewChanges = changeSet.query(files=fileChangeRange,
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
    """ `P4OOSet` of `P4OOChange` objects """

    def query(self, client: str=None, user: str=None, maxresults: int=None,
              status: str=None, files: str=None, longoutput: bool=None,
              **kwargs):
        """
        Executes 'p4 changes' query

        Args:
            client (P4OOClient | str, optional): The client (viewspec) to
                filter file revisions through
            user (P4OOUser | str, optional): The user that created the change
            maxresults (int, optional): Return only the first <max> results
            status (str, optional): Filter changes by status:
                [`pending`|`shelved`|`submitted`]
            files (P4OOFileSet | P4OOFile | str, optional): The set of file
                revisions to query
            longoutput (bool, optional): include the full changelist
                descriptions

        Returns:
            (P4OOChangeSet): `P4OOSet` of `P4OOChange` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_changes.html
        """
        return self._query(setObjType='changes', client=client, user=user,
                           maxresults=maxresults, status=status, files=files,
                           longoutput=longoutput, **kwargs)
