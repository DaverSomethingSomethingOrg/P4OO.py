######################################################################
#  Copyright (c)2011-2012,2015,2024 David L. Armstrong.
#  Copyright (c)2012, Cisco Systems, Inc.
#
#  P4OO.Client.py
#
######################################################################

'''
Perforce Client object

P4OO.Client provides standard P4OO._SpecObj behaviors

Spec Attributes:
      client
      description
      owner
      host
      root
      altroots
      options
      submitoptions
      lineend
      view
  datetime Attributes:
      update
      access

Query Options:
      user:
        type: [ string, P4OOUser ]
        multiplicity: 1
      owner: (interchangeable with user)
      namefilter:
        type: [ string ]
        multiplicity: 1
      maxresults:
        type: [ integer ]
        multiplicity: 1
'''

import re
from P4OO.Change import P4OOChangeSet
from P4OO.Exceptions import P4Warning, P4Fatal
from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOClient(_P4OOSpecObj):
    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'client'

    def addFiles(self, *fileSpec, **kwargs):
        ''' Add the specified files as new '''

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
        ''' Open the specified files for edit '''

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
        ''' Find all changes this client "has" sync'd '''

        # Asking a Client for its changes is implemented as querying
        # Changes filtered by Client
        changeSet = P4OOChangeSet(_p4Conn=self._getP4Connection())
        return changeSet.query(client=self, status=status)

    def getLatestChange(self):
        ''' find the latest change this client "has" '''

        # Asking a Client for its latest change is just querying the first
        # change record.  Nifty.
        changeSet = P4OOChangeSet(_p4Conn=self._getP4Connection())
        p4Changes = changeSet.query(files="#have", maxresults=1, client=self)

        # We only expect one result, we only return one result.
        return p4Changes[0]

    def getOpenedFiles(self, user=None):
        ''' Return a P4OOFileSet of files opened in this client. '''

        return self._runCommand('opened', user=user, client=self)

    def submitChange(self, *fileSpec, **kwargs):
        ''' Add the specified files as new '''

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
        ''' Sync the client (p4 sync) using the optional supplied
            fileSpec(s)
        '''

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
    ''' P4OOClientSet currently implements no custom logic of its own. '''

    # Subclasses must define SETOBJ_TYPE
    _SETOBJ_TYPE = 'clients'
