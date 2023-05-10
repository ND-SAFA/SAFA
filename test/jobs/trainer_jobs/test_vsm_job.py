from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.jobs.trainer_jobs.vsm_job import VSMJob
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.object_creator import ObjectCreator
from tgen.variables.typed_definition_variable import TypedDefinitionVariable


class TestVSMJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def _get_job(self):
        job_args: JobArgs = ObjectCreator.create(JobArgs)
        trainer_dataset_manager: TrainerDatasetManager = ObjectCreator.create(TrainerDatasetManager, **{
            "eval_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **ObjectCreator.dataset_creator_definition
            }
        }, override=False)
        return VSMJob(trainer_dataset_manager=trainer_dataset_manager, job_args=job_args,
                      metrics=ObjectCreator.trainer_args_definition["metrics"])

    def _assert_success(self, job: VSMJob, output_dict: dict):
        eval_dataset = job.trainer_dataset_manager[DatasetRole.EVAL]
        output_dict = output_dict[JobResult.BODY][JobResult.PREDICTION_OUTPUT]
        TestAssertions.verify_prediction_output(self, output_dict, eval_dataset, base_score=0.0)
