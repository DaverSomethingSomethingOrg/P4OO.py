######################################################################
#  Copyright (c)2011-2012,2015,2024 David L. Armstrong.
#
#  P4OO.Branch.py
#
######################################################################

from dataclasses import dataclass, field

from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet

@dataclass(unsafe_hash=True)
class P4OOBranch(_P4OOSpecObj):
    """
    Perforce Branch Spec Object

    id Required: Yes

    Forcible: Yes


    Attributes:
        branch (str): Name of the branch
        owner (P4OOUser): User that created the branch spec
        description (str): Description field
        options (str): [unlocked|locked]
        view (str): View spec mappings
        update (datetime): Time of last update to the spec
        access (datetime): Time of last access of the spec

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_branch.html
    """

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'branch'

@dataclass
class P4OOBranchSet(_P4OOSet):
    """ `P4OOSet` of `P4OOBranch` objects """

    def query(self, user: str=None, maxresults: int=None,
              namefilter: str=None, **kwargs):
        """
        Executes `p4 branches` query

        Args:
            user (P4OOUser | str, optional): The user that created the branch
            maxresults (int, optional): Return only the first <max> results
            namefilter (str, optional): Case-sensitive filter on branch name

        Returns:
            (P4OOBranchSet): `P4OOSet` of `P4OOBranch` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_branches.html
        """

        return self._query(setObjType='branches', user=user,
                           maxresults=maxresults, namefilter=namefilter,
                           **kwargs)
