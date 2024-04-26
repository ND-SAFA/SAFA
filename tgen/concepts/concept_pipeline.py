from typing import Type

from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.create_response import CreateResponse
from tgen.concepts.steps.direct_concept_matches import DirectConceptMatches
from tgen.concepts.steps.entity_matching import EntityMatching
from tgen.concepts.steps.extract_artifact_entities import EntityExtraction
from tgen.pipeline.abstract_pipeline import AbstractPipeline
from tgen.pipeline.state import State


class ConceptPipeline(AbstractPipeline[ConceptArgs, ConceptState]):
    steps = [
        DirectConceptMatches,
        EntityExtraction,
        EntityMatching,
        CreateResponse
    ]

    def __init__(self, args: ConceptArgs, **kwargs):
        """
        Creates pipeline with starting args.
        :param args: Args to initialize pipeline with.
        :param kwargs: Additional keyword arguments to pipeline
        """
        super().__init__(args, steps=self.steps, skip_summarization=True, **kwargs)

    def state_class(self) -> Type[State]:
        """
        :return: Returns ConceptState class
        """
        return ConceptState
