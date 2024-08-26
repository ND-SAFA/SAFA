from dataclasses import field
from typing import Dict, List

from gen_common.data.objects.trace import Trace
from gen_common.pipeline.state import State

from gen.health.concepts.matching.types.concept_direct_match import ConceptDirectMatch


class ConceptMatchingState(State):
    """
    List of concepts found directly in target artifact.
    """
    direct_matches: List[ConceptDirectMatch] = field(default_factory=lambda: [])
    """"
    List of predicted links between entities and concepts.
    """
    predicted_matches: List[Trace] = field(default_factory=lambda: [])
    """
    List of matches containing identical identifier but having different definitions.
    """
    multi_matches: Dict[str, Dict[int, List[ConceptDirectMatch]]] = field(default_factory=dict)
