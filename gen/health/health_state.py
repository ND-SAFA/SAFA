from dataclasses import dataclass, field
from typing import List

from gen_common.data.objects.trace import Trace
from gen_common.pipeline.state import State

from gen.health.concepts.extraction.undefined_concept import UndefinedConcept
from gen.health.concepts.matching.types.concept_direct_match import ConceptDirectMatch
from gen.health.contradiction.contradiction_result import ContradictionResult


@dataclass
class HealthState(State):
    """
    List of contradictions found in query artifacts.
    """
    contradictions: List[ContradictionResult] = field(default_factory=lambda: [])
    """
    List of undefined concepts found in query artifacts.
    """
    undefined_concepts: List[UndefinedConcept] = field(default_factory=lambda: [])
    """
    List of concepts found directly in target artifact.
    """
    direct_matches: List[ConceptDirectMatch] = field(default_factory=lambda: [])
    """"
    List of predicted links between entities and concepts.
    """
    predicted_matches: List[Trace] = field(default_factory=lambda: [])
