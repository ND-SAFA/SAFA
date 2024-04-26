from typing import List

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys
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
        entity_artifacts = self.strip_artifact_bodies(state.entity_df.to_artifacts())
        concept_artifacts = self.strip_artifact_bodies(args.concept_df.to_artifacts())

        prompt_builders = []
        prompts = []
        for entity_artifact in entity_artifacts:
            concept_prompt = MultiArtifactPrompt("# PROJECT ARTIFACTS", build_method=MultiArtifactPrompt.BuildMethod.XML)
            artifact_prompt = ArtifactPrompt(prompt_start="").build(artifact=entity_artifact)
            response_format = f"Record each referenced entity like so {self.create_example_xml('ARTIFACT_ID')}"
            # `referenced` will make the model speculate about potential matches, using cite
            instructions_prompt = Prompt(
                f"List the artifacts that are cited in the text below. If none exists, just say 'NA'.\n\n'{artifact_prompt}'\n\n",
                response_manager=PromptResponseManager(response_tag=self.MATCH_TAG,
                                                       response_instructions_format=response_format)
            )
            prompt_builder = PromptBuilder(prompts=[concept_prompt, instructions_prompt])
            prompt = prompt_builder.build(args.llm_manager.prompt_args, artifacts=concept_artifacts)[PromptKeys.PROMPT]
            prompts.append(prompt)
            prompt_builders.append(prompt_builder)

        output = LLMTrainer.predict_from_prompts(
            args.llm_manager,
            prompts=prompts,
            prompt_builders=prompt_builders
        )

        matches = []
        concept_artifact_ids = set([a[ArtifactKeys.ID] for a in concept_artifacts])

        for entity_artifact, entity_prediction, entity_prompt_builder in zip(entity_artifacts, output.predictions, prompt_builders):
            seen_ids = set()
            entity_response = entity_prediction[entity_prompt_builder.prompts[-1].id]
            entity_matches = entity_response[self.MATCH_TAG]
            for matched_concept in entity_matches:
                matched_entity = entity_artifact[ArtifactKeys.ID]
                if matched_concept not in concept_artifact_ids or matched_concept in seen_ids:
                    continue
                match_trace = Trace(source=matched_entity, target=matched_concept)
                matches.append(match_trace)
                seen_ids.add(matched_concept)
            print(len(matches))
        state.predicted_matches = matches

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
