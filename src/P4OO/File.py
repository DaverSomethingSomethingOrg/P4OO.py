######################################################################
#  Copyright (c)2012, David L. Armstrong.
#
#  P4OO.File.py
#
######################################################################


from P4OO._Base import _P4OOBase
from P4OO._Set import _P4OOSet


class P4OOFile(_P4OOBase):
    """
    Perforce File Object

    The P4OOFile object does not have a first-class equivalent in Perforce.
    It is just used to manage a path to a local file, or a depot file,
    or a revision range, or...  Anything used to communicate filenames to
    Perforce really.

    Within P4OO.py, P4OOFile objects are used to track and connect output
    from one Perforce operation to the next, carrying your _P4OOConnection
    object(s) along for the ride.

    id Required: Yes

    Attributes:
        None

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_files.html
    """

# TODO File are not Spec Objects, but...
#    # Subclasses must define SPECOBJ_TYPE
#    _SPECOBJ_TYPE = 'file'

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._getAttr('id'))


class P4OOFileSet(_P4OOSet):
    """ `P4OOSet` of `P4OOFile` objects """

    def query(self, archived: bool=False, allrevisions: bool=False,
              excludeDeleted: bool=False, maxresults: int=None,
              files: str=None, **kwargs):
        """
        Executes 'p4 files' query

        Args:
            archived (bool, optional): List all revisions in specified range
            allrevisions (bool, optional): Limit output to files in
                archive depots
            excludeDeleted (bool, optional): Exclude deleted/archived files.
                archive depots
            maxresults (int, optional): Return only the first <max> results
            files (P4OOFileSet | P4OOFile | str, optional): The set of file
                revisions to query

        Returns:
            (P4OOFileSet): `P4OOSet` of `P4OOFile` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_files.html
        """
        return self._query(setObjType='files', archived=archived,
                           allrevisions=allrevisions, excludeDeleted=excludeDeleted,
                           maxresults=maxresults, files=files, **kwargs)
