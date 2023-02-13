import os
from unittest import mock
from unittest.mock import patch

from constants import VALIDATION_PERCENTAGE_DEFAULT
from data.datasets.dataset_role import DatasetRole
from data.managers.deterministic_trainer_dataset_manager import DeterministicTrainerDatasetManager
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.tests.base_job_test import BaseJobTest
from jobs.train_job import TrainJob
from models.model_manager import ModelManager
from testres.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from testres.test_assertions import TestAssertions
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestTrainJob(BaseJobTest):
    CSV_DATA_DIR = os.path.join(TEST_DATA_DIR, "csv")
    CSV_DATA_FILE = os.path.join(CSV_DATA_DIR, "test_csv_data.csv")
    EXPECTED_SPLIT_ROLE: DatasetRole = DatasetRole.VAL
    DETERMINISTIC_ID = "1234"

    @patch.object(TraceTrainer, "save_model")
    def test_run_success(self, save_model_mock: mock.MagicMock):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def test_split_train_dataset(self):
        job = self._get_job()
        self.assertTrue(job.trainer_dataset_manager[self.EXPECTED_SPLIT_ROLE] is not None)

    def _assert_success(self, job: AbstractJob, output_dict: dict):
        TestAssertions.assert_training_output_matches_expected(self, output_dict)

    def test_initialize_with_deterministic_dataset_manager(self):
        job = self._get_job(deterministic=True)
        self.assertIsInstance(job.trainer_dataset_manager, DeterministicTrainerDatasetManager)
        self.assertEquals(job.trainer_dataset_manager.get_output_path(), os.path.join(TEST_OUTPUT_DIR,
                                                                                      job.trainer_dataset_manager.dataset_name))

    def _get_job(self, deterministic: bool = False) -> TrainJob:
        dataset_param = "_".join([self.EXPECTED_SPLIT_ROLE.value, "dataset", "creator"])
        trainer_dataset_manager = ObjectCreator.get_definition(TrainerDatasetManager)
        if deterministic:
            trainer_dataset_manager[DeterministicTrainerDatasetManager.DETERMINISTIC_KEY] = self.DETERMINISTIC_ID
            trainer_dataset_manager["output_dir"] = TEST_OUTPUT_DIR
        trainer_dataset_manager.update(**{
            dataset_param: {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
                "val_percentage": VALIDATION_PERCENTAGE_DEFAULT
            }})
        train_job_definition = {
            "model_manager": ObjectCreator.get_definition(ModelManager),
            "job_args": ObjectCreator.get_definition(JobArgs),
            "trainer_dataset_manager": trainer_dataset_manager,
            "trainer_args": {
                **ObjectCreator.get_definition(TrainerArgs),
                "evaluation_strategy": "no",
                "save_strategy": "no"
            }
        }
        job = ObjectCreator.create(TrainJob, override=True, **train_job_definition)
        self.assertEquals(job.trainer_args.num_train_epochs, 1)
        return job
