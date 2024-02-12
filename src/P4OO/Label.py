######################################################################
#  Copyright (c)2011-2012,2015,2024 David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO.Label.py
#
######################################################################

#NAME / DESCRIPTION
'''
Perforce Label Object

P4OO.Label provides standard P4OO._SpecObj behaviors

Spec Attributes:
      label
      description
      owner
      options
      revision
      view
  datetime Attributes:
      update
      access

Query Options:
      user:
        type: [ string, P4OOUser ]
        multiplicity: 1
      owner: (interchangeable with user)
      maxresults:
        type: [ integer ]
        multiplicity: 1
      namefilter:
        type: [ string ]
        multiplicity: 1
      files:
        type: [ string, File, FileSet ]
'''

######################################################################
# Includes
#
from P4OO._Exceptions import _P4Warning
from P4OO.Change import P4OOChangeSet
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


######################################################################
# P4Python Class Initialization
#
class P4OOLabel(_P4OOSpecObj):
    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'label'

    def getRevision(self):
        ''' Return the revision spec attribute of the label '''

        return self._getSpecAttr('Revision')


    def tagFiles(self, *fileSpec, **kwargs):
        ''' Tag the specified files against label (self) '''

        p4Output = None
        p4Output = self._runCommand('tag', label=self, files=fileSpec, **kwargs)

#TODO error checking
#        try:
#            p4Output = self._runCommand('add', p4client=self, files=fileSpec, **kwargs)
#        except _P4Warning as e:
#            if re.search(r"\nWARNING: File\(s\) up-to-date\.$", str(e)):
#                pass
#            else:
#                raise(e)

        return p4Output


    def getLastChange(self):
        ''' Return the latest change incorporated into the label

            Return None if the label sees no changes (empty depot).
        '''

        changeFileRevRange = "@" + self._getSpecID()
        p4Changes = self.query(P4OOChangeSet, files=changeFileRevRange, maxresults=1)

        if len(p4Changes) == 0:
            return None

        # We only expect one result, we only return one result.
        return p4Changes[0]


    def getChangesFromLabels(self, otherLabel, client):
        ''' Fetch the list of changes from this label to another one.
        
            Assumptions:
            - self represents the lower of the two labels.  If the other
              direction is desired, then make the call against the other
              label instead.
        '''

        if not isinstance(otherLabel, P4OOLabel):
            raise TypeError(otherLabel)

        firstChange = self.getLastChange()
        lastChange = otherLabel.getLastChange()

        return firstChange.getChangesFromChangeNums(lastChange, client)


    def getDiffsFromLabels(self, otherLabel, client, **diffOpts):
        ''' Fetch the list of diffs from this label to another one '''

        if not isinstance(otherLabel, P4OOLabel):
            raise TypeError(otherLabel)

        firstLabelName = self._getSpecID()
        otherLabelName = otherLabel._getSpecID()

        diffText = []
        view = client._getSpecAttr('View')
        for viewLine in view:
            viewSpec = viewLine.split(" ",2)

            firstLabelPath = '%s@%s' % (viewSpec[0], firstLabelName)
            otherLabelPath = '%s@%s' % (viewSpec[0], otherLabelName)

            try:
                # ask for rawOutput so we get the actual diff content, not just the diff tags.
                viewDiffs = self._runCommand('diff2',
                                             rawOutput=True,
                                             files=[firstLabelPath, otherLabelPath],
                                             **diffOpts
                                            )
                diffText.extend(viewDiffs)
            except _P4Warning:  # This gets thrown if no files exist in view path
                pass

        return diffText


class P4OOLabelSet(_P4OOSet):
    ''' P4OOLabelSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'labels'
