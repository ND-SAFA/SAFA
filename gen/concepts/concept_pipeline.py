from typing import Type

from gen_common.pipeline.state import State

from gen.concepts.concept_args import ConceptArgs
from gen.concepts.concept_state import ConceptState
from gen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from gen.concepts.steps.predict_entity_step import PredictEntityStep
from gen_common.pipeline.abstract_pipeline import AbstractPipeline


class ConceptPipeline(AbstractPipeline[ConceptArgs, ConceptState]):
    steps = [
        DirectConceptMatchingStep,
        PredictEntityStep
    ]

    def __init__(self, args: ConceptArgs, **kwargs):
        """
        Creates pipeline with starting args.
        :param args: Args to initialize pipeline with.
        :param kwargs: Additional keyword arguments to pipeline
        """
        super().__init__(args, steps=self.steps, skip_summarization=True, **kwargs)
        self.state.concept_df = args.dataset.artifact_df.get_artifacts_by_type(args.concept_layer_id)

    def state_class(self) -> Type[State]:
        """
        :return: Returns ConceptState class
        """
        return ConceptState
