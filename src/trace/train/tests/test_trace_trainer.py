from django.test import TestCase

from mock import patch

from trace.data.trace_dataset_creator import TraceDatasetCreator
from trace.jobs.trace_args import TraceArgs
from trace.train.trace_trainer import TraceTrainer


class TestTraceTrainer(TestCase):
    TEST_S_ARTS = {"s1": "token1",
                   "s2": "token2",
                   "s3": "token3"}

    TEST_T_ARTS = {"t1": "token1",
                   "t2": "token2",
                   "t3": "token3"}

    TEST_POS_LINKS = [("s1", "t1"), ("s2", "t1"), ("s3", "t2")]
    VAlIDATION_PERCENTAGE = 0.3
    EXPECTED_VALIDATION_SIZE = 3

    @patch("common.models.model_generator.ModelGenerator")
    def test_perform_training(self, model_generator_mock):
        test_trace_trainer = self.get_test_trace_trainer(model_generator_mock)

    def get_test_trace_trainer(self, model_generator_mock):
        trace_dataset_creator = TraceDatasetCreator(source_artifacts=self.TEST_S_ARTS, target_artifacts=self.TEST_T_ARTS,
                                                    true_links=self.TEST_POS_LINKS,
                                                    model_generator=model_generator_mock,
                                                    validation_percentage=self.VAlIDATION_PERCENTAGE)
        args = TraceArgs(model_generator=model_generator_mock,
                         trace_dataset_creator=trace_dataset_creator,
                         output_path="output")
        return TraceTrainer(args)
