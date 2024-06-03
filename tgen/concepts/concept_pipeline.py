from typing import Type

from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.create_response_step import CreateResponseStep
from tgen.concepts.steps.define_unknown_entities import DefineUnknownEntitiesStep
from tgen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from tgen.concepts.steps.entity_matching_step import EntityMatchingStep
from tgen.concepts.steps.predict_entity_step import PredictEntityStep
from tgen.pipeline.abstract_pipeline import AbstractPipeline
from tgen.pipeline.state import State


class ConceptPipeline(AbstractPipeline[ConceptArgs, ConceptState]):
    steps = [
        DirectConceptMatchingStep,
        PredictEntityStep,
        EntityMatchingStep,
        CreateResponseStep,
        DefineUnknownEntitiesStep
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
