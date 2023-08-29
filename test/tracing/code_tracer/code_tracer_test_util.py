from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.tdatasets.trace_dataset import TraceDataset


class CodeTracerTestUtil:
    code_artifact_type = "Code"
    h_file_name = "src/abc/some_class.h"
    cpp_file_name = "src/def/some_class.cpp"
    cc_file_name = "src/ghi/some_class.cc"
    artifacts = [{"id": h_file_name, "content": "", "layer_id": code_artifact_type, "summary": ""},
                 {"id": cpp_file_name, "content": "", "layer_id": code_artifact_type, "summary": ""},
                 {"id": cc_file_name, "content": "", "layer_id": code_artifact_type, "summary": ""}]

    @classmethod
    def get_trace_dataset(cls) -> TraceDataset:
        """
        Creates default trace dataset with class entities.
        """
        artifact_df = ArtifactDataFrame(CodeTracerTestUtil.artifacts)
        trace_df = TraceDataFrame()
        layer_df = LayerDataFrame()
        trace_dataset = TraceDataset(artifact_df, trace_df, layer_df)
        return trace_dataset
