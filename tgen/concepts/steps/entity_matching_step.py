from typing import Dict, List, Set

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.util.prompt_util import PromptUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.supported_prompts.concept_prompts import ENTITY_MATCHING_INSTRUCTIONS, ENTITY_MATCHING_RESPONSE_FORMAT


class EntityMatchingStep(AbstractPipelineStep):
    MATCH_TAG = "match"
    SOURCE_TAG = "source"
    TARGET_TAG = "target"
    PROMPT_ID = "main"

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Matches artifact entities to concepts.
        :param args: Contains artifact and concepts.
        :param state: Contains entities extracted from artifact.
        :return: None
        """
        entities: List[Artifact] = self.strip_artifact_bodies(state.entity_df.to_artifacts())
        if not entities:
            state.predicted_matches = []
            return
        concepts: List[Artifact] = self.strip_artifact_bodies(state.concept_df.to_artifacts())

        artifact_content = args.artifact[ArtifactKeys.CONTENT]
        direct_match_content = {artifact_content[match["start_loc"]:match["end_loc"]] for match in state.direct_matches}

        prompt_builders, prompts = self.create_prompts(entities, concepts, args.llm_manager, direct_match_content)
        entity_predictions = self.generate_predictions(prompts, prompt_builders, args.llm_manager)
        predicted_links = self.create_predicted_links(entities, entity_predictions, direct_match_content)

        concept_artifact_ids = set([a[ArtifactKeys.ID] for a in concepts])
        predicted_links = [m for m in predicted_links if
                           m[TraceKeys.TARGET] in concept_artifact_ids]  # remove links with erroneous concept ids
        state.predicted_matches = predicted_links

    @staticmethod
    def create_prompts(entities: List[Artifact], concepts: List[Artifact], llm_manager: AbstractLLMManager,
                       direct_match_content: Set[str]):
        """
        Creates matching prompt for each entity.
        :param entities: Entity artifacts matched against concepts.
        :param concepts: Concept artifacts used to match entities against.
        :param llm_manager: LLM manager used to make predictiosn.
        :param direct_match_content: Contains entities that have already been matched in the direct concept matching step.
        :return: Prompts builders used for parsing output and prompts built for each entity.
        """
        prompt_builders = []
        prompts = []
        for entity_artifact in entities:
            if entity_artifact[ArtifactKeys.ID] in direct_match_content:
                continue
            concept_prompt = MultiArtifactPrompt("# PROJECT ARTIFACTS", build_method=MultiArtifactPrompt.BuildMethod.XML)
            artifact_prompt = ArtifactPrompt(prompt_start=ENTITY_MATCHING_INSTRUCTIONS + NEW_LINE)
            response_format = ENTITY_MATCHING_RESPONSE_FORMAT.format(EntityMatchingStep.create_example_xml("ARTIFACT_ID"))
            # `referenced` will make the model speculate about potential matches, using cite
            instructions_prompt = Prompt(value=NEW_LINE, prompt_args=PromptArgs(prompt_id=EntityMatchingStep.PROMPT_ID),
                                         response_manager=PromptResponseManager(response_tag=EntityMatchingStep.MATCH_TAG,
                                                                                response_instructions_format=response_format))
            prompt_builder = PromptBuilder(prompts=[concept_prompt, artifact_prompt, instructions_prompt])
            prompt = prompt_builder.build(llm_manager.prompt_args, artifacts=concepts, artifact=entity_artifact)[PromptKeys.PROMPT]
            prompts.append(prompt)
            prompt_builders.append(prompt_builder)
        return prompt_builders, prompts

    @staticmethod
    def generate_predictions(prompts, prompt_builders, llm_manager: AbstractLLMManager):
        """
        Generates predictions for each prompt.
        :param prompts:
        :param prompt_builders:
        :param llm_manager:
        :return:
        """
        output = LLMTrainer.predict_from_prompts(
            llm_manager,
            message_prompts=prompts,
            prompt_builders=prompt_builders
        )
        entity_predictions = [prediction[EntityMatchingStep.PROMPT_ID] for prediction, pb in zip(output.predictions, prompt_builders)]
        return entity_predictions

    @staticmethod
    def create_predicted_links(entities: List[Artifact], entity_predictions: List[Dict],
                               direct_match_content: Set[str]) -> List[Trace]:
        """
        Parses model predictions into links between entities and concepts.
        :param entities: The entities corresponding to each prediction.
        :param entity_predictions: List of predicted concepts for each entity.
        :param direct_match_content: Contains entities that have already been matched in the direct concept matching step.
        :return: List of trace links from entities to concepts.
        """
        predicted_links = []
        entity_predictions = iter(entity_predictions)
        for entity_artifact in entities:
            if entity_artifact[ArtifactKeys.ID] in direct_match_content:
                continue
            entity_response = next(entity_predictions)
            seen_ids = set()
            entity_matches = entity_response[EntityMatchingStep.MATCH_TAG]
            for matched_concept in entity_matches:
                matched_entity = entity_artifact[ArtifactKeys.ID]
                if matched_concept in seen_ids:
                    continue
                match_trace = Trace(source=matched_entity, target=matched_concept)
                predicted_links.append(match_trace)
                seen_ids.add(matched_concept)
        return predicted_links

    @staticmethod
    def create_example_xml(target_text: str) -> str:
        """
        Creates example of how to enclose each match.
        :param target_text: The text inside of the xml.
        :return: String representation.
        """
        return PromptUtil.create_xml(EntityMatchingStep.MATCH_TAG, target_text)

    @staticmethod
    def strip_artifact_bodies(artifacts: List[Artifact]):
        """
        Removes lingering whitespace in artifact body.
        :param artifacts: The artifact to strip.
        :return: List of artifacts.
        """
        for a in artifacts:
            a[ArtifactKeys.CONTENT] = a[ArtifactKeys.CONTENT].strip()
        return artifacts
