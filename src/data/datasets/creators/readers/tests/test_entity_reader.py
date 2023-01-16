from data.datasets.creators.readers.pre_train_project_reader import PreTrainReader
from data.datasets.creators.tests.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from testres.base_test import BaseTest
from testres.test_assertions import TestAssertions


class TestPreTrainReader(BaseTest):
    def test_pre_train_reader(self):
        pre_train_reader = PreTrainReader(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        training_examples = pre_train_reader.get_entities()
        expected_lines = TestMLMPreTrainDatasetCreator.FILE1_LINES + TestMLMPreTrainDatasetCreator.FILE2_LINES
        TestAssertions.assert_lists_have_the_same_vals(self, training_examples, expected_lines)

    def test_get_invalid_property(self):
        pre_train_reader = PreTrainReader(TestMLMPreTrainDatasetCreator.PRETRAIN_DIR)
        with self.assertRaises(ValueError) as e:
            pre_train_reader.get_property("unknown_property")
        self.assertIn("unknown", str(e.exception))
