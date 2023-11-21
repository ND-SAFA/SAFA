from test.data.creators.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.readers.pre_train_project_reader import PreTrainProjectReader
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_open_ai_responses import SUMMARY_FORMAT
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestPreTrainProjectReader(BaseTest):
    """
    Tests that pre-train project creator is able to read pre-training entries.
    """

    def test_pre_train_reader(self):
        """
        Tests that pre-train project creator reads correct lines.
        """
        pre_train_reader = PreTrainProjectReader(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        training_examples = pre_train_reader.read_project()
        expected_lines = TestMLMPreTrainDatasetCreator.FILE1_LINES + TestMLMPreTrainDatasetCreator.FILE2_LINES
        TestAssertions.assert_lists_have_the_same_vals(self, training_examples, expected_lines)

    @mock_openai
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that pre-train data can be summarized
        """
        ai_manager.mock_summarization()
        pre_train_reader = PreTrainProjectReader(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        llm_manager = OpenAIManager(OpenAIArgs())
        pre_train_reader.set_summarizer(
            ArtifactsSummarizer(llm_manager_for_artifact_summaries=llm_manager, summarize_code_only=False))
        training_examples = pre_train_reader.read_project()
        expected_lines = TestMLMPreTrainDatasetCreator.FILE1_LINES + TestMLMPreTrainDatasetCreator.FILE2_LINES
        for i, example in enumerate(training_examples):
            self.assertEqual(SUMMARY_FORMAT.format(expected_lines[i]), example)
