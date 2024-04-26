from tgen.common.objects.trace import Trace
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.util.prompt_prediction import predict_prompts
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager


class EntityMatching(AbstractPipelineStep):
    MATCH_TAG = "match"
    SOURCE_TAG = "source"
    TARGET_TAG = "target"

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Matches artifact entities to concepts.
        :param args: Contains artifact and concepts.
        :param state: Contains entities extracted from artifact.
        :return: None
        """
        entity_artifacts = state.entity_df.to_artifacts()
        concept_artifacts = args.concept_df.to_artifacts()

        entity_prompt = MultiArtifactPrompt("# Source Entities")
        concept_prompt = MultiArtifactPrompt("# Target Entities")
        instructions_prompt = Prompt(
            "Above are two sets of entities. "
            "Your task record which pairs of source and target entities are referring to the same entity. "
            f"Enclose each match in {self.create_example_xml('[SOURCE_ENTITY]', '[TARGET_ENTITY]')}",
            response_manager=PromptResponseManager(response_tag={self.MATCH_TAG: [self.SOURCE_TAG, self.TARGET_TAG]})
        )
        prompts = [entity_prompt.build(artifacts=entity_artifacts), concept_prompt.build(artifacts=concept_artifacts)]
        llm_manager = OpenAIManager()
        response = predict_prompts(instructions_prompt, prompts, llm_manager)

        matches = []
        for match in response[self.MATCH_TAG]:
            match_source = match[self.SOURCE_TAG][0]
            match_target = match[self.TARGET_TAG][0]
            matches.append(Trace(source=match_source, target=match_target))
        state.predicted_matches = matches

    @staticmethod
    def create_example_xml(source_text: str, target_text: str) -> str:
        """
        Creates example of how to enclose each match.
        :return: String representation.
        """
        return (
            f"<{EntityMatching.MATCH_TAG}>"
            f"<{EntityMatching.SOURCE_TAG}>{source_text}</{EntityMatching.SOURCE_TAG}>"
            f"<{EntityMatching.TARGET_TAG}>{target_text}</{EntityMatching.TARGET_TAG}>"
            f"</{EntityMatching.MATCH_TAG}>"
        )
