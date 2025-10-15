from dataclasses import dataclass
from typing import List

from gen_common.infra.base_object import BaseObject


@dataclass
class UndefinedConcept(BaseObject):
    """
    :param artifact_ids: IDs of artifact containing undefined concept.
    :param concept_id: ID of concept being referenced.
    :param definition: Predicted definition of concept.
    """
    artifact_ids: List[str]
    concept_id: str
    definition: str
