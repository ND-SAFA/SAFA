import os
from copy import deepcopy
from unittest import mock
from unittest.mock import patch

from data.readers.definitions.structure_project_definition import StructureProjectDefinition
from data.readers.structured_project_reader import StructuredProjectReader
from experiments.experiment import Experiment
from experiments.tests.base_experiment_test import BaseExperimentTest
from jobs.predict_job import PredictJob
from jobs.train_job import TrainJob


class TestExperiment(BaseExperimentTest):
    @patch.object(StructuredProjectReader, "_get_definition_reader")
    @patch.object(PredictJob, "_run")
    @patch.object(TrainJob, "_run")
    def test_run(self, train_job_run_mock: mock.MagicMock, predict_job_run_mock: mock.MagicMock, definition_mock: mock.MagicMock):
        train_job_run_mock.side_effect = self.job_fake_run
        predict_job_run_mock.side_effect = self.job_fake_run
        definition_mock.return_value = StructureProjectDefinition()
        experiment = self.get_experiment()
        experiment.run()
        self.assertEqual(train_job_run_mock.call_count, 8)
        self.assertEqual(predict_job_run_mock.call_count, 1)
        result_dirs = os.listdir(os.path.join(experiment.output_dir, "experiment_0"))
        self.assertEquals(len(result_dirs), len(experiment.steps))

    @patch.object(StructuredProjectReader, "_get_definition_reader")
    @patch.object(PredictJob, "_run")
    @patch.object(TrainJob, "_run")
    def test_run_no_metric(self, train_job_run_mock: mock.MagicMock, predict_job_run_mock: mock.MagicMock,
                           definition_mock: mock.MagicMock):
        train_job_run_mock.side_effect = self.job_fake_run
        predict_job_run_mock.side_effect = self.job_fake_run
        definition_mock.return_value = StructureProjectDefinition()
        experiment = self.get_experiment(use_metric=False)
        experiment.run()
        self.assertEqual(train_job_run_mock.call_count, 8)
        self.assertEqual(predict_job_run_mock.call_count, 8)

    def get_experiment(self, use_metric: bool = True):
        definition = deepcopy(self.EXPERIMENT_DEFINITION)
        if not use_metric:
            definition["steps"][0].pop("comparison_criterion")
        return Experiment.initialize_from_definition(definition)
