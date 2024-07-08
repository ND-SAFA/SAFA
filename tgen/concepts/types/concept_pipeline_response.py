from typing import Dict, List, TypedDict

from tgen.concepts.types.concept_match import ConceptMatch
from tgen.concepts.types.entity_matching_pred import EntityMatchingPred
from tgen.concepts.types.undefined_concept import UndefinedConcept


class ConceptPipelineResponse(TypedDict):
    """
    List of direct matches found in artifact.
    """
    matches: List[ConceptMatch]
    """
    List of ambiguous matches found in artifact.
    """
    multi_matches: Dict[str, Dict[int, List[ConceptMatch]]]
    """
    List of predicted matches found in artifact.
    """
    predicted_matches: List[EntityMatchingPred]
    """
    Undefined entities.
    """
    undefined_entities: List[UndefinedConcept]
