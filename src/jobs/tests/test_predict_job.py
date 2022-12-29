from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_args import JobArgs
from jobs.predict_job import PredictJob
from jobs.tests.base_job_test import BaseJobTest
from models.model_manager import ModelManager
from test.test_assertions import TestAssertions
from train.trainer_args import TrainerArgs
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestPredictJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _get_job(self):
        job_args: JobArgs = ObjectCreator.create(JobArgs)
        model_manager: ModelManager = ObjectCreator.create(ModelManager)
        trainer_dataset_manager: TrainerDatasetManager = ObjectCreator.create(TrainerDatasetManager, **{
            "eval_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "CLASSIC_TRACE",
                **ObjectCreator.dataset_creator_definition
            }
        }, override=True)
        trainer_args: TrainerArgs = ObjectCreator.create(TrainerArgs)
        return PredictJob(job_args=job_args, model_manager=model_manager,
                          trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args)

    def _assert_success(self, output_dict: dict):
        TestAssertions.assert_prediction_output_matches_expected(self, output_dict)
