from typing import List, Optional, TypedDict

from gen_common.util.enum_util import EnumDict

from gen.health.concepts.extraction.undefined_concept import UndefinedConcept
from gen.health.contradiction.contradiction_result import ContradictionsResult


class HealthResults(TypedDict):
    context_traces: Optional[List[EnumDict]]
    contradictions: List[ContradictionsResult]
    undefined_concepts: List[UndefinedConcept]
