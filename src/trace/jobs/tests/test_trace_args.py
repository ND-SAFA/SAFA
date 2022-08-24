from django.test import TestCase
from mock import patch

from common.models.model_generator import ModelGenerator
from test.test_data import TEST_S_ARTS, TEST_T_ARTS, TEST_POS_LINKS
from trace.data.trace_dataset_creator import TraceDatasetCreator
from trace.jobs.trace_args import TraceArgs


class TestTraceArgs(TestCase):
    validation_percentage = 0.25

    def test_set_args(self):
        test_args = self.get_test_trace_args(max_seq_length=3)
        self.assertEquals(test_args.max_seq_length, 3)

    def test_set_args_unknown(self):
        try:
            self.get_test_trace_args(unknown_attr=3)
        except Exception as e:
            self.fail(e)

    def get_test_trace_args(self, **kwargs):
        model_generator = ModelGenerator("bert_trace_siamese", "path")
        return TraceArgs(model_generator,
                         TraceDatasetCreator(source_artifacts=TEST_S_ARTS, target_artifacts=TEST_T_ARTS,
                                             true_links=TEST_POS_LINKS,
                                             model_generator=model_generator,
                                             validation_percentage=self.validation_percentage),

                         "output_path",
                         **kwargs)
