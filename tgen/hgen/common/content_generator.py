import math
import uuid
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from tgen.common.constants.deliminator_constants import COMMA, EMPTY_STRING, NEW_LINE
from tgen.common.constants.hgen_constants import DEFAULT_REDUCTION_PERCENTAGE_GENERATIONS
from tgen.common.logging.logger_manager import logger
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.hgen_util import HGenUtil
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.hgen.hgen_state import HGenState
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class ContentGenerator:
    TASK_PROMPT_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'seed'))
    SOURCE_TAG_ID = "ids"
    TARGET_TAG_ID = "target"

    def __init__(self, args: HGenArgs, state: HGenState, source_dataset: PromptDataset):
        """
        Handles content generation for HGen given the current args and state.
        :param args: The arguments to HGen.
        :param state: The current state of HGen.
        :param source_dataset: The dataset to use to create documentation for.
        """
        self.args = args
        self.state = state
        self.source_dataset = source_dataset

    def generate_content(self, prompt_builder: PromptBuilder, generations_filename: str = None,
                         return_first: bool = False) -> List:
        """
        Generates content for a given dataset by using the prompt builder to create prompts for the LLM.
        :param prompt_builder: The builder to use to construct the prompt for the LLM.
        :param generations_filename: The filename to save the generations to.
        :param return_first: If True, returns the first item from each list of parsed tags (often there is only one per tag)
        :return: The model's parsed generations.
        """
        task_prompt = prompt_builder.get_prompt(-1)
        prompt_builder.format_prompts_with_var(source_type=self.args.source_type, target_type=self.args.target_type)

        export_path = FileUtil.safely_join_paths(self.state.export_dir, generations_filename)
        generated_artifacts_tag = task_prompt.response_manager.get_all_tag_ids()[0]
        generations = HGenUtil.get_predictions(prompt_builder, hgen_args=self.args, prediction_step=PredictionStep.GENERATION,
                                               dataset=self.source_dataset, response_prompt_ids={task_prompt.id},
                                               tags_for_response={generated_artifacts_tag}, return_first=return_first,
                                               export_path=export_path)
        return generations

    def create_prompt_builder(self, base_intro_prompt: SupportedPrompts, base_task_prompt: SupportedPrompts,
                              source_type: str, cluster2artifacts: Dict[str, List] = None,
                              format_variables: Dict[str, List] = None,
                              additional_task_response_instructions: str = EMPTY_STRING,
                              artifact_prompt_build_method: MultiArtifactPrompt.BuildMethod = MultiArtifactPrompt.BuildMethod.XML,
                              include_summary: bool = True) -> PromptBuilder:
        """
        Creates the prompt builder for the generations using the provided prompts and variables.
        :param base_intro_prompt: Will be used to introduce the problem at the start of the prompt.
        :param base_task_prompt: Will be used to provide the main task to the LLM at the end of the prompt.
        :param cluster2artifacts: Maps cluster id to the list of artifacts in that cluster.
        :param source_type: The source type contained in the dataset that will be used to generate the content.
        :param format_variables: Any variables to give the prompt builder to dynamically format.
        :param additional_task_response_instructions: Any additional instructions to include on how the model should format its res.
        :param include_summary: If True, includes summary in prompt.
        :param artifact_prompt_build_method: How to construct the source artifacts in prompt.
        :return: The prompt builder for the generations using the provided prompts and variables.
        """
        task_prompt = self._create_generations_task_prompt(base_task_prompt.value, cluster2artifacts,
                                                           additional_response_instructions=additional_task_response_instructions)
        artifact_prompt = self.create_source_artifact_prompt(source_type, cluster2artifacts,
                                                             build_method=artifact_prompt_build_method) \
            if artifact_prompt_build_method else None

        prompt_builder = self._get_prompt_builder_for_generation(
            task_prompt, base_intro_prompt.value, artifact_prompt, format_variables, include_summary)
        return prompt_builder

    def map_generations_to_predicted_sources(self, generations: List,
                                             cluster_ids: List = None) -> Tuple[Dict[str, Set[str]], Dict[Any, List[str]]]:
        """
        Creates a mapping of the generated artifact to a list of the predicted links to it and the source artifacts
        :param generations: The predictions from the LLM
        :param cluster_ids: The list of cluster ids used to create generations.
        :return: A mapping of the generated artifact to a list of the predicted links to it and the source artifacts
        """
        generations2sources = {}
        cluster2generations = {cluster_id: [] for cluster_id in cluster_ids} if cluster_ids else {}
        for i, generations4cluster in enumerate(generations):
            for generation in generations4cluster:
                try:
                    target = generation[self.TARGET_TAG_ID][0]
                    sources = set(generation[self.SOURCE_TAG_ID][0]) if len(generation[self.SOURCE_TAG_ID]) > 0 else set()
                    generations2sources[target] = sources
                    if cluster_ids:
                        cluster2generations[cluster_ids[i]].append(target)
                except Exception:
                    logger.exception("A generation failed")
        return generations2sources, cluster2generations

    @staticmethod
    def calculate_number_of_targets_per_cluster(artifact_ids: List, cluster2artifacts: Dict[str, List[EnumDict]],
                                                cluster2cohesion: Dict[str, float], source_dataset: PromptDataset) -> List[int]:
        """
        Calculates the expected number of targets for each cluster based on the number of artifacts in each cluster
        :param artifact_ids: The ids of the artifact representing each cluster
        :param cluster2artifacts: Dictionary mapping cluster id to the artifacts in that cluster.
        :param cluster2cohesion: Dictionary mapping cluster id to the cohesion of the cluster.
        :param source_dataset: Contains all source artifacts.
        :return: A list of the expected number of target artifacts for each cluster
        """
        file_lengths = [len(content.splitlines()) for content in source_dataset.artifact_df[ArtifactKeys.CONTENT]]
        avg_file_size = sum(file_lengths) / len(file_lengths)
        cluster2artifacts = cluster2artifacts
        cluster2cohesion = {c_id: cohesion if cohesion else 1 for c_id, cohesion in cluster2cohesion.items()}
        max_cohesion = max(cluster2cohesion.values())
        cluster2retention_percentage = {cluster_id: ContentGenerator.convert_cohesion_to_reduction_percentage(cohesion, max_cohesion)
                                        for cluster_id, cohesion in cluster2cohesion.items()}
        retention_percentage_delta = max(0.75 - max(cluster2retention_percentage.values()), 0)
        cluster2retention_percentage = {cluster_id: rp + retention_percentage_delta
                                        for cluster_id, rp in cluster2retention_percentage.items()}
        n_targets = [ContentGenerator._calculate_n_targets_for_cluster(artifacts=cluster2artifacts[i],
                                                                       avg_file_size=avg_file_size,
                                                                       retention_percentage=cluster2retention_percentage[i])
                     for i in artifact_ids]
        return n_targets

    @staticmethod
    def convert_cohesion_to_reduction_percentage(cohesion: float, max_cohesion: float) -> float:
        return 1 - math.log(cohesion + 1) / math.log(max_cohesion + 1)

    @staticmethod
    def _calculate_n_targets_for_cluster(artifacts: List[EnumDict], avg_file_size: float,
                                         retention_percentage: float = DEFAULT_REDUCTION_PERCENTAGE_GENERATIONS, ) -> int:
        """
        Calculates how many artifacts would be equal to a proportion of the total based on a given branching factor
        :param artifacts: The artifacts in the cluster.
        :param avg_file_size: The average size of files for the project.
        :param retention_percentage: Determines the proportion of source artifacts to use for # of generations
        :return: The number of artifacts equal to a proportion of the total
        """
        debugging = [a[ArtifactKeys.ID] for a in artifacts]
        length_of_artifacts = sum([len(artifact[ArtifactKeys.CONTENT].splitlines()) for artifact in artifacts])
        # adjust for amount of content
        n_artifacts = (length_of_artifacts / avg_file_size)
        n_artifacts = min(max(n_artifacts, math.ceil(len(artifacts) / 2)), len(artifacts) + 1)

        # adjust for cohesion
        min_acceptable = max(math.ceil(len(artifacts) / 2), 1)
        max_acceptable = max(len(artifacts) - 1, 1)
        n_targets = max(round(n_artifacts * retention_percentage), min_acceptable)
        return min(round(n_targets), max_acceptable)

    def _create_generations_task_prompt(self, task_prompt: QuestionnairePrompt, cluster2artifacts: Dict[str, List] = None,
                                        additional_response_instructions: str = EMPTY_STRING) -> QuestionnairePrompt:
        """
        Creates the prompt used for the primary creation task
        :param task_prompt: The main prompt being used to prompt the model to generate artifacts.
        :param cluster2artifacts: Maps cluster id to the list of artifacts in that cluster.
        :param additional_response_instructions: If provided, will be used to instruct the model how to format the response.
        :return: The prompt used for the primary creation task
        """
        task_prompt.id = self.TASK_PROMPT_ID
        if not task_prompt.response_manager.response_tag:
            target_type_tag = HGenUtil.convert_spaces_to_dashes(self.args.target_type)
            response_instructions_format = f"Enclose each final {self.args.target_type} in " \
                                           "{target}. " + additional_response_instructions
            sources = {a[ArtifactKeys.ID] for artifacts in cluster2artifacts.values() for a in artifacts} \
                if cluster2artifacts else set(self.state.source_dataset.artifact_df.index)
            task_prompt.response_manager = PromptResponseManager(
                response_instructions_format=response_instructions_format,
                expected_responses={self.SOURCE_TAG_ID: sources},
                id2tag={self.TARGET_TAG_ID: target_type_tag},
                response_tag={target_type_tag: [self.SOURCE_TAG_ID]},
                value_formatter=lambda tag, val: self._format_generations(tag, val))
        task_prompt.format_value(format=self.state.format_of_artifacts, description=self.state.description_of_artifact,
                                 example=self.state.example_artifact)
        return task_prompt

    def _get_prompt_builder_for_generation(self, task_prompt: QuestionnairePrompt, base_prompt: Prompt,
                                           artifact_prompt: MultiArtifactPrompt, format_variables: Dict = None,
                                           include_summary: bool = True) -> PromptBuilder:
        """
        Gets the prompt builder used for the generations.
        :param task_prompt: The questionnaire prompt given to the model to produce the generations.
        :param base_prompt: The main prompt that starts the prompt.
        :param artifact_prompt: The prompt that contains the source artifacts.
        :param format_variables: Any variables to give the prompt builder to dynamically format.
        :param include_summary: If True, includes summary in prompt.
        :return: The prompt builder used for the generations
        """

        if isinstance(task_prompt, QuestionnairePrompt):
            task_prompt.use_multi_step_task_instructions = True

        prompts = [base_prompt, artifact_prompt, task_prompt]
        prompt_builder = PromptBuilder(prompts)

        if format_variables:
            prompt_builder.format_variables = format_variables

        if include_summary:
            self._add_project_summary_to_prompt(prompt_builder)

        return prompt_builder

    def _add_project_summary_to_prompt(self, prompt_builder: PromptBuilder) -> None:
        """
        Adds the project summary to the prompt builder for the LLM to use.
        :param prompt_builder: The prompt builder being used in the generations.
        :return: None
        """
        if self.state.project_summary:
            project_overview = self.state.project_summary.to_string(self.args.content_generation_project_summary_sections)
            overview_of_system_prompt = Prompt(f"\n{PromptUtil.as_markdown_header('Overview of System:')}"
                                               f"{NEW_LINE}{project_overview}", allow_formatting=False)
            prompt_builder.add_prompt(overview_of_system_prompt, 1)

    @staticmethod
    def create_source_artifact_prompt(source_type: str, id_to_context_artifacts: Dict[str, List] = None,
                                      build_method: MultiArtifactPrompt.BuildMethod = MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                      **multi_artifact_params) -> MultiArtifactPrompt:
        """
        Creates the prompt that will be used to supply the LLM with the source artifacts.
        :param source_type: The type of artifact that will be given to the LLM as sources.
        :param id_to_context_artifacts: Maps the id of the artifact in the provided dataset to the list of sources that are related.
        :param build_method: The method to use to format the artifacts.
        :param multi_artifact_params: Any additional params to the prompt.
        :return: The prompt that will be used to supply the LLM with the source artifacts.
        """
        artifact_prompt_kwargs = dict(prompt_prefix=PromptUtil.as_markdown_header(f"{source_type.upper()}S:"),
                                      build_method=build_method,
                                      include_ids=build_method == MultiArtifactPrompt.BuildMethod.XML,
                                      data_type=MultiArtifactPrompt.DataType.ARTIFACT,
                                      xml_tags={
                                          HGenUtil.convert_spaces_to_dashes(source_type.lower()): ["id",
                                                                                                   "description"]},
                                      **multi_artifact_params)
        artifact_prompt = ContextPrompt(id_to_context_artifacts=id_to_context_artifacts, **artifact_prompt_kwargs) \
            if id_to_context_artifacts else MultiArtifactPrompt(**artifact_prompt_kwargs)
        return artifact_prompt

    def _format_generations(self, tag: Optional[str], val: str) -> Union[List, str]:
        """
        Formats the responses from the LLM for the generations.
        :param tag: The response tag being parsed.
        :param val: The response value for the tag.
        :return: The formatted generations.
        """
        if tag == self.SOURCE_TAG_ID:
            return [self._format_generations(val=v, tag=None) for v in val.split(COMMA)]
        else:
            return PromptUtil.strip_new_lines_and_extra_space(val)
