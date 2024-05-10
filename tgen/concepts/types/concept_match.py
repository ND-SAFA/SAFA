from tgen.common.util.typed_enum_dict import TypedEnumDict


class ConceptMatch(TypedEnumDict):
    """
    Artifact ID of concept matched.
    """
    id: str
    """
    Index in target artifact where match started
    """
    start_loc: int
    """
    Index in target artifact where match ended
    """
    end_loc: int
