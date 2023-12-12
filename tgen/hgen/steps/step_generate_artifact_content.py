from typing import Any, Dict, List, Set, Tuple

from tgen.common.constants.deliminator_constants import NEW_LINE, EMPTY_STRING, TAB
from tgen.common.constants.hgen_constants import DEFAULT_REDUCTION_PERCENTAGE_GENERATIONS
from tgen.common.constants.hgen_constants import DEFAULT_TOKEN_TO_TARGETS_RATIO
from tgen.common.logging.logger_manager import logger
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.content_generator import ContentGenerator
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.hgen.hgen_state import HGenState
from tgen.models.tokens.token_calculator import TokenCalculator
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class GenerateArtifactContentStep(AbstractPipelineStep[HGenArgs, HGenState]):
    GENERATION_FILENAME = "artifact_gen_response"

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates the content for the new artifacts.
        :param args: HGEN configuration.
        :param state: The current state of the HGEN run.
        :return: None
        """
        logger.info(f"Generating {args.target_type}s\n")

        base_task_prompt = SupportedPrompts.HGEN_GENERATION_QUESTIONNAIRE if not state.cluster2artifacts \
            else SupportedPrompts.HGEN_CLUSTERING_QUESTIONNAIRE

        dataset = state.cluster_dataset if state.cluster_dataset is not None else state.source_dataset

        format_variables = {}
        if state.cluster2artifacts:
            n_targets = self._calculate_number_of_targets_per_cluster(dataset.artifact_df.index, args, state)
            format_variables.update({"n_targets": n_targets})

        content_generator = ContentGenerator(args, state)
        prompt_builder = content_generator.create_prompt_builder(SupportedPrompts.HGEN_GENERATION, base_task_prompt,
                                                                 args.source_type, state.get_cluster2artifacts(), format_variables)

        if args.seed_layer_id:
            self._add_seeds_to_prompt(dataset, prompt_builder, state)

        generations = content_generator.generate_content(dataset, prompt_builder, generations_filename=self.GENERATION_FILENAME)
        generations2sources, cluster2generation = content_generator.map_generations_to_predicted_sources(generations)
        state.generations2sources = generations2sources
        state.cluster2generation = cluster2generation

    @staticmethod
    def _add_seeds_to_prompt(dataset: PromptDataset, prompt_builder: PromptBuilder, state: HGenState) -> None:
        """
        Adds the seeds to the prompt if they came from a real artifact layer so that they can ground the model's generations.
        :param dataset: The dataset made from the clusters/
        :param prompt_builder: The builder of the prompt for the generations.
        :param state: The current state of HGen.
        :return: None
        """
        seed_contents = [state.cluster_id2seeds.get(c_id, EMPTY_STRING).replace(NEW_LINE, f"{NEW_LINE}{TAB}")
                         for c_id in dataset.artifact_df.index]
        prompt_builder.add_prompt(SupportedPrompts.HGEN_SEED_PROMPT.value, -2)
        prompt_builder.format_variables.update({"seed_content": seed_contents})

    @staticmethod
    def _calculate_number_of_targets_per_cluster(artifact_ids: List, args: HGenArgs, state: HGenState) -> List[int]:
        """
        Calculates the expected number of targets for each cluster based on the number of artifacts in each cluster
        :param artifact_ids: The ids of the artifact representing each cluster
        :param args: Arguments to HGEN
        :param state: The current HGEN state
        :return: A list of the expected number of target artifacts for each cluster
        """
        cluster2artifacts = state.get_cluster2artifacts()
        n_targets = [GenerateArtifactContentStep._calculate_proportion_of_artifacts(len(cluster2artifacts[i]),
                                                                                    reduction_percentage=args.reduction_percentage)
                     for i in artifact_ids]
        return n_targets

    @staticmethod
    def _calculate_proportion_of_artifacts(n_artifacts: int,
                                           reduction_percentage: float = DEFAULT_REDUCTION_PERCENTAGE_GENERATIONS) -> int:
        """
        Calculates how many artifacts would be equal to a proportion of the total based on a given branching factor
        :param n_artifacts: Total number of artifacts
        :param reduction_percentage: Determines the proportion of source artifacts to use for # of generations
        :return: The number of artifacts equal to a proportion of the total
        """
        return max(round(n_artifacts * reduction_percentage), 1)

    @staticmethod
    def _calculate_proportion_of_tokens(artifacts: List, args: HGenArgs,
                                        token_to_target_ratio: float = DEFAULT_TOKEN_TO_TARGETS_RATIO) -> int:
        """
        Calculates how many artifacts to generate based on proportion of total artifact tokens
        :param artifacts: List of artifact in the given cluster
        :param args: The arguments to HGEN
        :param token_to_target_ratio: The token to target token ratio.
        :return: The number of artifacts equal to a proportion of the artifact tokens
        """
        model_name = args.llm_managers[PredictionStep.GENERATION.value].llm_args.model
        contents = [artifact[ArtifactKeys.CONTENT] for artifact in artifacts]
        token_counts = [TokenCalculator.estimate_num_tokens(content, model_name) for content in contents]
        n_artifacts_proportion = GenerateArtifactContentStep._calculate_proportion_of_artifacts(len(contents))
        n_artifacts_tokens = max(round(sum(token_counts) / token_to_target_ratio), n_artifacts_proportion)
        return n_artifacts_tokens


