from copy import deepcopy

from typing import Dict, List

from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE, DASH, EMPTY_STRING
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.delta.change_type import ChangeType
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class IndividualDiffSummaryStep(AbstractPipelineStep[DeltaArgs, DeltaState]):
    LAYER_ID = "diff"
    CATEGORIES = [ChangeType.RENAMED_VARS, ChangeType.DEPENDENCIES_IMPORTS, ChangeType.NEW_FUNC, ChangeType.MODIFIED_FUNC,
                  ChangeType.BUG_FIXES, ChangeType.REFACTORED]

    def _run(self, args: DeltaArgs, state: DeltaState) -> None:
        """
        Gets summaries and categorizations for each modified file diff
        :param args: The arguments for the delta summarizer
        :param state: The current state of the delta summarizer
        :return: None
        """
        logger.log_with_title("STEP 1 - Generating DIFF Summaries")
        modified_diffs = args.change_type_to_diffs[ChangeType.MODIFIED]
        ids = list(modified_diffs.keys())
        diff_dataset = self._create_dataset_from_diff(args, modified_diffs, ids)
        output = self._get_prediction_output(args, diff_dataset, state)
        results = self._parse_output(ids, output)
        state.diff_summaries = results

    def _create_dataset_from_diff(self, args: DeltaArgs, modified_diffs: Dict[str, str], ids: List[str]) -> PromptDataset:
        """
        Creates a dataset from the file diffs
        :param args: The arguments for the delta summarizer
        :param modified_diffs: The dictionary containing all file diffs that were modified
        :param ids: The filename ids
        :return: The dataset created from the file diffs
        """
        original_artifacts = args.dataset.artifact_df
        content = [SupportedPrompts.DELTA_CHANGED_FILE_PROMPT.value.format_value(
            self._get_parent_artifact_content(a_id, args.dataset),
            original_artifacts.get_artifact(a_id)[ArtifactKeys.CONTENT], modified_diffs[a_id]) for a_id in ids]
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ids,
                                         ArtifactKeys.CONTENT: content,
                                         ArtifactKeys.LAYER_ID: [self.LAYER_ID for _ in ids]})
        diff_dataset = PromptDataset(artifact_df=artifact_df)
        return diff_dataset

    def _parse_output(self, ids, output) -> Dict[str, Dict[str, str]]:
        """
        Parses the output to create dictionary mapping the filename to the diff summaries/related
        :param ids: The list of filenames
        :param output: The output from the model
        :return: A dictionary mapping the filename to the diff summaries/related
        """
        questionnaire: QuestionnairePrompt = SupportedPrompts.DELTA_DIFF_SUMMARY_QUESTIONNAIRE.value
        assert len(output) == len(ids), "Missing predictions."
        results = {}
        for pred, filename in zip(output, ids):
            results[filename] = {}
            res = {tag: val[0].lstrip(NEW_LINE) for tag, val in pred[questionnaire.id].items()}
            for category in self.CATEGORIES:
                category_tag = DASH.join(SeparateJoinedWordsStep.separate_deliminated_word(category.name.lower()))
                category_res: str = res.get(category_tag, "no")
                if not category_res.lower().startswith("no"):
                    results[filename][category.value] = category_res
            for i in range(1, 3):
                tag = questionnaire.question_prompts[-i].response_manager.response_tag
                results[filename][tag] = res[tag]
        return results

    @staticmethod
    def _get_prediction_output(args: DeltaArgs, diff_dataset: PromptDataset, state: DeltaState) -> List:
        """
        Gets the model predictions for each file diff
        :param args: The arguments for the delta summarizer
        :param diff_dataset: The dataset created from the file diffs
        :param state: The current state of the delta summarizer
        :return: The model predictions for each file diff
        """
        dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: diff_dataset})
        prompt_builder = PromptBuilder(prompts=[SupportedPrompts.DELTA_PROJECT_SUMMARY_PROMPT.value,
                                                ArtifactPrompt(include_id=False),
                                                SupportedPrompts.DELTA_DIFF_SUMMARY_QUESTIONNAIRE.value])
        prompt_builder.format_prompts_with_var(summary=state.project_summary)
        trainer = LLMTrainer(LLMTrainerState(llm_manager=args.llm_manager,
                                             trainer_dataset_manager=dataset_manager,
                                             prompt_builder=prompt_builder,
                                             completion_type=LLMCompletionType.GENERATION))
        output = trainer.perform_prediction().predictions
        return output

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
            return f"{PromptUtil.format_as_markdown('CONTEXT:')}{NEW_LINE}{content}"
        return EMPTY_STRING