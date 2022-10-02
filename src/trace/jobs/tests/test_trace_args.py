from common.models.model_generator import ModelGenerator
from test.base_test import BaseTest
from test.test_data import TEST_POS_LINKS, TEST_SOURCE_LAYERS, TEST_TARGET_LAYERS
from trace.data.trace_dataset_creator import TraceDatasetCreator
from trace.jobs.trace_args import TraceArgs


class TestTraceArgs(BaseTest):
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
                         **self.get_test_params(),
                         **kwargs)
