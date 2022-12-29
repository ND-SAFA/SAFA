import os
from unittest import mock
from unittest.mock import patch

from testres.paths.paths import TEST_DATA_DIR
from testres.test_assertions import TestAssertions

from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.gan_train_job import GanTrainJob
from jobs.tests.base_job_test import BaseJobTest
from models.model_manager import ModelManager
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestGanTrainJob(BaseJobTest):
    """
    Tests that GAN is able to train and testres.
    TODO: Add testres that includes a pre-training data
    TODO: Reduce the run time of the testres to < 10 seconds
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
        TestAssertions.assert_training_output_matches_expected(self, output_dict, self.EXAMPLE_TRAINING_OUTPUT)

    def _get_job(self) -> AbstractJob:
        trainer_dataset_manager = ObjectCreator.create(TrainerDatasetManager, override=True, **{
            "pre_train_dataset_creator": ObjectCreator.pretrain_dataset_definition,
            "train_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "CLASSIC_TRACE",
                **ObjectCreator.dataset_creator_definition
            },
        })
        job_args = ObjectCreator.create(JobArgs)
        model_manager = ObjectCreator.create(ModelManager)
        trainer_args = ObjectCreator.create(TrainerArgs, **{
            "num_train_epochs": 1
        })

        return GanTrainJob(job_args, trainer_dataset_manager=trainer_dataset_manager, model_manager=model_manager,
                           trainer_args=trainer_args)
