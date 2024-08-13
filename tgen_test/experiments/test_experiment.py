import os
from copy import deepcopy
from unittest import mock
from unittest.mock import patch

from common_resources.data.readers.definitions.structure_project_definition import StructureProjectDefinition
from common_resources.data.readers.structured_project_reader import StructuredProjectReader
from tgen.experiments.experiment import Experiment
from tgen.jobs.trainer_jobs.hugging_face_job import HuggingFaceJob
from tgen.testres.base_tests.base_experiment_test import BaseExperimentTest


class TestExperiment(BaseExperimentTest):

    @patch.object(StructuredProjectReader, "get_definition_reader")
    @patch.object(HuggingFaceJob, "_run")
    def test_run(self, hf_run_mock: mock.MagicMock, definition_mock: mock.MagicMock):
        hf_run_mock.side_effect = self.job_fake_run
        experiment = self.get_experiment()
        experiment.run()
        self.assertEqual(hf_run_mock.call_count, 9)
        result_dirs = os.listdir(os.path.join(experiment.output_dir, "experiment_0"))
        self.assertEqual(len(result_dirs), len(experiment.steps))

    @patch.object(StructuredProjectReader, "get_definition_reader")
    @patch.object(HuggingFaceJob, "_run")
    def test_run_no_metric(self, hf_run_mock: mock.MagicMock,
                           definition_mock: mock.MagicMock):
        hf_run_mock.side_effect = self.job_fake_run
        definition_mock.return_value = StructureProjectDefinition()
        experiment = self.get_experiment(use_metric=False)
        experiment.run()
        self.assertEqual(hf_run_mock.call_count, len(experiment.steps[0]) + len(experiment.steps[1]))

    def get_experiment(self, use_metric: bool = True):
        definition = deepcopy(self.EXPERIMENT_DEFINITION)
        if not use_metric:
            definition["steps"][0].pop("comparison_criterion")
        return Experiment.initialize_from_definition(definition)
