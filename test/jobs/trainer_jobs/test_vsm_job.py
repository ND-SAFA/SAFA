from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.trainer_jobs.vsm_job import VSMJob
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.test_assertions import TestAssertions
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
                      metrics=ObjectCreator.trainer_args_definition["metrics"], select_predictions=False)

    def _assert_success(self, job: VSMJob, job_result: JobResult):
        eval_dataset = job.trainer_dataset_manager[DatasetRole.EVAL]
        output: TracePredictionOutput = job_result.body
        TestAssertions.verify_prediction_output(self, output, eval_dataset, base_score=0.0)
