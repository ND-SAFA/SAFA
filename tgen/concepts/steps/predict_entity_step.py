from typing import Dict, List, Set

import stanza

from tgen.common.constants.concept_pipeline_constants import ENTITY_NAME_TAG, ENTITY_TAG
from tgen.common.constants.deliminator_constants import EMPTY_STRING, F_SLASH, SPACE
from tgen.common.objects.artifact import Artifact
from tgen.common.util.str_util import StrUtil
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


class PredictEntityStep(AbstractPipelineStep):
    """
    Prompts LLM to list (and define) all acronyms found in artifact content.

    * This is just a starting point and more robust entity extraction must be researched.
    """

    def __init__(self):
        """
        Initializes the pipeline from StandfordNLP.
        """
        self.nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Extracts the most important entities from the target artifact.
        :param args: Contains artifact content to extract entities from.
        :param state: Stored entity df.
        :return: None
        """
        if args.use_llm_for_entity_extraction:
            artifact_responses = self.predict_artifact_prompt(args.artifacts,
                                                              SupportedPrompts.CONCEPT_ENTITY_EXTRACTION.value,
                                                              args.llm_manager)
        else:
            direct_match_content = {match["matched_content"] for match in state.direct_matches}
            artifact_responses = self.identify_entities_with_stanza(args.artifacts, direct_match_content)

        data_frames = []
        for artifact, artifact_response in zip(args.artifacts, artifact_responses):
            artifact_entity_df = self.create_artifact_df(artifact_response[ENTITY_TAG], args.entity_layer_id)
            data_frames.append(artifact_entity_df)
        state.entity_data_frames = data_frames

    @staticmethod
    def predict_artifact_prompt(artifacts: List[Artifact],
                                instructions_prompt: Prompt,
                                llm_manager: AbstractLLMManager,
                                artifact_prompt_title="Artifact Content") -> List[Dict]:
        """
        Predicts the response from the LLM based on the artifact content and additional instructions.
        :param artifacts: The artifact to complete prompt for.
        :param instructions_prompt: Instructions to append to the artifact content.
        :param llm_manager: LLM manager instance to use for predictions.
        :param artifact_prompt_title: Title placed on top of artifact content.s
        :return: The parsed response from the LLM.
        """
        prompt_builders = []
        for artifact in artifacts:
            artifact_prompt = Prompt(artifact[ArtifactKeys.CONTENT], prompt_args=PromptArgs(title=artifact_prompt_title))
            prompt_builder = PromptBuilder(prompts=[artifact_prompt, instructions_prompt])
            prompt_builders.append(prompt_builder)

        output = LLMTrainer.predict_from_prompts(
            llm_manager,
            prompt_builders,
        )

        predictions = []
        for prompt_builder, prompt_builder_prediction in zip(prompt_builders, output.predictions):
            prompt_builder_output = prompt_builder_prediction[instructions_prompt.args.prompt_id]
            predictions.append(prompt_builder_output)

        return predictions

    @staticmethod
    def create_artifact_df(entity_response_dict: List[Dict], entity_layer_id: str) -> ArtifactDataFrame:
        """
        Parses the predicted entities inside of artifact.
        :param entity_response_dict: List of parsed entity predictions.
        :param entity_layer_id: Layer ID to give entities created.
        :return: Entity Artifacts.
        """
        entities = []
        for entity_dict in entity_response_dict:
            if ENTITY_NAME_TAG not in entity_dict:
                continue
            entity_name = entity_dict[ENTITY_NAME_TAG][0]
            entities.append(Artifact(id=entity_name, content=EMPTY_STRING, layer_id=entity_layer_id))
        return ArtifactDataFrame(entities)

    def identify_entities_with_stanza(self, artifacts: List[Artifact], direct_match_content: Set[str]) -> List[dict]:
        """
        Finds any entities that are mentioned in target artifact using stanza package.
        :param artifacts: All artifacts to identify the entities.
        :param direct_match_content: Set of concept that was directly matched.
        :return: List of identified entities for each artifact, formatted in a response dict.
        """
        entities_response = []
        for artifact in artifacts:
            target_artifact_content = artifact[ArtifactKeys.CONTENT]
            doc = self.nlp(target_artifact_content)
            entities = {self.process_entity(e.text) for e in doc.entities if e.text not in direct_match_content}
            artifacts = [{ENTITY_NAME_TAG: [e]} for e in entities if len(e) > 1 and not StrUtil.is_number(e)]
            entities_response.append({ENTITY_TAG: artifacts})
        return entities_response

    @staticmethod
    def process_entity(entity: str) -> str:
        """
        Run's pre-processing on the entity to clean it.
        :param entity: The entity to process.
        :return: The processed entity.
        """
        processed_entity = entity.replace(F_SLASH, SPACE)
        processed_entity = StrUtil.remove_stop_words(processed_entity)
        processed_entity = StrUtil.remove_common_words(processed_entity)
        return processed_entity
