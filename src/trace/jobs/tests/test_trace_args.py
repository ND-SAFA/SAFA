from common.models.base_models.supported_base_model import SupportedBaseModel
from common.models.model_generator import ModelGenerator
from test.base_test import BaseTest
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
        model_generator = ModelGenerator(SupportedBaseModel.BERT_TRACE_SIAMESE, "path")
        return TraceArgs(model_generator,
                         **self.get_test_params(),
                         **kwargs)
