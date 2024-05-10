from typing import Optional, List, TypedDict

from tgen.common.util.enum_util import EnumDict
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.contradictions.contradictions_result import ContradictionsResult


class HealthCheckResults(TypedDict):
    context_traces: Optional[List[EnumDict]]
    contradictions: Optional[ContradictionsResult]
    concept_matches: Optional[ConceptPipelineResponse]
