from typing import Dict, List

from tgen.common.constants.concept_pipeline_constants import ENTITY_DESCRIPTION_TAG, ENTITY_NAME_TAG, ENTITY_TAG
from tgen.common.objects.artifact import Artifact
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class EntityExtractionStep(AbstractPipelineStep):
    """
    Prompts LLM to list (and define) all acronyms found in artifact content.

    * This is just a starting point and more robust entity extraction must be researched.
    """

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Extracts the most important entities from the target artifact.
        :param args: Contains artifact content to extract entities from.
        :param state: Stored entity df.
        :return: None
        """
        artifact_content = args.artifact[ArtifactKeys.CONTENT]
        parsed_response = self.predict_artifact_prompt(artifact_content, SupportedPrompts.CONCEPT_ENTITY_EXTRACTION.value,
                                                       args.llm_manager)
        state.entity_df = self.create_entity_df(parsed_response[ENTITY_TAG], args.entity_layer_id)

    @staticmethod
    def create_entity_df(entity_response_dict: List[Dict], entity_layer_id: str) -> ArtifactDataFrame:
        """
        Parses the predicted entities inside of artifact.
        :param entity_response_dict: List of parsed entity predictions.
        :param entity_layer_id: Layer ID to give entities created.
        :return: Entity Artifacts.
        """
        entities = []
        for entity_dict in entity_response_dict:
            entity_name = entity_dict[ENTITY_NAME_TAG][0]
            entity_description = entity_dict[ENTITY_DESCRIPTION_TAG][0]
            entities.append(Artifact(id=entity_name, content=entity_description, layer_id=entity_layer_id, summary=""))
        return ArtifactDataFrame(entities)

    @staticmethod
    def predict_artifact_prompt(artifact_content: str,
                                instructions_prompt: Prompt,
                                llm_manager: AbstractLLMManager,
                                artifact_prompt_title="Artifact Content") -> Dict:
        """
        Predicts the response from the LLM based on the artifact content and additional instructions.
        :param artifact_content: The content of the artifact.
        :param instructions_prompt: Instructions to append to the artifact content.
        :param llm_manager: LLM manager instance to use for predictions.
        :param artifact_prompt_title: Title placed on top of artifact content.s
        :return: The parsed response from the LLM.
        """
        artifact_prompt = Prompt(artifact_content, prompt_args=PromptArgs(title=artifact_prompt_title))
        prompt_builder = PromptBuilder(prompts=[artifact_prompt, instructions_prompt])
        output = LLMTrainer.predict_from_prompts(
            llm_manager,
            prompt_builder,
        )
        return output.predictions[0][instructions_prompt.args.prompt_id]
