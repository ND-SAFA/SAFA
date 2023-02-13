import os
from unittest import mock
from unittest.mock import patch

import math

from constants import BASE_EXPERIMENT_NAME
from data.datasets.dataset_role import DatasetRole
from data.managers.deterministic_trainer_dataset_manager import DeterministicTrainerDatasetManager
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from data.readers.definitions.structure_project_definition import StructureProjectDefinition
from data.readers.structured_project_reader import StructuredProjectReader
from experiments.experiment_step import ExperimentStep
from experiments.tests.base_experiment_test import BaseExperimentTest
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.predict_job import PredictJob
from jobs.train_job import TrainJob
from models.model_manager import ModelManager
from testres.paths.paths import TEST_OUTPUT_DIR
from train.trainer_args import TrainerArgs
from util.file_util import FileUtil
from util.object_creator import ObjectCreator
from util.status import Status
from variables.undetermined_variable import UndeterminedVariable


class TestExperimentStep(BaseExperimentTest):
    EXPERIMENT_VARS = ["trainer_dataset_manager.train_dataset_creator.project_path",
                       "trainer_args.num_train_epochs"]

    @patch.object(StructuredProjectReader, "_get_definition_reader")
    @patch.object(TrainJob, "_run")
    def test_run(self, train_job_run_mock: mock.MagicMock, definition_mock: mock.MagicMock):
        train_job_run_mock.side_effect = self.job_fake_run
        definition_mock.return_value = StructureProjectDefinition()
        experiment_step = self.get_experiment_step()
        experiment_step.run(TEST_OUTPUT_DIR)
        experiment_step.save_results(TEST_OUTPUT_DIR)
        output = self._load_step_output()
        job_dirs = FileUtil.ls_dir(TEST_OUTPUT_DIR)
        self.assertEqual(len(output["jobs"]), len(job_dirs))
        self.assert_experimental_vars(experiment_step)
        self.assertEquals(output["status"], Status.SUCCESS.value)
        best_job = self.get_job_by_id(experiment_step, output["best_job"])
        self.assertTrue(best_job is not None)
        self.assertEquals(max(self.accuracies), best_job.result[JobResult.METRICS]["accuracy"])
        self.assertEqual(train_job_run_mock.call_count, 4)

    @patch.object(StructuredProjectReader, "_get_definition_reader")
    @patch.object(TrainJob, "_run")
    def test_run_failed(self, train_job_run_mock: mock.MagicMock, definition_mock: mock.MagicMock):
        train_job_run_mock.side_effect = ValueError()
        definition_mock.return_value = StructureProjectDefinition()
        experiment_step = self.get_experiment_step()
        experiment_step.run(TEST_OUTPUT_DIR)
        self.assertEquals(experiment_step.status, Status.FAILURE)
        self.assertEqual(train_job_run_mock.call_count, 1)

    @patch.object(StructuredProjectReader, "_get_definition_reader")
    @patch.object(PredictJob, "_run")
    def test_run_with_best_prior(self, predict_job_run_mock: mock.MagicMock, definition_mock: mock.MagicMock):
        predict_job_run_mock.side_effect = self.job_fake_run
        definition_mock.return_value = StructureProjectDefinition()
        train_experiment_step = self.get_experiment_step()
        predict_experiment_step = self.get_experiment_step(train=False)
        best_job_from_prior = train_experiment_step.jobs.pop()
        best_job = predict_experiment_step.run(TEST_OUTPUT_DIR, [best_job_from_prior]).pop()
        expected_model_path = best_job_from_prior.model_manager.model_path
        self.assertEquals(best_job.model_manager.model_path, expected_model_path)
        self.assertEqual(predict_job_run_mock.call_count, 1)

    @patch.object(StructuredProjectReader, "_get_definition_reader")
    def test_divide_jobs_into_runs(self, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        train_step = self.get_experiment_step()
        runs = train_step._divide_jobs_into_runs()
        self.assertEquals(len(runs), math.ceil(len(train_step.jobs) / train_step.MAX_JOBS))
        for run_ in runs:
            self.assertLessEqual(len(run_), train_step.MAX_JOBS)

    @patch.object(StructuredProjectReader, "_get_definition_reader")
    def test_update_jobs_undetermined_vars(self, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        train_step = self.get_experiment_step()
        predict_step = self.get_experiment_step(train=False)
        predict_step.jobs[0].trainer_args.num_train_epochs = UndeterminedVariable()
        final_jobs = predict_step._update_jobs_undetermined_vars(predict_step.jobs, train_step.jobs)
        self.assertEquals(len(final_jobs), len(train_step.jobs))
        for job in final_jobs:
            self.assertTrue(not isinstance(job.trainer_args.num_train_epochs, UndeterminedVariable))
            self.assertTrue(not isinstance(job.model_manager.model_path, UndeterminedVariable))

    def test_get_failed_jobs(self):
        jobs = self.get_test_jobs()
        jobs[0].result.set_job_status(Status.FAILURE)
        failed_jobs = ExperimentStep._get_failed_jobs(jobs)
        self.assertEquals(1, len(failed_jobs))

    @patch.object(StructuredProjectReader, "_get_definition_reader")
    def test_run_on_all_jobs(self, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        jobs = self.get_test_jobs()
        results = ExperimentStep._run_on_jobs(jobs, "get_output_filepath")
        self.assertEquals(len(results), 2)
        self.assertEquals(results[0], results[1])  # Nothing differentiating the two paths other than id which is set by experiment

    @patch.object(StructuredProjectReader, "_get_definition_reader")
    @patch.object(AbstractTraceJob, "get_trainer")
    def test_get_best_job(self, get_trainer_mock, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        job1, job2 = self.get_test_jobs()
        step = self.get_experiment_step()
        job1.result[JobResult.METRICS] = {"accuracy": 0.5}

        job2.result[JobResult.METRICS] = {"accuracy": 0.8}
        best_job = step._get_best_job([job1, job2])
        self.assertEquals(best_job.id, job2.id)

    def test_update_job_children_output_paths(self):
        job1, job2 = self.get_test_jobs()
        output_dir = os.path.join(TEST_OUTPUT_DIR, "experiment_step")
        job1.model_manager = ModelManager("bert-base-uncased")
        experiment_step = ExperimentStep([job1, job2])
        experiment_step.update_output_path(output_dir)
        self.assertEquals(job1.model_manager.output_dir, os.path.join(output_dir, BASE_EXPERIMENT_NAME, "models"))

    @staticmethod
    def get_experiment_step(train=True) -> ExperimentStep:
        kwargs = {}
        if not train:
            kwargs = {"override": True, **{
                "jobs": [{
                    **ObjectCreator.experiment_predict_job_definition,
                    "model_manager": {
                        "model_path": "?"
                    }
                }]
            }}
        return ObjectCreator.create(ExperimentStep, **kwargs)

    @staticmethod
    def get_test_jobs():
        job1 = TrainJob(JobArgs(output_dir=TEST_OUTPUT_DIR), ModelManager(TEST_OUTPUT_DIR), TrainerDatasetManager(),
                        TrainerArgs(output_dir=TEST_OUTPUT_DIR))
        job2 = TrainJob(JobArgs(output_dir=TEST_OUTPUT_DIR), ModelManager(TEST_OUTPUT_DIR), TrainerDatasetManager(),
                        TrainerArgs(output_dir=TEST_OUTPUT_DIR))
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
