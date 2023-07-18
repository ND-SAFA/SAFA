from unittest import mock

from test.data.creators.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from tgen.data.readers.pre_train_project_reader import PreTrainProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT, fake_open_ai_completion
from tgen.train.args.open_ai_args import OpenAIArgs


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

    @mock.patch("openai.ChatCompletion.create")
    def test_summarization(self, mock_completion: mock.MagicMock):
        """
        Tests that pre-train data can be summarized
        """
        mock_completion.side_effect = fake_open_ai_completion
        pre_train_reader = PreTrainProjectReader(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        llm_manager = OpenAIManager(OpenAIArgs())
        pre_train_reader.set_summarizer(Summarizer(llm_manager, code_or_exceeds_limit_only=False))
        training_examples = pre_train_reader.read_project()
        expected_lines = TestMLMPreTrainDatasetCreator.FILE1_LINES + TestMLMPreTrainDatasetCreator.FILE2_LINES
        for i, example in enumerate(training_examples):
            self.assertEqual(SUMMARY_FORMAT.format(expected_lines[i]), example)
