import os
from unittest import mock
from unittest.mock import patch

from data.datasets.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.gan_train_job import GanTrainJob
from jobs.tests.base_job_test import BaseJobTest
from models.model_manager import ModelManager
from test.paths.paths import TEST_DATA_DIR
from test.test_assertions import TestAssertions
from test.test_object_creator import TestObjectCreator
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs


class TestGanTrainJob(BaseJobTest):
    """
    Tests that GAN is able to train and test.
    TODO: Add test that includes a pre-training data
    TODO: Reduce the run time of the test to < 10 seconds
    """
    PRETRAIN_DIR = os.path.join(TEST_DATA_DIR, "pre_train")
    EXAMPLE_TRAINING_OUTPUT = {
        "stats": [{
            "epoch": 1,
            "Valid. Accur.": 0
        }]
    }

    @patch.object(TraceTrainer, "save_model")
    def test_run_success(self, save_model_mock: mock.MagicMock):
        self._test_run_success()

    def _assert_success(self, output_dict: dict):
        TestAssertions.assert_training_output_matches_expected(self, output_dict)

    def _get_job(self) -> AbstractJob:
        trainer_dataset_manager = TestObjectCreator.create(TrainerDatasetManager, override=True, **{
            "pre_train_dataset_creator": TestObjectCreator.pretrain_dataset_definition,
            "train_dataset_creator": TestObjectCreator.dataset_creator_definition,
        })
        job_args = TestObjectCreator.create(JobArgs)
        model_manager = TestObjectCreator.create(ModelManager)
        trainer_args = TestObjectCreator.create(TrainerArgs, **{
            "num_train_epochs": 1
        })

        return GanTrainJob(job_args, trainer_dataset_manager=trainer_dataset_manager, model_manager=model_manager,
                           trainer_args=trainer_args)
