import os

from data.datasets.creators.readers.entity.artifact_reader import ArtifactReader
from data.datasets.creators.readers.entity.pre_train_reader import PreTrainReader
from data.datasets.creators.tests.test_mlm_pre_train_dataset_creator import TestMLMPreTrainDatasetCreator
from data.datasets.keys.structure_keys import StructureKeys
from test.base_test import BaseTest
from test.paths.paths import TEST_DATA_DIR
from test.test_assertions import TestAssertions


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

    def test_get_folder(self):
        folder_path = os.path.join(TEST_DATA_DIR, "folder_entities")
        artifact_reader = ArtifactReader(TEST_DATA_DIR, {
            StructureKeys.PATH: folder_path
        })
        entity_parser = artifact_reader.get_entity_parser()
        entities = entity_parser(folder_path)
        self.assertEquals(len(entities), 2)

    def test_unknown_parser(self):
        file_path = os.path.join(TEST_DATA_DIR, "test_errors", "unknown_format.wrt")
        artifact_reader = ArtifactReader(TEST_DATA_DIR, {
            StructureKeys.PATH: file_path
        })
        with self.assertRaises(ValueError) as e:
            artifact_reader.get_entity_parser()
        self.assertIn("unknown", str(e.exception))
