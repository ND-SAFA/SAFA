from typing import Dict, List, TypedDict

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.concepts.types.concept_match import ConceptMatch


class ConceptPipelineResponse(TypedDict):
    """
    List of direct matches found in artifact.
    """
    matches: List[ConceptMatch]
    """
    List of ambiguous matches found in artifact.
    """
    multi_matches: Dict[int, List[ConceptMatch]]
    """
    List of predicted matches found in artifact.
    """
    predicted_matches: List[Trace]
    """
    Undefined entities.
    """
    undefined_entities: List[Artifact]
