from test.base_test import BaseTest
from test.test_data import TEST_POS_LINKS, TEST_SOURCE_LAYERS, TEST_TARGET_LAYERS
from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT
from trace.data.trace_link import TraceLink
from trace.jobs.trace_args_builder import TraceArgsBuilder


class TestTraceArgsBuilder(BaseTest):

    EXPECTED_VALUES = BaseTest.get_test_args()

    def test_build(self, ):
        test_trace_args_buidler = self.get_test_trace_arg_builder()
        args = test_trace_args_buidler.build()
        self.assertEquals(args.model_generator.model_name.lower(), self.EXPECTED_VALUES["base_model"])
        self.assertEquals(args.model_generator.model_path, self.EXPECTED_VALUES["model_path"])
        self.assertEquals(args.output_dir, self.EXPECTED_VALUES["output_dir"])
        for link in TEST_POS_LINKS:
            link_id = TraceLink.generate_link_id(link[0], link[1])
            self.assertIn(link_id, args.trace_dataset_creator.pos_link_ids)

    def get_test_trace_arg_builder(self):
        return TraceArgsBuilder(**self.EXPECTED_VALUES)
