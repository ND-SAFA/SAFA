from common_resources.tools.util.typed_enum_dict import TypedEnumDict


class EntityMatchingPred(TypedEnumDict):
    """
    :param artifact_id: ID of artifact whose entity was predicted to match against concept.
    :param entity_id: ID of entity matched.
    :param concept_id: ID of concept matched against entity.
    """
    artifact_id: str
    entity_id: str
    concept_id: str
