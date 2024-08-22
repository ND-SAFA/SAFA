from dataclasses import dataclass
from typing import List

from gen_common.infra.base_object import BaseObject


@dataclass
class ContradictionResult(BaseObject):
    conflicting_ids: List[str]
    explanation: str
