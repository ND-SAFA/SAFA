import uuid
from typing import Dict

from tgen.core.trace_output.stage_eval import Metrics
from tgen.core.trainers.vsm_trainer import VSMTrainer
from common_resources.data.tdatasets.dataset_role import DatasetRole
from tgen.jobs.components.job_result import JobResult
from tgen.testres.base_tests.base_trace_test import BaseTraceTest
from tgen.testres.dataset_creator_tutil import DatasetCreatorTUtil
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.test_data_manager import TestDataManager


class TestVSMTrainer(BaseTraceTest):
    EXPECTED_PREDICTION_SIZE = TestDataManager.get_n_candidates()
    TEST_METRIC_DEFINITION = [["map", ["map"]],
                              ["classification", ["precision", "recall", "f1", "f2"]]]
    TEST_METRICS_NAMES = [m for m, aliases in TEST_METRIC_DEFINITION]

    def test_perform_prediction(self):
        test_trace_trainer = self.get_custom_trace_trainer(dataset_container_args={"val_dataset_creator": None})
        test_trace_trainer.perform_training()
        trace_prediction_output = test_trace_trainer.perform_prediction()
        trace_prediction_job_result = JobResult(job_id=uuid.uuid4(), body=trace_prediction_output)
        eval_dataset = test_trace_trainer.trainer_dataset_manager[DatasetRole.EVAL]
        TestAssertions.verify_prediction_output(self, trace_prediction_job_result, eval_dataset, base_score=0.0)
        self.assert_metrics(trace_prediction_output.metrics)

    def get_custom_trace_trainer(self, dataset_container_args: Dict = None):
        trainer_dataset_manager = DatasetCreatorTUtil.create_trainer_dataset_manager([DatasetRole.EVAL], **dataset_container_args)
        return VSMTrainer(trainer_dataset_manager=trainer_dataset_manager, metrics=self.TEST_METRICS_NAMES, select_predictions=False)

    def assert_metrics(self, metrics: Metrics):
        """
        Verifies that metrics contains all the desired metrics.
        :param metrics: The metrics object being checked.
        """
        for metric, aliases in self.TEST_METRIC_DEFINITION:
            for alias in aliases:
                self.assertIn(alias, metrics)
