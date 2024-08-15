from typing import Dict, List, TypedDict

from tgen.concepts.types.concept_match import ConceptMatch
from tgen.concepts.types.entity_matching_pred import EntityMatchingPred


class ConceptPipelineResponse(TypedDict):
    """
    :param matches: List of direct matches found in artifact.
    :param multi_matches: List of ambigously matched concepts pertaining to the same word.
    :param predicted_matches: List of predicted matches.
=    """
    matches: List[ConceptMatch]
    """
    List of ambiguous matches found in artifact.
    """
    multi_matches: Dict[str, Dict[int, List[ConceptMatch]]]
    """
    List of predicted matches found in artifact.
    """
    predicted_matches: List[EntityMatchingPred]
