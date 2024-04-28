######################################################################
#  Copyright (c)2011-2012,2015,2024 David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO.Label.py
#
######################################################################


from P4OO.Exceptions import P4Warning
from P4OO.Change import P4OOChangeSet
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOLabel(_P4OOSpecObj):
    """
    Perforce Label Spec Object

    id Required: Yes

    Forcible: Yes

    Attributes:
        label (str): Name of the label
        owner (P4OOUser): User that owns the label spec
        description (str): Description field
        options (str): [`locked`|`unlocked`|`autoreload`|`noautoreload`]
        revision (str): optional revision specification for automatic label
        view (str): View spec mappings
        update (datetime): Time of last update to the spec
        access (datetime): Time of last access of the spec

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_label.htm
    """

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'label'

    def getRevision(self):
        """ Return the revision spec attribute of the label """

        return self._getSpecAttr('Revision')

    def tagFiles(self, *fileSpec, **kwargs):
        """ Tag the specified files against label (self) """

        p4Output = None
        p4Output = self._runCommand('tag', label=self, files=fileSpec,
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

    def getLastChange(self):
        """ Return the latest change incorporated into the label

            Return None if the label sees no changes (empty depot).
        """

        changeFileRevRange = "@" + self._getSpecID()

        changeSet = P4OOChangeSet(_p4Conn=self._getP4Connection())
        p4Changes = changeSet.query(files=changeFileRevRange, maxresults=1)

        if len(p4Changes) == 0:
            return None

        # We only expect one result, we only return one result.
        return p4Changes[0]

    def getChangesFromLabels(self, otherLabel, client):
        """ Fetch the list of changes from this label to another one.

            Assumptions:
            - self represents the lower of the two labels.  If the other
              direction is desired, then make the call against the other
              label instead.
        """

        if not isinstance(otherLabel, P4OOLabel):
            raise TypeError(otherLabel)

        firstChange = self.getLastChange()
        lastChange = otherLabel.getLastChange()

        return firstChange.getChangesFromChangeNums(lastChange, client)

    def getDiffsFromLabels(self, otherLabel, client, **diffOpts):
        """ Fetch the list of diffs from this label to another one """

        if not isinstance(otherLabel, P4OOLabel):
            raise TypeError(otherLabel)

        firstLabelName = self._getSpecID()
        otherLabelName = otherLabel._getSpecID()

        diffText = []
        view = client._getSpecAttr('View')
        for viewLine in view:
            viewSpec = viewLine.split(" ", 2)

            firstLabelPath = '%s@%s' % (viewSpec[0], firstLabelName)
            otherLabelPath = '%s@%s' % (viewSpec[0], otherLabelName)

            try:
                # ask for rawOutput so we get the actual diff content,
                # not just the diff tags.
                viewDiffs = self._runCommand('diff2',
                                             rawOutput=True,
                                             files=[firstLabelPath,
                                                    otherLabelPath],
                                             **diffOpts)
                diffText.extend(viewDiffs)

            except P4Warning:
                # This gets thrown if no files exist in view path
                pass

        return diffText


class P4OOLabelSet(_P4OOSet):
    """ `P4OOSet` of `P4OOLabel` objects """

    def query(self, user: str=None, maxresults: int=None,
              namefilter: str=None, files: str=None, **kwargs):
        """
        Executes `p4 labels` query

        Args:
            user (P4OOUser | str, optional): The user that owns the label
            maxresults (int, optional): Return only the first [max] results
            namefilter (str, optional): Case-sensitive filter on label name
            files (P4OOFileSet | P4OOFile | str, optional): The set of file
                revisions to query

        Returns:
            (P4OOLabelSet): `P4OOSet` of `P4OOLabel` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_labels.html
        """

        return self._query(setObjType='labels', user=user,
                           maxresults=maxresults, namefilter=namefilter,
                           files=files, **kwargs)
