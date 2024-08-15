import math
import os
from unittest import mock
from unittest.mock import patch

from common_resources.data.readers.definitions.structure_project_definition import StructureProjectDefinition
from common_resources.data.readers.structured_project_reader import StructuredProjectReader
from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.llm.args.hugging_face_args import HuggingFaceArgs
from common_resources.tools.constants.symbol_constants import PERIOD
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.status import Status
from common_resources.tools.variables.undetermined_variable import UndeterminedVariable

from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.experiments.experiment_step import ExperimentStep
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.jobs.trainer_jobs.hugging_face_job import HuggingFaceJob
from tgen.models.model_manager import ModelManager
from tgen.testres.base_tests.base_experiment_test import BaseExperimentTest
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.paths.paths import TEST_OUTPUT_DIR


class TestExperimentStep(BaseExperimentTest):
    EXPERIMENT_VARS = ["trainer_dataset_manager.train_dataset_creator.project_path",
                       "trainer_args.num_train_epochs"]

    @patch.object(StructuredProjectReader, "get_definition_reader")
    @patch.object(HuggingFaceJob, "_run")
    def test_run(self, train_job_run_mock: mock.MagicMock, definition_mock: mock.MagicMock):
        FileUtil.delete_dir(TEST_OUTPUT_DIR)
        self.assertFalse(os.path.exists(TEST_OUTPUT_DIR))
        train_job_run_mock.side_effect = self.job_fake_run
        definition_mock.return_value = StructureProjectDefinition()

        experiment_step = self.get_experiment_step()
        experiment_step.run(TEST_OUTPUT_DIR)
        experiment_step.save_results(TEST_OUTPUT_DIR)
        output = self._load_step_output()
        n_jobs = len(output["jobs"])
        self.assertEqual(n_jobs, len(output["jobs"]))
        self.assert_experimental_vars(experiment_step)
        self.assertEqual(output["status"], Status.SUCCESS.value)
        best_job = self.get_job_by_id(experiment_step, output["best_job"]["id"])
        self.assertTrue(best_job is not None)
        self.assertEqual(max(self.accuracies), best_job.result.body.metrics["accuracy"])
        self.assertEqual(train_job_run_mock.call_count, 4)

    @patch.object(StructuredProjectReader, "get_definition_reader")
    @patch.object(HuggingFaceJob, "_run")
    def test_run_failed(self, train_job_run_mock: mock.MagicMock, definition_mock: mock.MagicMock):
        train_job_run_mock.side_effect = ValueError()
        definition_mock.return_value = StructureProjectDefinition()
        experiment_step = self.get_experiment_step()
        experiment_step.run(TEST_OUTPUT_DIR)
        self.assertEqual(experiment_step.status, Status.FAILURE)
        self.assertEqual(train_job_run_mock.call_count, 1)

    @patch.object(StructuredProjectReader, "get_definition_reader")
    @patch.object(HuggingFaceJob, "_run")
    def test_run_with_best_prior(self, predict_job_run_mock: mock.MagicMock, definition_mock: mock.MagicMock):
        predict_job_run_mock.side_effect = self.job_fake_run
        definition_mock.return_value = StructureProjectDefinition()
        train_experiment_step = self.get_experiment_step()
        predict_experiment_step = self.get_experiment_step(train=False)
        best_job_from_prior = train_experiment_step.jobs.pop()
        best_job = predict_experiment_step.run(TEST_OUTPUT_DIR, [best_job_from_prior]).pop()
        expected_model_path = best_job_from_prior.model_manager.model_path
        self.assertEqual(best_job.model_manager.model_path, expected_model_path)
        self.assertEqual(predict_job_run_mock.call_count, 1)

    @patch.object(StructuredProjectReader, "get_definition_reader")
    def test_divide_jobs_into_runs(self, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        train_step = self.get_experiment_step()
        runs = train_step._divide_jobs_into_runs()
        self.assertEqual(len(runs), math.ceil(len(train_step.jobs) / train_step.MAX_JOBS))
        for run_ in runs:
            self.assertLessEqual(len(run_), train_step.MAX_JOBS)

    @patch.object(StructuredProjectReader, "get_definition_reader")
    def test_update_jobs_undetermined_vars(self, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        train_step = self.get_experiment_step()
        predict_step = self.get_experiment_step(train=False)
        predict_step.jobs[0].trainer_args.num_train_epochs = UndeterminedVariable()
        final_jobs = predict_step._update_jobs_undetermined_vars(predict_step.jobs, train_step.jobs)
        self.assertEqual(len(final_jobs), len(predict_step.jobs))
        for job in final_jobs:
            self.assertTrue(not isinstance(job.trainer_args.num_train_epochs, UndeterminedVariable))
            self.assertTrue(not isinstance(job.model_manager.model_path, UndeterminedVariable))

    def test_get_failed_jobs(self):
        jobs = self.get_test_jobs()
        jobs[0].result.status = Status.FAILURE
        failed_jobs = ExperimentStep._get_failed_jobs(jobs)
        self.assertEqual(1, len(failed_jobs))

    @patch.object(StructuredProjectReader, "get_definition_reader")
    def test_run_on_all_jobs(self, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        jobs = self.get_test_jobs()
        results = ExperimentStep._run_on_jobs(jobs, "get_output_filepath")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], results[1])  # Nothing differentiating the two paths other than id which is set by experiment

    @patch.object(StructuredProjectReader, "get_definition_reader")
    @patch.object(AbstractTrainerJob, "get_trainer")
    def test_get_best_job(self, get_trainer_mock, definition_mock: mock.MagicMock):
        definition_mock.return_value = StructureProjectDefinition()
        job1, job2 = self.get_test_jobs()
        step = self.get_experiment_step()
        job1.result.body = TracePredictionOutput(metrics={"accuracy": 0.5})

        job2.result.body = TracePredictionOutput(metrics={"accuracy": 0.8})
        best_job = step._get_best_job([job1, job2])
        self.assertEqual(best_job.id, job2.id)

    def test_update_job_children_output_paths(self):
        job1, job2 = self.get_test_jobs()
        output_dir = os.path.join(TEST_OUTPUT_DIR, "experiment_step")
        job1.model_manager = ModelManager("bert-base-uncased")
        experiment_step = ExperimentStep([job1, job2])
        experiment_step.update_output_path(output_dir)
        self.assertEqual(job1.model_manager.output_dir, os.path.join(output_dir, "models"))

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
        job1 = HuggingFaceJob(job_args=JobArgs(output_dir=TEST_OUTPUT_DIR), model_manager=ModelManager(TEST_OUTPUT_DIR),
                              trainer_dataset_manager=TrainerDatasetManager(),
                              trainer_args=HuggingFaceArgs(output_dir=TEST_OUTPUT_DIR), task=TrainerTask.TRAIN)
        job2 = HuggingFaceJob(job_args=JobArgs(output_dir=TEST_OUTPUT_DIR), model_manager=ModelManager(TEST_OUTPUT_DIR),
                              trainer_dataset_manager=TrainerDatasetManager(),
                              trainer_args=HuggingFaceArgs(output_dir=TEST_OUTPUT_DIR), task=TrainerTask.TRAIN)
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
            job_experiment_vars = job.result.experimental_vars
            for experiment_var_path in self.EXPERIMENT_VARS:
                path_attrs = experiment_var_path.split(PERIOD)
                attr = job
                for i, attr_name in enumerate(path_attrs):
                    if not hasattr(attr, attr_name):
                        if isinstance(attr, TrainerDatasetManager):
                            attr = attr.get_creator(DatasetRole.TRAIN)
                        continue
                    attr = getattr(attr, attr_name)
                    self.assertIn(attr_name, job_experiment_vars.keys())
                    if i == len(path_attrs) - 1:
                        self.assertEqual(attr, job_experiment_vars[attr_name])
