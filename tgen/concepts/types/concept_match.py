from tgen.common.util.typed_enum_dict import TypedEnumDict


class ConceptMatch(TypedEnumDict):
    """
    ID of artifact being matched.
    """
    artifact_id: str
    """
    ID of concept matched with.
    """
    concept_id: str
    """
    Index in target artifact where match started
    """
    start_loc: int
    """
    Index in target artifact where match ended
    """
    end_loc: int
    """
    String of match content
    """
    matched_content: str
