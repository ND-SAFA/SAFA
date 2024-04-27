from typing import Dict, List

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
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
from tgen.prompts.prompt_builder import PromptBuilder
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
        entities: List[Artifact] = self.strip_artifact_bodies(state.entity_df.to_artifacts())
        concepts: List[Artifact] = self.strip_artifact_bodies(args.concept_df.to_artifacts())

        prompt_builders, prompts = self.create_prompts(entities, concepts, args.llm_manager)
        entity_predictions = self.generate_predictions(prompts, prompt_builders, args.llm_manager)
        predicted_links = self.create_predicted_links(entities, entity_predictions)

        concept_artifact_ids = set([a[ArtifactKeys.ID] for a in concepts])
        predicted_links = [m for m in predicted_links if
                           m[TraceKeys.TARGET] in concept_artifact_ids]  # remove links with erroneous concept ids
        state.predicted_matches = predicted_links

    @staticmethod
    def create_prompts(entities: List[Artifact], concepts: List[Artifact], llm_manager: AbstractLLMManager):
        """
        Creates matching prompt for each entity.
        :param entities: Entity artifacts matched against concepts.
        :param concepts: Concept artifacts used to match entities against.
        :param llm_manager: LLM manager used to make predictiosn.
        :return: Prompts builders used for parsing output and prompts built for each entity.
        """
        prompt_builders = []
        prompts = []
        for entity_artifact in entities:
            concept_prompt = MultiArtifactPrompt("# PROJECT ARTIFACTS", build_method=MultiArtifactPrompt.BuildMethod.XML)
            artifact_prompt = ArtifactPrompt(prompt_start="").build(artifact=entity_artifact)
            response_format = f"Record each referenced entity like so {EntityMatching.create_example_xml('ARTIFACT_ID')}"
            # `referenced` will make the model speculate about potential matches, using cite
            instructions_prompt = Prompt(
                f"List the artifacts that are cited in the text below. If none exists, just say 'NA'.\n\n'{artifact_prompt}'\n\n",
                response_manager=PromptResponseManager(response_tag=EntityMatching.MATCH_TAG,
                                                       response_instructions_format=response_format)
            )
            prompt_builder = PromptBuilder(prompts=[concept_prompt, instructions_prompt])
            prompt = prompt_builder.build(llm_manager.prompt_args, artifacts=concepts)[PromptKeys.PROMPT]
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
            prompts=prompts,
            prompt_builders=prompt_builders
        )
        entity_predictions = [prediction[pb.prompts[-1].id] for prediction, pb in zip(output.predictions, prompt_builders)]
        return entity_predictions

    @staticmethod
    def create_predicted_links(entities: List[Artifact], entity_predictions: List[Dict]) -> List[Trace]:
        """
        Parses model predictions into links between entities and concepts.
        :param entities: The entities corresponding to each prediction.
        :param entity_predictions: List of predicted concepts for each entity.
        :return: List of trace links from entities to concepts.
        """
        predicted_links = []
        for entity_artifact, entity_response in zip(entities, entity_predictions):
            seen_ids = set()
            entity_matches = entity_response[EntityMatching.MATCH_TAG]
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
        :return: String representation.
        """
        return (
            f"<{EntityMatching.MATCH_TAG}>{target_text}</{EntityMatching.MATCH_TAG}>"
        )

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
