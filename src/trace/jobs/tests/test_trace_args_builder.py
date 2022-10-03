from test.base_test import BaseTest
from test.test_data import TEST_POS_LINKS, TEST_SOURCE_LAYERS, TEST_TARGET_LAYERS
from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT
from trace.data.trace_link import TraceLink
from trace.jobs.trace_args_builder import TraceArgsBuilder


class TestTraceArgsBuilder(BaseTest):

    EXPECTED_VALUES = BaseTest.get_test_params(include_settings=False)

    def test_build(self):
        test_trace_args_buidler = self.get_test_trace_arg_builder()
        args = test_trace_args_buidler.build()
        self.build_test(args)

    def test_build_with_settings(self, ):
        params = self.get_test_params(include_settings=True)
        test_trace_args_buidler = self.get_test_trace_arg_builder(params)
        args = test_trace_args_buidler.build()
        for setting_name, setting_val in params["settings"].items():
            self.assertEqual(getattr(args, setting_name), setting_val)
        self.build_test(args)

    def build_test(self, args):
        self.assertEquals(args.model_generator.model_name.lower(), self.EXPECTED_VALUES["base_model"])
        self.assertEquals(args.model_generator.model_path, self.EXPECTED_VALUES["model_path"])
        self.assertEquals(args.output_dir, self.EXPECTED_VALUES["output_dir"])
        for link in TEST_POS_LINKS:
            link_id = TraceLink.generate_link_id(link[0], link[1])
            self.assertIn(link_id, args.trace_dataset_creator.pos_link_ids)

    def get_test_trace_arg_builder(self, params=None):
        params = params if params else self.EXPECTED_VALUES
        return TraceArgsBuilder(**params)
