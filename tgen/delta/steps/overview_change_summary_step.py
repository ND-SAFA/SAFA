from collections import OrderedDict
from typing import Any, Dict, List

from common_resources.tools.constants.symbol_constants import COMMA, EMPTY_STRING, NEW_LINE, SPACE
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.dataframe_util import DataFrameUtil
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.prompt_util import PromptUtil
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from tgen.delta.change_type import ChangeType
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.delta.delta_util import get_prediction_output
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class OverviewChangeSummaryStep(AbstractPipelineStep[DeltaArgs, DeltaState]):
    LAYER_ID = "diff"
    ARTIFACT_CONTENT = "{}" + NEW_LINE + "{}"
    UNKNOWN_CHANGE_TYPE_KEY = "other"
    IMPACT_TAG_ID: QuestionnairePrompt = SupportedPrompts.DIFF_SUMMARY_QUESTIONNAIRE.value.get_response_tags_for_prompt(-1)

    OVERVIEW_TITLE = "Overview"
    USER_LEVEL_SUMMARY_TITLE = "User-level Summary"
    CHANGE_DETAILS_TITLE = "Change Details"

    def _run(self, args: DeltaArgs, state: DeltaState) -> None:
        """
        Creates the complete summary of all changes made to the project
        :param args: The arguments for the delta summarizer
        :param state: The current state of the delta summarizer
        :return: None
        """
        logger.log_with_title("STEP 3 - Generating Complete Change Summary")
        artifact_df = self._create_diff_artifact_df(state)
        task_prompt: QuestionnairePrompt = SupportedPrompts.DELTA_CHANGE_SUMMARY_QUESTIONNAIRE.value

        output = self._get_output(args, state, artifact_df, task_prompt)
        state.change_summary_output = output

        low_level_summary = self._get_summary_from_output(state.change_summary_output, task_prompt, 1)
        user_level_summary = self._get_summary_from_output(state.change_summary_output, task_prompt, 2)
        state.overview_section = [PromptUtil.as_markdown_header(OverviewChangeSummaryStep.OVERVIEW_TITLE),
                                  low_level_summary,
                                  PromptUtil.as_markdown_header(OverviewChangeSummaryStep.USER_LEVEL_SUMMARY_TITLE),
                                  user_level_summary]

        change_types = self._create_change_type_mapping(state.change_summary_output, task_prompt)
        state.change_details_section = self._create_change_details_section(change_types)

    @staticmethod
    def _create_change_details_section(change_types: Dict[str, Dict[str, List]]) -> List[str]:
        """
        Add the change details section to the summary
        :param change_types: The dictionary containing changes for each change type
        :return: The list of all parts of the change details summary
        """
        change_details = [PromptUtil.as_markdown_header(OverviewChangeSummaryStep.CHANGE_DETAILS_TITLE)]
        for change_type, changes in change_types.items():
            if len(changes) < 1:
                continue
            change_details.append(PromptUtil.as_markdown_header(change_type.title(), level=2))
            for change, filenames in changes.items():
                change_details.append(PromptUtil.as_bullet_point(change))
                for filename in filenames:
                    change_details.append(PromptUtil.as_bullet_point(filename, level=2))
        return change_details

    def _create_change_type_mapping(self, change_summary_output: Dict, task_prompt: QuestionnairePrompt) -> Dict[str, Dict[str, List]]:
        """
        Creates a mapping of change type to the associated changes which are mapped to the affected filenames
        :param change_summary_output: The dictionary containing the models responses for the change summary
        :param task_prompt: The prompt used to create the output
        :return: A dictionary mapping change type to the associated changes which are mapped to the affected filenames
        """
        group_tag, filenames_tag, change_tag, type_tag = task_prompt.get_response_tags_for_prompt(0)
        groups = change_summary_output[group_tag]
        change_type_mapping = OrderedDict({ct.value.lower(): {} for ct in ChangeType.get_granular_change_type_categories()})
        change_type_mapping[self.UNKNOWN_CHANGE_TYPE_KEY] = {}
        for group in groups:
            filenames = group[filenames_tag][0]
            change = group[change_tag][0]
            change_type = group[type_tag][0]
            key = self._match_change_type(change_type, change_type_mapping)
            change_type_mapping[key][change.strip(NEW_LINE)] = filenames
        return change_type_mapping

    @staticmethod
    def _create_diff_artifact_df(state: DeltaState, include_impact: bool = False) -> ArtifactDataFrame:
        """
        Creates a dataframe of artifacts representing the diff summary for each changed file
        :param state: The current state of the delta summarizer
        :param include_impact: Whether to include the impact section of delta summarization.s
        :return: A dataframe of artifacts representing the diff summary for each changed file
        """
        artifacts = {}
        for filenames, diff_info in state.diff_summaries.items():
            content = NEW_LINE + \
                      EMPTY_STRING.join([OverviewChangeSummaryStep.ARTIFACT_CONTENT.format(name.upper(), val)
                                         for name, val in diff_info.items()
                                         if (name != OverviewChangeSummaryStep.IMPACT_TAG_ID or include_impact)])
            DataFrameUtil.append(artifacts, EnumDict({ArtifactKeys.ID: filenames,
                                                      ArtifactKeys.CONTENT: content,
                                                      ArtifactKeys.LAYER_ID: OverviewChangeSummaryStep.LAYER_ID}))
        artifact_df = ArtifactDataFrame(artifacts)
        return artifact_df

    @staticmethod
    def _get_output(args: DeltaArgs, state: DeltaState, artifact_df: ArtifactDataFrame, task_prompt: QuestionnairePrompt) -> Dict:
        """
        Gets the output for the model for creating the summary
        :param args: The arguments used for the delta summarizer
        :param state: The current state of the delta summarizer
        :param artifact_df: A dataframe containing the diff summary for each change
        :param task_prompt: The prompt used to generate the output
        :return: The output from the model's predictions
        """
        categories = f"{COMMA}{SPACE}".join(
            [ct.value.lower() for ct in ChangeType.get_granular_change_type_categories()])
        prompts = [SupportedPrompts.DELTA_CHANGE_SUMMARY_STARTER.value,
                   MultiArtifactPrompt(
                       prompt_start=PromptUtil.as_markdown_header("CHANGES:"),
                       build_method=MultiArtifactPrompt.BuildMethod.XML,
                       xml_tags={"file-change": ["filename", "description"]}),
                   task_prompt
                   ]
        output = get_prediction_output(args, artifact_df, state, categories=categories,
                                       prompts=prompts)
        return output[0][task_prompt.args.prompt_id]

    @staticmethod
    def _match_change_type(types: List[str], change_type_mapping: Dict[str, Any]) -> str:
        """
        Attempts to match the change type produced by the model with known change types
        :param types: The change type produced by the model
        :param change_type_mapping: A dictionary with all change_types
        :return: The matched change type if successful otherwise "other"
        """
        change_type = types[0].lower()
        if change_type not in change_type_mapping:
            return OverviewChangeSummaryStep.UNKNOWN_CHANGE_TYPE_KEY
        else:
            return change_type

    @staticmethod
    def _get_summary_from_output(change_summary_output: Dict, task_prompt: QuestionnairePrompt, prompt_num: int) -> str:
        """
        Gets the summary output from all of the model predictions
        :param change_summary_output: The output from the model
        :param task_prompt: The prompt used to get the output
        :param prompt_num: The number of the prompt that produced the summary
        :return: The summary
        """
        tag = task_prompt.get_response_tags_for_prompt(prompt_num)
        return change_summary_output[tag][0]
