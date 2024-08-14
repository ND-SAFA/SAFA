from typing import List, Optional, TypedDict

from common_resources.tools.util.enum_util import EnumDict

from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.contradictions.contradictions_result import ContradictionsResult


class HealthCheckResults(TypedDict):
    context_traces: Optional[List[EnumDict]]
    contradictions: List[ContradictionsResult]


class ConceptPredictionResponse(TypedDict):
    concept_matches: Optional[ConceptPipelineResponse]
