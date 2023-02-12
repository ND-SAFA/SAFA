import os

from analysis.dataset_analyzer import DatasetAnalyzer
from jobs.abstract_job import AbstractJob
from jobs.analyze_dataset_job import AnalyzeDatasetJob
from jobs.tests.base_job_test import BaseJobTest
from testres.paths.paths import TEST_OUTPUT_DIR
from util.object_creator import ObjectCreator
from variables.definition_variable import DefinitionVariable
from variables.variable import Variable


class TestAnalyzeDatasetJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, output_dict: dict):
        self.assertIn(DatasetAnalyzer.OUTPUT_FILENAME, os.listdir(TEST_OUTPUT_DIR))

    def _get_job(self) -> AbstractJob:
        definition = {"job_args": ObjectCreator.job_args_definition,
                      "dataset_creator": ObjectCreator.dataset_creator_definition,
                      "model_managers": [{"model_path": "bert-base-uncased"}]}
        return ObjectCreator.create(AnalyzeDatasetJob, **definition, override=True)
