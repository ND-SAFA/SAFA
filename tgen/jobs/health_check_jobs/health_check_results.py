from dataclasses import dataclass
from typing import Optional, List

from tgen.common.util.enum_util import EnumDict
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse


@dataclass
class HealthCheckResults:
    related_traces: Optional[List[EnumDict]] = None
    conflicting_ids: Optional[List[str]] = None
    concept_matches: Optional[ConceptPipelineResponse] = None
