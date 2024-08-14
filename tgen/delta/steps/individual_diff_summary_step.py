from typing import Dict, List

from common_resources.tools.constants.symbol_constants import DASH, EMPTY_STRING, NEW_LINE
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.prompt_util import PromptUtil
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys, TraceKeys
from common_resources.data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from tgen.delta.change_type import ChangeType
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.delta.delta_util import get_prediction_output
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class IndividualDiffSummaryStep(AbstractPipelineStep[DeltaArgs, DeltaState]):
    LAYER_ID = "diff"
    CHANGE_TYPE_TO_QUESTION_PROMPT = {ChangeType.ADDED: SupportedPrompts.DELTA_NEW_FILE,
                                      ChangeType.DELETED: SupportedPrompts.DELTA_REMOVED_FILE}
    NO_CHANGE_RESPONSE = "no"
    CONTEXT_TITLE = 'CONTEXT:'
    ORIGINAL_TITLE = 'ORIGINAL CODE FILE:'
    DIFF_TITLE = 'DIFF FOR CODE:'

    def _run(self, args: DeltaArgs, state: DeltaState) -> None:
        """
        Gets summaries and categorizations for each modified file diff
        :param args: The arguments for the delta summarizer
        :param state: The current state of the delta summarizer
        :return: None
        """
        state.diff_summaries = {}
        for change_type in [ChangeType.MODIFIED, ChangeType.ADDED, ChangeType.DELETED]:
            diffs = args.change_type_to_diffs[change_type]
            if len(diffs) < 1:
                continue
            logger.info(f"Getting diff summaries for {change_type.value} files.")
            ids = list(diffs.keys())
            artifact_df = self._create_artifact_df_from_diff(args, diffs, ids, include_original=change_type == ChangeType.MODIFIED)
            questionnaire: QuestionnairePrompt = SupportedPrompts.DIFF_SUMMARY_QUESTIONNAIRE.value
            if change_type in self.CHANGE_TYPE_TO_QUESTION_PROMPT:
                questionnaire.question_prompts = [self.CHANGE_TYPE_TO_QUESTION_PROMPT[change_type].value] \
                                                 + questionnaire.child_prompts[-2:]
            output = get_prediction_output(args, artifact_df, state, prompts=[SupportedPrompts.DIFF_SUMMARY_STARTER.value,
                                                                              ArtifactPrompt(include_id=False),
                                                                              questionnaire])

            state.diff_summaries.update(self._parse_output(ids, output, questionnaire))
            state.save(self.get_step_name())

    @staticmethod
    def _create_artifact_df_from_diff(args: DeltaArgs, filename2diffs: Dict[str, str], ids: List[str],
                                      include_original: bool = True) -> ArtifactDataFrame:
        """
        Creates a dataset from the file diffs
        :param args: The arguments for the delta summarizer
        :param filename2diffs: The dictionary containing filenames mapped to their diffs
        :param ids: The filename ids
        :param include_original: Whether to include original artifacts in the prompt.
        :return: The artifacts df created from the file diffs
        """
        contents = []
        for a_id in ids:
            content = []
            parent = IndividualDiffSummaryStep._get_parent_artifact_content(a_id, args.dataset)
            if parent:
                content.append(parent)
            if include_original:
                original = args.dataset.artifact_df.get_artifact(a_id)[ArtifactKeys.CONTENT]
                content.extend([PromptUtil.as_markdown_header(IndividualDiffSummaryStep.ORIGINAL_TITLE), original])
            content.extend([PromptUtil.as_markdown_header(IndividualDiffSummaryStep.DIFF_TITLE), filename2diffs[a_id]])
            contents.append(f'{NEW_LINE}{NEW_LINE.join(content)}{NEW_LINE}')
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ids,
                                         ArtifactKeys.CONTENT: contents,
                                         ArtifactKeys.LAYER_ID: [IndividualDiffSummaryStep.LAYER_ID for _ in ids]})
        return artifact_df

    @staticmethod
    def _parse_output(ids: List[str], output: List[Dict], questionnaire: QuestionnairePrompt) -> Dict[str, Dict[str, str]]:
        """
        Parses the output to create dictionary mapping the filename to the diff summaries/related
        :param ids: The list of filenames
        :param output: The output from the model
        :param questionnaire: The questionnaire used to build the prompt.
        :return: A dictionary mapping the filename to the diff summaries/related
        """
        no_res = IndividualDiffSummaryStep.NO_CHANGE_RESPONSE
        assert len(output) == len(ids), "Missing predictions."
        results = {}
        for pred, filename in zip(output, ids):
            results[filename] = {}
            res = {tag: val[0].lstrip(NEW_LINE) if val else no_res for tag, val in pred[questionnaire.args.prompt_id].items()}
            for category in ChangeType.get_granular_change_type_categories():
                category_tag = DASH.join(SeparateJoinedWordsStep.separate_deliminated_word(category.name.lower()))
                category_res: str = res.get(category_tag, no_res)
                if not category_res.lower().startswith(no_res):
                    results[filename][category.value] = category_res
            for i in range(1, 3):
                tag = questionnaire.get_response_tags_for_prompt(-i)
                results[filename][tag] = res[tag]
        return results

    @staticmethod
    def _get_parent_artifact_content(child_id: str, original_dataset: PromptDataset) -> str:
        """
        Gets the parent artifact content to include in the prompt as context
        :param child_id: The id of the child
        :param original_dataset: The original dataset with parent artifacts
        :return: The content to include in the prompt
        """
        if original_dataset.trace_dataset:
            links = original_dataset.trace_df.filter_by_row(lambda row: row[TraceKeys.SOURCE.value] == child_id
                                                                        and row[TraceKeys.LABEL.value] == 1)
            parents = [original_dataset.artifact_df.get_artifact(link[TraceKeys.TARGET])[ArtifactKeys.CONTENT]
                       for i, link in links.itertuples()]
            content = NEW_LINE.join(parents)
            if content:
                return f"{PromptUtil.as_markdown_header(IndividualDiffSummaryStep.CONTEXT_TITLE)}{NEW_LINE}{content}"
        return EMPTY_STRING
