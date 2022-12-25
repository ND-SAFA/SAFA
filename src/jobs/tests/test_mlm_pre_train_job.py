import os
from unittest import mock
from unittest.mock import patch

from transformers import AutoModelForMaskedLM

from data.datasets.trainer_dataset_manager import TrainerDatasetManager
from experiments.variables.typed_definition_variable import TypedDefinitionVariable
from jobs.components.job_args import JobArgs
from jobs.mlm_pre_train_job import MLMPreTrainJob
from jobs.tests.base_job_test import BaseJobTest
from models.model_manager import ModelManager
from models.model_properties import ModelTask
from test.paths.paths import TEST_DATA_DIR
from test.test_assertions import TestAssertions
from test.test_object_builder import TestObjectBuilder
from train.trainer_args import TrainerArgs


class TestMLMPreTrainJob(BaseJobTest):
    PRETRAIN_DIR = os.path.join(TEST_DATA_DIR, "pre_train")

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    @patch.object(ModelManager, '_ModelManager__load_model')
    @patch.object(ModelManager, 'get_tokenizer')
    def _test_run_success(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = AutoModelForMaskedLM.from_pretrained("bert-base-uncased")
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        job = self.get_job()
        job.run()
        self.assert_output_on_success(self._load_job_output(job))

    def _assert_success(self, output_dict: dict):
        TestAssertions.assert_training_output_matches_expected(self, output_dict)

    def _get_job(self):
        job_args = TestObjectBuilder.create(JobArgs)
        model_manager = TestObjectBuilder.create(ModelManager, model_task=ModelTask.MASKED_LEARNING)
        trainer_dataset_manager = TestObjectBuilder.create(TrainerDatasetManager, **{
            "train_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "MLM_PRETRAIN",
                "orig_data_path": self.PRETRAIN_DIR
            }
        })
        trainer_args = TestObjectBuilder.create(TrainerArgs)
        return MLMPreTrainJob(job_args=job_args, model_manager=model_manager,
                              trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args)
