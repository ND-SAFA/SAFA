from dataclasses import dataclass
from typing import List

from gen_common.infra.base_object import BaseObject


@dataclass
class ContradictionResult(BaseObject):
    """
    Artifact Ids forming a contradiction.
    """
    conflicting_ids: List[str]
    """
    Explanation of contradiction.
    """
    explanation: str
