from dataclasses import dataclass
from typing import List, Optional

from gen_common.infra.base_object import BaseObject
from gen_common.util.enum_util import EnumDict

from gen.health.concepts.extraction.undefined_concept import UndefinedConcept
from gen.health.contradiction.contradiction_result import ContradictionResult


@dataclass
class HealthResults(BaseObject):
    context_traces: Optional[List[EnumDict]]
    contradictions: List[ContradictionResult]
    undefined_concepts: List[UndefinedConcept]
