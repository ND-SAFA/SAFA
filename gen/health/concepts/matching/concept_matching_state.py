from dataclasses import dataclass, field
from typing import List

from gen_common.data.objects.trace import Trace
from gen_common.pipeline.state import State

from gen.health.concepts.matching.types.concept_direct_match import ConceptDirectMatch


@dataclass
class ConceptMatchingState(State):
    """
    List of concepts found directly in target artifact.
    """
    direct_matches: List[ConceptDirectMatch] = field(default_factory=lambda: [])
    """"
    List of predicted links between entities and concepts.
    """
    predicted_matches: List[Trace] = field(default_factory=lambda: [])
