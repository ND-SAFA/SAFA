from tgen.data.readers.pre_train_project_reader import PreTrainProjectReader
from test.data.creators.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions


class TestPreTrainProjectReader(BaseTest):
    """
    Tests that pre-train project creator is able to read pre-training entries.
    """

    def test_pre_train_reader(self):
        """
        Tests that pre-train project creator reads correct lines.
        """
        pre_train_reader = PreTrainProjectReader(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        training_examples = pre_train_reader.create()
        expected_lines = TestMLMPreTrainDatasetCreator.FILE1_LINES + TestMLMPreTrainDatasetCreator.FILE2_LINES
        TestAssertions.assert_lists_have_the_same_vals(self, training_examples, expected_lines)
