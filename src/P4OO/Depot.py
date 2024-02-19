######################################################################
#  Copyright (c)2012,2015,2024 David L. Armstrong.
#
#  P4OO.Depot.py
#
######################################################################


from P4OO._SpecObj import _P4OOSpecObj
from P4OO._Set import _P4OOSet


class P4OODepot(_P4OOSpecObj):
    """
    Perforce Depot Spec Object

    id Required: Yes

    Forcible: No

    Attributes:
        depot (str): Name of the depot
        owner (P4OOUser): User that created the depot spec
        description (str): Description field
        type (str): [`remote`|`local`|`stream`|`spec`|`archive`|`graph`|`trait`]
        address (str): P4PORT address for `remote` depot type
        suffix (str): filename extension for storing `spec`
        map (str): Relative location of the depot subdirectory
        date (datetime): Time of last update to the spec

    See Also:
        Perforce Helix Core Command Reference:
        https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_depot.html
    """

    # Subclasses must define SPECOBJ_TYPE
    _SPECOBJ_TYPE = 'depot'


class P4OODepotSet(_P4OOSet):
    """ `P4OOSet` of `P4OODepot` objects """

    def query(self, depottype: str=None, namefilter: str=None, **kwargs):
        """
        Executes 'p4 depots' query

        Args:
            depottype (str, optional):
                [`remote`|`local`|`stream`|`spec`|`archive`|`graph`|`trait`]
            namefilter (str, optional): Case-sensitive filter on depot name

        Returns:
            (P4OODepotSet): `P4OOSet` of `P4OODepot` objects matching query
                parameters

        See Also:
            Perforce Helix Core Command Reference:
            https://www.perforce.com/manuals/cmdref/Content/CmdRef/p4_depots.html
        """
        return self._query(setObjType='depots', depottype=depottype,
                           namefilter=namefilter, **kwargs)
