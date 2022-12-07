import os
from unittest.mock import patch

from test.base_trace_test import BaseTraceTest
from test.paths.paths import TEST_OUTPUT_DIR
from data.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.creators.split_dataset_creator import SplitDatasetCreator
from data.datasets.dataset_role import DatasetRole
from data.datasets.trace_dataset import TraceDataset
from data.datasets.trainer_dataset_manager import TrainerDatasetManager


class TestTrainerDatasetsContainer(BaseTraceTest):
    TRAIN_DATASET_CREATOR = ClassicTraceDatasetCreator(source_layers=BaseTraceTest.SOURCE_LAYERS,
                                                       target_layers=BaseTraceTest.TARGET_LAYERS,
                                                       true_links=BaseTraceTest.POS_LINKS,
                                                       data_cleaner=BaseTraceTest.DATA_CLEANING_STEPS,
                                                       use_linked_targets_only=False)
    VAL_DATASET_CREATOR = SplitDatasetCreator(split_percentage=0.3)
    EVAL_DATASET_CREATOR = SplitDatasetCreator(split_percentage=0.2)

    @patch.object(MLMPreTrainDatasetCreator, "create")
    def test_prepare_datasets(self, create_mock):
        datasets_container = self.get_trainer_datasets_manager(
            pre_train_dataset_creator=MLMPreTrainDatasetCreator("orig_data_path"),
            eval_dataset_creator=self.EVAL_DATASET_CREATOR)
        datasets_container._prepare_datasets([])
        self.assert_final_datasets_are_as_expected(datasets_container)

    @patch.object(MLMPreTrainDatasetCreator, "create")
    def test_create_dataset_splits(self, create_mock):
        dataset_creators_map = {
            DatasetRole.PRE_TRAIN: MLMPreTrainDatasetCreator("orig_data_path"),
            DatasetRole.TRAIN: self.TRAIN_DATASET_CREATOR,
            DatasetRole.VAL: self.VAL_DATASET_CREATOR,
            DatasetRole.EVAL: self.EVAL_DATASET_CREATOR
        }
        expected_dataset_split_roles = [DatasetRole.TRAIN, DatasetRole.VAL, DatasetRole.EVAL]
        train_dataset = self.TRAIN_DATASET_CREATOR.create()
        splits = TrainerDatasetManager._create_dataset_splits(train_dataset, dataset_creators_map)

        for dataset_role in expected_dataset_split_roles:
            self.assertIn(dataset_role, splits)
            self.assertTrue(isinstance(splits[dataset_role], TraceDataset))
        self.assertNotIn(DatasetRole.PRE_TRAIN, splits)

    def test_get_creator(self):
        datasets_container = self.get_trainer_datasets_manager()
        self.assertIsInstance(datasets_container.get_creator(DatasetRole.TRAIN), ClassicTraceDatasetCreator)

    def test_save_dataset_splits(self):
        if not os.path.exists(TEST_OUTPUT_DIR):
            os.makedirs(TEST_OUTPUT_DIR)
        datasets_container = self.get_trainer_datasets_manager()
        datasets_container.save_dataset_splits(TEST_OUTPUT_DIR)
        self.assert_lists_have_the_same_vals(["train.csv", "val.csv"], os.listdir(TEST_OUTPUT_DIR))

    @patch.object(MLMPreTrainDatasetCreator, "create")
    def test_create_from_map(self, create_mock):
        dataset_creators_map = {DatasetRole.PRE_TRAIN: MLMPreTrainDatasetCreator("orig_data_path"),
                                DatasetRole.TRAIN: self.TRAIN_DATASET_CREATOR,
                                DatasetRole.VAL: self.VAL_DATASET_CREATOR,
                                DatasetRole.EVAL: None}
        datasets_container = self.get_trainer_datasets_manager()
        datasets_map = datasets_container._create_datasets_from_creators(dataset_creators_map)
        self.assertTrue(datasets_map[DatasetRole.PRE_TRAIN] is not None)
        self.assertIsInstance(datasets_map[DatasetRole.TRAIN], TraceDataset)

    def _create_datasets_from_creators(self):
        dataset_creators_map = {DatasetRole.PRE_TRAIN: MLMPreTrainDatasetCreator("orig_data_path"),
                                DatasetRole.TRAIN: self.TRAIN_DATASET_CREATOR,
                                DatasetRole.VAL: self.VAL_DATASET_CREATOR,
                                DatasetRole.EVAL: self.EVAL_DATASET_CREATOR}
        datasets_container = TrainerDatasetManager.create_from_map(dataset_creators_map)
        self.assert_final_datasets_are_as_expected(datasets_container)

    def test_get_set_bad_index(self):
        datasets_container = self.get_trainer_datasets_manager()
        try:
            datasets_container["eval"] = None
            self.fail("Did not raise Exception on bad index")
        except Exception:
            pass

    def get_trainer_datasets_manager(self, pre_train_dataset_creator=None, eval_dataset_creator=None):
        train_dataset_creator = self.TRAIN_DATASET_CREATOR

        val_dataset_creator = self.VAL_DATASET_CREATOR
        trainer_datasets_container = TrainerDatasetManager(
            pre_train_dataset_creator = pre_train_dataset_creator,
            train_dataset_creator=train_dataset_creator,
            val_dataset_creator=val_dataset_creator,
            eval_dataset_creator=eval_dataset_creator)
        return trainer_datasets_container

    def assert_final_datasets_are_as_expected(self, datasets_container):
        expected_dataset_split_roles = [DatasetRole.TRAIN, DatasetRole.VAL, DatasetRole.EVAL]
        for dataset_role in expected_dataset_split_roles:
            self.assertIn(dataset_role, datasets_container)
            self.assertTrue(isinstance(datasets_container[dataset_role], TraceDataset))
        self.assertIn(DatasetRole.PRE_TRAIN, datasets_container)
        self.assertEquals(len(datasets_container[DatasetRole.TRAIN].pos_link_ids),
                          len(datasets_container[DatasetRole.TRAIN].neg_link_ids))