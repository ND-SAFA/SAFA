from gen_common_test.data.creators.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from gen_common.data.readers.pre_train_project_reader import PreTrainProjectReader
from gen_common.data.summarizer.artifacts_summarizer import ArtifactsSummarizer
from gen_common_test.base_tests.base_test import BaseTest
from gen_common_test.mocking import mock_anthropic
from gen_common_test.mocking import SUMMARY_FORMAT
from gen_common_test.mocking import TestAIManager


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
        self.assert_lists_have_the_same_vals(training_examples, expected_lines)

    @mock_anthropic
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that pre-train data can be summarized
        """
        ai_manager.mock_summarization()
        pre_train_reader = PreTrainProjectReader(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        pre_train_reader.set_summarizer(
            ArtifactsSummarizer(summarize_code_only=False))
        training_examples = pre_train_reader.read_project()
        expected_lines = TestMLMPreTrainDatasetCreator.FILE1_LINES + TestMLMPreTrainDatasetCreator.FILE2_LINES
        for i, example in enumerate(training_examples):
            self.assertEqual(SUMMARY_FORMAT.format(expected_lines[i]), example)
