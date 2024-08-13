from tgen_test.tracing.code_tracer.code_tracer_test_util import CodeTracerTestUtil
from common_resources.data.keys.structure_keys import TraceKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.tracing.code.code_tracer import CodeTracer


class TestCodeTracer(BaseTest):

    def test_base_name_connections(self):
        """
        Tests that header files are links to their implementation files.
        """
        trace_dataset = CodeTracerTestUtil.get_trace_dataset()
        code_tracer = CodeTracer(trace_dataset)
        code_tracer.add_code_traces()
        links = trace_dataset.trace_df.get_links()

        self.assertEqual(2, len(links))
        for link in links:
            self.assertEqual(CodeTracerTestUtil.h_file_name, link[TraceKeys.SOURCE])

        targets = set([link[TraceKeys.TARGET] for link in links])
        self.assertIn(CodeTracerTestUtil.cpp_file_name, targets)
        self.assertIn(CodeTracerTestUtil.cc_file_name, targets)
