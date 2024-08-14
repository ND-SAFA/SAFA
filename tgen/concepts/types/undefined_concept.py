from typing import List

from common_resources.tools.util.typed_enum_dict import TypedEnumDict


class UndefinedConcept(TypedEnumDict):
    """
    :param artifact_ids: IDs of artifact containing undefined concept.
    :param concept_id: ID of concept being referenced.
    :param concept_definition: Predicted definition of concept.
    """
    artifact_ids: List[str]
    concept_id: str
    concept_definition: str
