from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.summarizer.summarizer import Summarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary import Summary
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MockResponses, TEST_PROJECT_SUMMARY
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.safa_test_project import SafaTestProject


class TestSummarizer(BaseTest):

    N_ARTIFACTS = len(SafaTestProject.get_source_artifacts() + SafaTestProject.get_target_artifacts())
    N_PROJECT_SECTIONS = len(MockResponses.project_summary_responses)

    """
    NO RE-SUMMARIZATIONS SO EVERYTHING IS SUMMARIZED AT MAX ONCE
    """
    @mock_anthropic
    def test_with_no_resummarize_and_no_summaries(self, ai_manager: TestAIManager):
        args = SummarizerArgs(do_resummarize_artifacts=False)

        ai_manager.set_responses(MockResponses.project_summary_responses)
        summarizer = self.get_summarizer(args)
        n_expected_summarizations = self.N_ARTIFACTS + self.N_PROJECT_SECTIONS
        self._assert_summarization(summarizer, n_expected_summarizations, ai_manager)

    @mock_anthropic
    def test_with_no_resummarize_with_project_summary(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=False)

        summarizer = self.get_summarizer(args, with_project_summary=True)
        self._assert_summarization(summarizer, self.N_ARTIFACTS, ai_manager)

    @mock_anthropic
    def test_with_no_resummarize_with_artifact_summaries(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=False)

        ai_manager.set_responses(MockResponses.project_summary_responses)
        summarizer = self.get_summarizer(args, with_artifact_summaries=True)
        self._assert_summarization(summarizer, self.N_PROJECT_SECTIONS, ai_manager)

    @mock_anthropic
    def test_with_no_resummarize_with_all_summarized(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=False)

        summarizer = self.get_summarizer(args, with_artifact_summaries=True, with_project_summary=True)
        self._assert_summarization(summarizer, 0, ai_manager)


    """
    RE_SUMMARIZE ARTIFACTS SO ARTIFACTS ARE ALWAYS SUMMARIZED AT LEAST ONCE, PROJECT SUMMARIZED NO MORE THAN ONCE
    """
    @mock_anthropic
    def test_with_resummarize_artifacts_and_no_summaries(self, ai_manager: TestAIManager):
        args = SummarizerArgs(do_resummarize_artifacts=True)

        ai_manager.set_responses(MockResponses.project_summary_responses)
        summarizer = self.get_summarizer(args)
        n_expected_summarizations = 2*self.N_ARTIFACTS + self.N_PROJECT_SECTIONS
        self._assert_summarization(summarizer, n_expected_summarizations, ai_manager)

    @mock_anthropic
    def test_with_resummarize_artifacts_with_project_summary(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=True)

        summarizer = self.get_summarizer(args, with_project_summary=True)
        self._assert_summarization(summarizer, self.N_ARTIFACTS, ai_manager)

    @mock_anthropic
    def test_with_resummarize_artifacts_with_artifact_summaries(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=True)

        ai_manager.set_responses(MockResponses.project_summary_responses)
        summarizer = self.get_summarizer(args, with_artifact_summaries=True)
        self._assert_summarization(summarizer, self.N_PROJECT_SECTIONS+self.N_ARTIFACTS, ai_manager)

    @mock_anthropic
    def test_with_resummarize_artifacts_with_all_summarized(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=True)

        summarizer = self.get_summarizer(args, with_artifact_summaries=True, with_project_summary=True)
        self._assert_summarization(summarizer, self.N_ARTIFACTS, ai_manager)

    def _assert_summarization(self, summarizer: Summarizer, expected_summarization_calls: int, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        dataset = summarizer.summarize()
        self.assertEqual(ai_manager.mock_calls, expected_summarization_calls)
        self.assertFalse(DataFrameUtil.contains_empty_string(dataset.artifact_df[ArtifactKeys.SUMMARY]))
        self.assertFalse(DataFrameUtil.contains_na(dataset.artifact_df[ArtifactKeys.SUMMARY]))
        self.assertIsInstance(dataset.project_summary, Summary)

    def get_summarizer(self, summarizer_args: SummarizerArgs,
                       with_artifact_summaries: bool = False, with_project_summary: bool = False) -> Summarizer:
        creator = PromptDatasetCreator(trace_dataset_creator=TraceDatasetCreator(SafaTestProject.get_project_reader()))
        dataset = creator.create()
        if with_artifact_summaries:
            dataset.artifact_df[ArtifactKeys.SUMMARY] = [f"summary of {c}" for c in dataset.artifact_df[ArtifactKeys.CONTENT]]
        if with_project_summary:
            dataset.project_summary = TEST_PROJECT_SUMMARY
        summarizer_args.summarize_code_only = False
        return Summarizer(summarizer_args, dataset)


