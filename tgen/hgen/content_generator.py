import uuid
from typing import Union, Dict, List, Optional

from tgen.common.constants.deliminator_constants import COMMA, NEW_LINE
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
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
    SOURCE_TAG_ID = "source"
    TARGET_TAG_ID = "target"

    def __init__(self, args: HGenArgs, state: HGenState):
        """
        Handles content generation for HGen given the current args and state.
        :param args: The arguments to HGen.
        :param state: The current state of HGen.
        """
        self.args = args
        self.state = state

    def generate_content(self, source_dataset: PromptDataset, prompt_builder: PromptBuilder,
                         generations_filename: str = None) -> List[Dict]:
        """
        Generates content for a given dataset by using the prompt builder to create prompts for the LLM.
        :param source_dataset: The dataset to use to create documentation for.
        :param prompt_builder: The builder to use to construct the prompt for the LLM.
        :param generations_filename: The filename to save the generations to.
        :return: The model's parsed generations.
        """
        task_prompt = prompt_builder.get_prompt(-1)
        prompt_builder.format_prompts_with_var(source_type=self.args.source_type, target_type=self.args.target_type)

        export_path = FileUtil.safely_join_paths(self.state.export_dir, generations_filename)
        generated_artifacts_tag, links_tag = task_prompt.response_manager.get_all_tag_ids()
        generations = HGenUtil.get_predictions(prompt_builder, hgen_args=self.args, prediction_step=PredictionStep.GENERATION,
                                               dataset=source_dataset, response_prompt_ids={task_prompt.id},
                                               tags_for_response={generated_artifacts_tag}, return_first=False,
                                               export_path=export_path)
        return generations

    def create_prompt_builder(self, base_intro_prompt: SupportedPrompts, base_task_prompt: SupportedPrompts,
                              source_type: str, cluster2artifacts: Dict[str, List] = None,
                              format_variables: Dict[str, List] = None) -> PromptBuilder:
        """
        Creates the prompt builder for the generations using the provided prompts and variables.
        :param base_intro_prompt: Will be used to introduce the problem at the start of the prompt.
        :param base_task_prompt: Will be used to provide the main task to the LLM at the end of the prompt.
        :param cluster2artifacts: Maps cluster id to the list of artifacts in that cluster.
        :param source_type: The source type contained in the dataset that will be used to generate the content.
        :param format_variables: Any variables to give the prompt builder to dynamically format.
        :return:
        """
        task_prompt = self._create_generations_task_prompt(base_task_prompt.value)
        artifact_prompt = self._create_source_artifact_prompt(source_type, cluster2artifacts)
        prompt_builder = self._get_prompt_builder_for_generation(task_prompt, base_intro_prompt.value,
                                                                 artifact_prompt, format_variables)
        return prompt_builder

    def _create_generations_task_prompt(self, task_prompt: QuestionnairePrompt) -> QuestionnairePrompt:
        """
        Creates the prompt used for the primary creation task
        :param task_prompt: The main prompt being used to prompt the model to generate artifacts.
        :return: The prompt used for the primary creation task
        """
        task_prompt.id = self.TASK_PROMPT_ID
        target_type_tag = HGenUtil.convert_spaces_to_dashes(self.args.target_type)
        source_type_tag = HGenUtil.convert_spaces_to_dashes(self.args.source_type)
        task_prompt.response_manager = PromptResponseManager(
            response_instructions_format=f"Enclose each {self.args.target_type} in "
                                         "{target}. ",
            expected_responses={self.SOURCE_TAG_ID: set(self.state.source_dataset.artifact_df.index)},
            id2tag={self.TARGET_TAG_ID: target_type_tag,
                    self.SOURCE_TAG_ID: source_type_tag},
            response_tag={target_type_tag: [source_type_tag]},
            value_formatter=lambda tag, val: self._format_generations(tag, val))
        task_prompt.format_value(format=self.state.format_of_artifacts, description=self.state.description_of_artifact)
        return task_prompt

    def _get_prompt_builder_for_generation(self, task_prompt: QuestionnairePrompt, base_prompt: Prompt,
                                           artifact_prompt: MultiArtifactPrompt, format_variables: Dict = None) -> PromptBuilder:
        """
        Gets the prompt builder used for the generations.
        :param task_prompt: The questionnaire prompt given to the model to produce the generations.
        :param base_prompt: The main prompt that starts the prompt.
        :param artifact_prompt: The prompt that contains the source artifacts.
        :param format_variables: Any variables to give the prompt builder to dynamically format.
        :return: The prompt builder used for the generations
        """

        if isinstance(task_prompt, QuestionnairePrompt):
            task_prompt.use_multi_step_task_instructions = True

        prompts = [base_prompt, artifact_prompt, task_prompt]
        prompt_builder = PromptBuilder(prompts)

        if format_variables:
            prompt_builder.format_variables = format_variables

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
    def _create_source_artifact_prompt(source_type: str, id_to_context_artifacts: Dict[str, List] = None,
                                       build_method: MultiArtifactPrompt.BuildMethod = MultiArtifactPrompt.BuildMethod.XML,
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
