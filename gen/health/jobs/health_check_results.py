from typing import List, Optional, TypedDict

from gen_common.util.enum_util import EnumDict

from gen.concepts.types.undefined_concept import UndefinedConcept
from gen.health.contradictions_result import ContradictionsResult


class HealthCheckResults(TypedDict):
    context_traces: Optional[List[EnumDict]]
    contradictions: List[ContradictionsResult]
    undefined_concepts: List[UndefinedConcept]
