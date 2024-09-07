######################################################################
#  Copyright (c)2012, 2015, 2024 David L. Armstrong.
#
#  P4OO.Group.py
#
######################################################################

from dataclasses import dataclass, field

from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet

@dataclass(unsafe_hash=True)
class P4OOGroup(_P4OOSpecObj):
    """
    Perforce Group Spec Object

    id Required: Yes

    Forcible: Yes

    Attributes:
        group (str): Name of the group
        description (str): Description field
        owners (P4OOUserSet | P4OOUser | str): Owners of the group
        users (P4OOUserSet | P4OOUser | str): Members of the group
        subgroups (P4OOGroupSet | P4OOGroup | str): Subgroup Members of
            the group
        sessiontimeout (int): Maximum duration a session ticket will be
            valid for members of this group
        passwordtimeout (int): Maximum duration a user password will be
            valid for members of this group
        maxresults (int): Maximum maxresults value for all queries by
            members of this group
        maxscanrows (int): Maximum rows that can be queried by members
            of this group
        maxlocktime (int): Maximum time (ms) any operation can lock any
            database by members of this group
        maxopenfiles (int): Maximum number of files any single command can
            open by members of this group
        maxmemory (int): Maximum memory (MB) any single command can use
            by members of this group


    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_group.html
    """

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'group'

@dataclass
class P4OOGroupSet(_P4OOSet):
    """ `P4OOSet` of `P4OOGroup` objects """

    def query(self, group: str=None, member: str=None, owner: str=None,
              indirect: str=None, maxresults: int=None, **kwargs):
        """
        Executes `p4 groups` query

        Args:
            group (P4OOGroup | str, optional): List groups that `group`
                is a member of
            member (P4OOUser | str, optional): List groups that `member`
                is a member of
            owner (P4OOUser | str, optional): List groups that `owner`
                is an owner of
            indirect (P4OOUser | P4OOGroup | str, optional): List
                indirect/transitive memberships as well as direct
            maxresults (int, optional): Return only the first [max] results

        Returns:
            (P4OOGroupSet): `P4OOSet` of `P4OOGroup` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_groups.html
        """

        return self._query(setObjType='groups', group=group, member=member,
                           indirect=indirect, owner=owner,
                           maxresults=maxresults, **kwargs)
