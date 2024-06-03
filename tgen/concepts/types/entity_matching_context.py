from dataclasses import dataclass
from typing import Dict, List, Set

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.objects.artifact import Artifact
from tgen.common.util.prompt_util import PromptUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.types.entity_matching_pred import EntityMatchingPred
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager
from tgen.prompts.supported_prompts.concept_prompts import ENTITY_MATCHING_INSTRUCTIONS, ENTITY_MATCHING_RESPONSE_FORMAT


@dataclass
class EntityMatchingContext:
    MATCH_TAG = "match"
    SOURCE_TAG = "source"
    TARGET_TAG = "target"
    PROMPT_ID = "main"

    args: ConceptArgs
    state: ConceptState
    artifact_id_map: Dict[int, int] = None
    prompt_builders: List[PromptBuilder] = None
    prompts: List[Prompt] = None
    completions: List[Dict] = None
    entities: List[Artifact] = None
    _direct_match_content: Set = None

    def create_entity_matching_prompts(self) -> None:
        """
        Creates a prompt for each entity in each target artifact. Skips entities matched in direct matching step.
        :param self: Matching context containing target artifacts and their entities.
        :return: None. Context prompts is modified.
        """
        self.prompts = []
        self.prompt_builders = []
        self.entities = []
        self.artifact_id_map = {}

        direct_match_content = {match["matched_content"] for match in self.state.direct_matches}
        for artifact_index, (entity_df, target_artifact) in enumerate(zip(self.state.entity_data_frames, self.args.artifacts)):
            entities: List[Artifact] = entity_df.to_artifacts()
            concepts: List[Artifact] = self.state.concept_df.to_artifacts()
            if not entities or not concepts:
                self.state.predicted_matches = []
                continue

            filtered_entities = [e for e in entities if e[ArtifactKeys.ID] not in direct_match_content]
            self._create_prompts(filtered_entities,
                                 concepts,
                                 self.args.llm_manager.prompt_args,
                                 artifact_index)

    def generate_predictions(self) -> List[EntityMatchingPred]:
        """
        Generates prompt completions, parses completions, and creates entity matching predictions.
        :return: List of predicted matches for entities to concepts.
        """
        if self.prompts is None:
            raise Exception("Prompts have not been created in context.")
        if len(self.prompts) == 0:
            return []
        output = LLMTrainer.predict_from_prompts(
            self.args.llm_manager,
            message_prompts=self.prompts,
            prompt_builders=self.prompt_builders
        )
        completions = [prediction[EntityMatchingContext.PROMPT_ID] for prediction in output.predictions]

        predictions = []
        for i, completion in enumerate(completions):
            artifact_index = self.artifact_id_map[i]
            artifact = self.args.artifacts[artifact_index]
            entity = self.entities[i]
            matched_concept_ids = completion[EntityMatchingContext.MATCH_TAG]
            for concept_id in matched_concept_ids:
                predictions.append(
                    EntityMatchingPred(
                        artifact_id=artifact[ArtifactKeys.ID],
                        concept_id=concept_id,
                        entity_id=entity[ArtifactKeys.ID]
                    )
                )
        return predictions

    def _create_prompts(self, entities: List[Artifact], concepts: List[Artifact], prompt_args: PromptArgs,
                        artifact_index: int) -> None:
        """
        Creates a prompt for each entity to match against concepts.
        :param entities: List of entities to batch against concepts.
        :param concepts: The concepts to match entity against, included in each prompt.
        :param prompt_args: Prompt args to format prompts to.
        :param artifact_index: Index of artifacts associated with entities.
        :return: None
        """

        prompt_builders = []
        prompts = []
        for entity in entities:
            concept_prompt = MultiArtifactPrompt("# PROJECT ARTIFACTS", build_method=MultiArtifactPrompt.BuildMethod.XML)
            artifact_prompt = ArtifactPrompt(prompt_start=ENTITY_MATCHING_INSTRUCTIONS + NEW_LINE)
            response_format = ENTITY_MATCHING_RESPONSE_FORMAT.format(EntityMatchingContext.create_example_xml("ARTIFACT_ID"))
            instructions_prompt = Prompt(value=NEW_LINE, prompt_args=PromptArgs(prompt_id=EntityMatchingContext.PROMPT_ID),
                                         response_manager=XMLResponseManager(response_tag=EntityMatchingContext.MATCH_TAG,
                                                                             response_instructions_format=response_format))
            prompt_builder = PromptBuilder(prompts=[concept_prompt, artifact_prompt, instructions_prompt])
            prompt = prompt_builder.build(prompt_args, artifacts=concepts, artifact=entity)[PromptKeys.PROMPT]
            prompts.append(prompt)
            prompt_builders.append(prompt_builder)
            self.entities.append(entity)

        starting_index = len(self.prompts)
        self.prompt_builders.extend(prompt_builders)
        self.prompts.extend(prompts)

        for i, prompt in enumerate(prompts):
            self.artifact_id_map[starting_index + i] = artifact_index

    @staticmethod
    def create_example_xml(target_text: str) -> str:
        """
        Create XML example of how the model should respond with a prediction.
        :param target_text: The text to put inside the tags.
        :return: String example
        """
        return PromptUtil.create_xml(EntityMatchingContext.MATCH_TAG, target_text)
