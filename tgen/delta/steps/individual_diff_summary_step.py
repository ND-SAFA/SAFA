from typing import Dict, List

from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE, DASH, EMPTY_STRING
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.delta.change_type import ChangeType
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.delta.delta_util import get_prediction_output
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class IndividualDiffSummaryStep(AbstractPipelineStep[DeltaArgs, DeltaState]):
    LAYER_ID = "diff"
    CHANGE_TYPE_TO_QUESTION_PROMPT = {ChangeType.ADDED: SupportedPrompts.DELTA_NEW_FILE,
                                      ChangeType.DELETED: SupportedPrompts.DELTA_REMOVED_FILE}

    def _run(self, args: DeltaArgs, state: DeltaState) -> None:
        """
        Gets summaries and categorizations for each modified file diff
        :param args: The arguments for the delta summarizer
        :param state: The current state of the delta summarizer
        :return: None
        """
        logger.log_with_title("STEP 2 - Generating DIFF Summaries")

        state.diff_summaries = {}
        for change_type in [ChangeType.MODIFIED, ChangeType.ADDED, ChangeType.DELETED]:
            diffs = args.change_type_to_diffs[change_type]
            if len(diffs) < 1:
                continue
            logger.info(f"Getting diff summaries for {change_type.value} files.")
            ids = list(diffs.keys())
            artifacts_df = self._create_artifacts_df_from_diff(args, diffs, ids, include_original=change_type == ChangeType.MODIFIED)
            questionnaire: QuestionnairePrompt = SupportedPrompts.DIFF_SUMMARY_QUESTIONNAIRE.value
            if change_type in self.CHANGE_TYPE_TO_QUESTION_PROMPT:
                questionnaire.question_prompts = [self.CHANGE_TYPE_TO_QUESTION_PROMPT[change_type].value] \
                                                 + questionnaire.question_prompts[-2:]
            output = get_prediction_output(args, artifacts_df, state, prompts=[SupportedPrompts.DIFF_SUMMARY_STARTER.value,
                                                                               ArtifactPrompt(include_id=False),
                                                                               questionnaire])

            state.diff_summaries.update(self._parse_output(ids, output, questionnaire))
            state.save(self.get_step_name())

    def _create_artifacts_df_from_diff(self, args: DeltaArgs, modified_diffs: Dict[str, str], ids: List[str],
                                       include_original: bool = True) -> ArtifactDataFrame:
        """
        Creates a dataset from the file diffs
        :param args: The arguments for the delta summarizer
        :param modified_diffs: The dictionary containing all file diffs that were modified
        :param ids: The filename ids
        :return: The artifacts df created from the file diffs
        """
        contents = []
        for a_id in ids:
            content = []
            parent = self._get_parent_artifact_content(a_id, args.dataset)
            if parent:
                content.extend(parent)
            if include_original:
                original = args.dataset.artifact_df.get_artifact(a_id)[ArtifactKeys.CONTENT]
                content.extend([PromptUtil.format_as_markdown_header('ORIGINAL CODE FILE:'), original])
            content.extend([PromptUtil.format_as_markdown_header('DIFF FOR CODE:'), modified_diffs[a_id]])
            contents.append(f'{NEW_LINE}{NEW_LINE.join(content)}{NEW_LINE}')
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ids,
                                         ArtifactKeys.CONTENT: contents,
                                         ArtifactKeys.LAYER_ID: [self.LAYER_ID for _ in ids]})
        return artifact_df

    @staticmethod
    def _parse_output(ids: List[str], output: List[Dict], questionnaire: QuestionnairePrompt) -> Dict[str, Dict[str, str]]:
        """
        Parses the output to create dictionary mapping the filename to the diff summaries/related
        :param ids: The list of filenames
        :param output: The output from the model
        :return: A dictionary mapping the filename to the diff summaries/related
        """
        assert len(output) == len(ids), "Missing predictions."
        results = {}
        for pred, filename in zip(output, ids):
            results[filename] = {}
            res = {tag: val[0].lstrip(NEW_LINE) for tag, val in pred[questionnaire.id].items()}
            for category in ChangeType.get_granular_change_type_categories():
                category_tag = DASH.join(SeparateJoinedWordsStep.separate_deliminated_word(category.name.lower()))
                category_res: str = res.get(category_tag, "no")
                if not category_res.lower().startswith("no"):
                    results[filename][category.value] = category_res
            for i in range(1, 3):
                tag = questionnaire.get_response_tags_for_question(-i)
                results[filename][tag] = res[tag]
        return results

    @staticmethod
    def _get_parent_artifact_content(child_id: str, original_dataset: TraceDataset) -> str:
        """
        Gets the parent artifact content to include in the prompt as context
        :param child_id: The id of the child
        :param original_dataset: The original dataset with parent artifacts
        :return: The content to include in the prompt
        """
        links = original_dataset.trace_df.filter_by_row(lambda row: row[TraceKeys.SOURCE.value] == child_id
                                                                    and row[TraceKeys.LABEL.value] == 1)
        parents = [original_dataset.artifact_df.get_artifact(link[TraceKeys.TARGET])[ArtifactKeys.CONTENT]
                   for i, link in links.itertuples()]
        content = NEW_LINE.join(parents)
        if content:
            return f"{PromptUtil.format_as_markdown_header('CONTEXT:')}{NEW_LINE}{content}"
        return EMPTY_STRING
