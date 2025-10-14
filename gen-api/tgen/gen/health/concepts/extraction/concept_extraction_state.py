from typing import Dict, List

from gen_common.pipeline.state import State

from gen.health.concepts.extraction.undefined_concept import UndefinedConcept


class ConceptExtractionState(State):
    """
    :param artifact2undefined: Map of artifact ids to undefined concepts found within them.
    :param undefined_concepts: List of undefined concepts found for query ids in dataset.
    """
    artifact2undefined: Dict[str, List[str]]
    undefined_concepts: List[UndefinedConcept]
