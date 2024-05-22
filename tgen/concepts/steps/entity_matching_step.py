from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.types.entity_matching_context import EntityMatchingContext
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class EntityMatchingStep(AbstractPipelineStep):

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Matches entities to the concepts.
        :param args: Arguments to the concept pipeline.
        :param state: Current state of the concept pipeline.
        :return: None
        """
        context = EntityMatchingContext(args=args, state=state, artifact_id_map={}, prompt_builders=[], prompts=[])
        context.create_entity_matching_prompts()
        predictions = context.generate_predictions()
        state.predicted_matches = predictions
