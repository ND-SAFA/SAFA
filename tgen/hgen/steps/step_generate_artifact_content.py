from typing import Any, Dict, List, Set, Tuple

from common_resources.tools.constants.symbol_constants import EMPTY_STRING, NEW_LINE, TAB
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.content_generator import ContentGenerator
from tgen.hgen.common.special_doc_types import DocTypeConstraints
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.supported_hgen_doc_type_prompts import SupportedHGenDocPrompts
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
            else SupportedHGenDocPrompts.get_prompt_by_type(args.target_type)

        dataset = state.cluster_dataset if state.cluster_dataset is not None else state.source_dataset

        format_variables = {}
        if state.cluster2artifacts:
            n_targets = ContentGenerator.calculate_number_of_targets_per_cluster(dataset.artifact_df.index,
                                                                                 state.get_cluster2artifacts(),
                                                                                 state.cluster2cohesion,
                                                                                 state.source_dataset,
                                                                                 is_first_layer=args.is_first_layer)
            format_variables.update({"n_targets": n_targets})

        content_generator = ContentGenerator(args, state, dataset)
        context_mapping = state.original_dataset.create_dependency_mapping(include_parents=True) \
            if state.original_dataset.trace_dataset and args.check_target_type_constraints(
            DocTypeConstraints.USE_SOURCE_CONTEXT) else {}
        prompt_builder = content_generator.create_prompt_builder(SupportedPrompts.HGEN_GENERATION,
                                                                 base_task_prompt,
                                                                 args.source_type, state.get_cluster2artifacts(),
                                                                 context_mapping=context_mapping,
                                                                 format_variables=format_variables, include_summary=False)

        if args.seed_layer_id and args.include_seed_in_prompt:
            self._add_seeds_to_prompt(dataset, prompt_builder, state)

        generations = content_generator.generate_content(prompt_builder, generations_filename=self.GENERATION_FILENAME)
        cluster_ids = state.get_cluster_ids() if state.cluster_dataset else []
        generations2sources, cluster2generation = content_generator.map_generations_to_predicted_sources(generations,
                                                                                                         cluster_ids=cluster_ids)
        state.generations2sources = generations2sources
        state.cluster2generations = cluster2generation

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
    def _map_generations_to_predicted_sources(generations: List, source_tag_id: str, target_tag_id: str,
                                              state: HGenState) -> Tuple[Dict[str, Set[str]], Dict[Any, str]]:
        """
        Creates a mapping of the generated artifact to a list of the predicted links to it and the source artifacts
        :param generations: The predictions from the LLM
        :param source_tag_id: The id of the predicted sources tag
        :param target_tag_id: The id of the generated target artifact tag
        :param state: The current state of the hierarchy generator
        :return: A mapping of the generated artifact to a list of the predicted links to it and the source artifacts
        """
        generations2sources = {}
        cluster2generations = {cluster_id: [] for cluster_id in state.get_cluster_ids()} if state.cluster_dataset else {}
        cluster_ids = state.get_cluster_ids() if state.cluster_dataset is not None else []
        n_failed = 0
        for i, generations4cluster in enumerate(generations):
            for generation in generations4cluster:
                try:
                    target = generation[target_tag_id][0]
                    sources = set(generation[source_tag_id][0]) if len(generation[source_tag_id]) > 0 else set()
                    generations2sources[target] = sources
                    if cluster_ids:
                        cluster2generations[cluster_ids[i]].append(target)
                except Exception:
                    n_failed += 1
                    logger.exception("A generation failed")
        if n_failed > 0:
            assert n_failed < len(generations), "All generations have failed."
            logger.warning(f"{n_failed} generations failed. ")
        return generations2sources, cluster2generations
