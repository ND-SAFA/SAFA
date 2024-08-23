from typing import Type

from gen_common.pipeline.abstract_pipeline import AbstractPipeline
from gen_common.pipeline.state import State

from gen.health.concepts.matching.steps.direct_concept_matching_step import DirectConceptMatchingStep
from gen.health.concepts.matching.steps.llm_concept_matching_step import LLMConceptMatchingStep
from gen.health.health_args import HealthArgs
from gen.health.health_state import HealthState


class ConceptMatchingPipeline(AbstractPipeline[HealthArgs, HealthState]):
    steps = [
        DirectConceptMatchingStep,
        LLMConceptMatchingStep
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
        return HealthState
