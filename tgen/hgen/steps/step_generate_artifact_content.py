import os
import uuid
from typing import Any, Dict, List, Set, Tuple

from tgen.common.constants.deliminator_constants import COMMA, NEW_LINE
from tgen.common.constants.hgen_constants import TEMPERATURE_ON_RERUNS, DEFAULT_BRANCHING_FACTOR
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.hgen_util import HGenUtil
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.hgen.hgen_state import HGenState
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class GenerateArtifactContentStep(AbstractPipelineStep[HGenArgs, HGenState]):
    TASK_PROMPT_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'seed'))

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates the content for the new artifacts.
        :param args: HGEN configuration.
        :param state: The current state of the HGEN run.
        :return: None
        """
        logger.info(f"Generating {args.target_type}s\n")

        filename = "artifact_gen_response"
        if state.n_generations > 0:
            filename = f"{filename}_{state.n_generations}"
            args.hgen_llm_manager_best.llm_args.temperature = TEMPERATURE_ON_RERUNS
        export_path = FileUtil.safely_join_paths(state.export_dir, filename)

        task_prompt, target_tag_id, source_tag_id = self._create_task_prompt(args, state)
        generated_artifacts_tag, links_tag = task_prompt.response_manager.get_all_tag_ids()

        dataset = state.cluster_dataset if state.cluster_dataset is not None else state.source_dataset

        prompt_builder = HGenUtil.get_prompt_builder_for_generation(args, task_prompt,
                                                                    combine_summary_and_task_prompts=True,
                                                                    id_to_context_artifacts=state.id_to_cluster_artifacts)
        if state.id_to_cluster_artifacts:
            n_targets = self._calculate_number_of_targets_per_cluster(dataset.artifact_df.index, state)
            prompt_builder.format_variables = {"n_targets": n_targets}
        if state.project_summary:
            overview_of_system_prompt = Prompt(f"{PromptUtil.as_markdown_header('Overview of System:')}"
                                               f"{NEW_LINE}{state.project_summary.to_string()}", allow_formatting=False)
            prompt_builder.add_prompt(overview_of_system_prompt, 1)

        generation_predictions = HGenUtil.get_predictions(prompt_builder, hgen_args=args, prediction_step=PredictionStep.GENERATION,
                                                          dataset=dataset, response_prompt_ids={task_prompt.id},
                                                          tags_for_response={generated_artifacts_tag}, return_first=False,
                                                          export_path=export_path)
        state.generation_predictions, state.cluster2generation = self._map_generations_to_predicted_sources(generation_predictions,
                                                                                                            source_tag_id,
                                                                                                            target_tag_id, state)
        state.n_generations += 1

    @staticmethod
    def _calculate_number_of_targets_per_cluster(artifact_ids: List, state: HGenState,
                                                 branching_factor: int = DEFAULT_BRANCHING_FACTOR) -> List[int]:
        """
        Calculates the expected number of targets for each cluster based on the number of artifacts in each cluster
        :param artifact_ids: The ids of the artifact representing each cluster
        :param state: The current HGEN state
        :param branching_factor: Determines the percentage of target artifacts per source artifacts
        :return: A list of the expected number of target artifacts for each cluster
        """
        n_targets = [GenerateArtifactContentStep._calculate_proportion_of_artifacts(len(state.id_to_cluster_artifacts[i]),
                                                                                    branching_factor) for i in artifact_ids]
        return n_targets

    @staticmethod
    def _calculate_proportion_of_artifacts(n_artifacts: int,  branching_factor: int) -> int:
        """
        Calculates how many artifacts would be equal to a proportion of the total based on a given branching factor
        :param n_artifacts: Total number of artifacts
        :param branching_factor: Determines the proportion (e.g. branching_factor = 2 would be 50% of artifacts)
        :return: The number of artifacts equal to a proportion of the total
        """
        return max(round(n_artifacts * (1 / branching_factor)), 1)

    @staticmethod
    def _map_generations_to_predicted_sources(generation_predictions: List, source_tag_id: str, target_tag_id: str,
                                              state: HGenState) -> Tuple[Dict[str, Set[str]], Dict[Any, str]]:
        """
        Creates a mapping of the generated artifact to a list of the predicted links to it and the source artifacts
        :param generation_predictions: The predictions from the LLM
        :param source_tag_id: The id of the predicted sources tag
        :param target_tag_id: The id of the generated target artifact tag
        :param state: The current state of the hierarchy generator
        :return: A mapping of the generated artifact to a list of the predicted links to it and the source artifacts
        """
        generated_artifact_to_predicted_sources = {}
        cluster2generations = {cluster_id: [] for cluster_id in
                               state.cluster_dataset.artifact_df.index} if state.cluster_dataset else {}
        cluster_ids = list(cluster2generations.keys()) if state.cluster_dataset is not None else []
        for i, pred in enumerate(generation_predictions):
            for p in pred:
                generation = p[target_tag_id][0]
                sources = set(p[source_tag_id][0]) if len(p[source_tag_id]) > 0 else set()
                generated_artifact_to_predicted_sources[generation] = sources
                if cluster_ids:
                    cluster2generations[cluster_ids[i]].append(generation)
        return generated_artifact_to_predicted_sources, cluster2generations

    def _create_task_prompt(self, args: HGenArgs, state: HGenState) -> Tuple[QuestionnairePrompt, str, str]:
        """
        Creates the prompt used for the primary creation task
        :param args: The args to the hierarchy generator
        :param state: The current state of the hierarchy generator
        :return: The prompt used for the primary creation task
        """
        task_prompt = SupportedPrompts.HGEN_GENERATION_QUESTIONNAIRE.value if not state.id_to_cluster_artifacts \
            else SupportedPrompts.HGEN_CLUSTERING_QUESTIONNAIRE.value
        task_prompt.id = self.TASK_PROMPT_ID
        target_type_tag, target_tag_id = HGenUtil.convert_spaces_to_dashes(args.target_type), "target"
        source_type_tag, source_tag_id = HGenUtil.convert_spaces_to_dashes(args.source_type), "source"
        task_prompt.response_manager = PromptResponseManager(
            response_instructions_format=f"Enclose each {args.target_type}s in "
                                         "{target}. ",
            expected_responses={source_tag_id: set(state.source_dataset.artifact_df.index)},
            value_formatter=lambda tag, val: [v.strip() for v in val.split(COMMA)] if tag == source_tag_id
            else val.strip().strip(NEW_LINE),
            id2tag={target_tag_id: target_type_tag,
                    source_tag_id: source_type_tag},
            response_tag={target_type_tag: [source_type_tag]})
        task_prompt.format_value(format=state.format_of_artifacts, description=state.description_of_artifact)
        return task_prompt, target_tag_id, source_tag_id
