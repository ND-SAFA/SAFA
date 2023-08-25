from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.testres.base_tests.base_test import BaseTest
from tgen.tracing.code_tracer import CodeTracer


class TestCodeTracer(BaseTest):
    h_file_name = "src/abc/some_class.h"
    cpp_file_name = "src/def/some_class.cpp"
    cc_file_name = "src/ghi/some_class.cc"
    artifacts = [{"id": h_file_name, "content": "", "layer_id": "Code", "summary": ""},
                 {"id": cpp_file_name, "content": "", "layer_id": "Code", "summary": ""},
                 {"id": cc_file_name, "content": "", "layer_id": "Code", "summary": ""}]

    def test_base_name_connections(self):
        """
        Tests that header files are links to their implementation files.
        """
        artifact_df = ArtifactDataFrame(self.artifacts)
        trace_df = TraceDataFrame()
        layer_df = LayerDataFrame()
        trace_dataset = TraceDataset(artifact_df, trace_df, layer_df)
        code_tracer = CodeTracer(trace_dataset)
        links = code_tracer.trace()
        self.assertEqual(2, len(links))
        for link in links:
            self.assertEqual(self.h_file_name, link["source"])
        targets = set([link["target"] for link in links])
        self.assertIn(self.cpp_file_name, targets)
        self.assertIn(self.cc_file_name, targets)
