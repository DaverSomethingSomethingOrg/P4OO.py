######################################################################
#  Copyright (c)2012,2015,2024 David L. Armstrong.
#
#  P4OO.Job.py
#
######################################################################


from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OOJob(_P4OOSpecObj):
    """
    Perforce Job Spec Object

    id Required: No

    Forcible: Yes

    Attributes:
        job (str): Name of the job
        user (P4OOUser): User that created the job spec
        description (str): Description field
        status (str): [`open`|`closed`|`suspended`]
        date (datetime): Time of last update to the spec

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_job.html
    """

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'job'


class P4OOJobSet(_P4OOSet):
    """ `P4OOSet` of `P4OOJob` objects """

    def query(self, jobview: str=None, maxresults: int=None,
              files: str=None, longoutput: bool=None,
              **kwargs):
        """
        Executes `p4 jobs` query

        Args:
            jobview (str, optional): List only those jobs matching
                specified job view
            maxresults (int, optional): Return only the first [max] results
            files (P4OOFileSet | P4OOFile | str, optional): The set of file
                revisions to query
            longoutput (bool, optional): include the full changelist
                descriptions

        Returns:
            (P4OOJobSet): `P4OOSet` of `P4OOJob` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_jobs.html
        """

        return self._query(setObjType='jobs', jobview=jobview,
                           maxresults=maxresults, files=files,
                           longoutput=longoutput, **kwargs)
