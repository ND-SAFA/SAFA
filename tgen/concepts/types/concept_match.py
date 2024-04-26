from typing_extensions import TypedDict


class ConceptMatch(TypedDict):
    """
    Artifact ID of concept matched.
    """
    artifact_id: str
    """
    Index in target artifact where match was found
    """
    loc: int
