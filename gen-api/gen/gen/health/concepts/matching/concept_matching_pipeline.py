from typing import Type

from gen_common.pipeline.abstract_pipeline import AbstractPipeline
from gen_common.pipeline.state import State

from gen.health.concepts.matching.concept_matching_state import ConceptMatchingState
from gen.health.concepts.matching.steps.direct_concept_matching_step import DirectConceptMatchingStep
from gen.health.concepts.matching.steps.llm_concept_matching_step import LLMConceptMatchingStep
from gen.health.concepts.matching.steps.multi_match_step import MultiMatchStep
from gen.health.health_args import HealthArgs


class ConceptMatchingPipeline(AbstractPipeline[HealthArgs, ConceptMatchingState]):
    steps = [
        DirectConceptMatchingStep,
        LLMConceptMatchingStep,
        MultiMatchStep
    ]

    def __init__(self, args: HealthArgs, **kwargs):
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
        return ConceptMatchingState
