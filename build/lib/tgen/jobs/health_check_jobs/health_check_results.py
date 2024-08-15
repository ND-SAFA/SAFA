from typing import List, Optional, TypedDict

from common_resources.tools.util.enum_util import EnumDict

from tgen.concepts.types.undefined_concept import UndefinedConcept
from tgen.health.contradictions_result import ContradictionsResult


class HealthCheckResults(TypedDict):
    context_traces: Optional[List[EnumDict]]
    contradictions: List[ContradictionsResult]
    undefined_concepts: List[UndefinedConcept]
