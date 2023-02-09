import os
from unittest import mock
from unittest.mock import patch

from data.datasets.dataset_role import DatasetRole
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from experiments.multi_epoch_experiment_step import MultiEpochExperimentStep
from experiments.tests.base_experiment_test import BaseExperimentTest
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.delete_model_job import DeleteModelJob
from jobs.supported_job_type import SupportedJobType
from jobs.train_job import TrainJob
from testres.paths.paths import TEST_OUTPUT_DIR
from util.file_util import FileUtil
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestMultiEpochExperimentStep(BaseExperimentTest):
    EXPERIMENT_VARS = ["trainer_dataset_manager.train_dataset_creator.project_path",
                       "trainer_args.num_train_epochs"]

    EPOCH_ARGS = [10, 40, 10]

    @patch.object(TrainJob, "_run")
    def test_run(self, train_job_run_mock: mock.MagicMock):
        train_job_run_mock.side_effect = self.job_fake_run
        experiment_step = self.get_experiment_step()
        experiment_step.run(TEST_OUTPUT_DIR)

        output_dirs = FileUtil.ls_dir(TEST_OUTPUT_DIR)
        epochs_run = set()
        for job_id in output_dirs:
            output_file = os.path.join(TEST_OUTPUT_DIR, job_id, AbstractJob.OUTPUT_FILENAME)
            step_output = self._load_step_output(output_file_path=output_file)
            step_experimental_vars = step_output[JobResult.EXPERIMENTAL_VARS]
            epochs_run.add(step_experimental_vars["num_train_epochs"])
        self.assertEquals(len(epochs_run), len(self.EPOCH_ARGS))
        for epoch in range(*self.EPOCH_ARGS):
            self.assertIn(epoch, epochs_run)

    def get_experiment_step(self):
        kwargs = {"override": True, **{
            "jobs": [{
                TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.TRAIN.name,
                "model_manager": ObjectCreator.model_manager_definition,
                "job_args": {},
                "trainer_dataset_manager": {
                    "train_dataset_creator": {
                        TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                        **ObjectCreator.dataset_creator_definition
                    }
                },
                "trainer_args": {**ObjectCreator.trainer_args_definition,
                                 "train_epochs_range": TestMultiEpochExperimentStep.EPOCH_ARGS},

            }]
        }}
        return ObjectCreator.create(MultiEpochExperimentStep, **kwargs)

    @staticmethod
    def get_test_jobs():
        job1 = DeleteModelJob(job_args=JobArgs(output_dir=TEST_OUTPUT_DIR))
        job2 = DeleteModelJob(job_args=JobArgs(output_dir=TEST_OUTPUT_DIR))
        return [job1, job2]

    @staticmethod
    def get_job_by_id(step, job_id):
        found_job = None
        for job in step.jobs:
            if str(job.id) == job_id:
                found_job = job
                break
        return found_job

    def assert_experimental_vars(self, experiment_step):
        for job in experiment_step.jobs:
            self.assertIn(JobResult.EXPERIMENTAL_VARS, job.result)
            job_experiment_vars = job.result[JobResult.EXPERIMENTAL_VARS]
            for experiment_var_path in self.EXPERIMENT_VARS:
                path_attrs = experiment_var_path.split(".")
                attr = job
                for i, attr_name in enumerate(path_attrs):
                    if not hasattr(attr, attr_name):
                        if isinstance(attr, TrainerDatasetManager):
                            attr = attr.get_creator(DatasetRole.TRAIN)
                        continue
                    attr = getattr(attr, attr_name)
                    self.assertIn(attr_name, job_experiment_vars.keys())
                    if i == len(path_attrs) - 1:
                        self.assertEquals(attr, job_experiment_vars[attr_name])
