import os

import pandas as pd
from dotenv.main import load_dotenv

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame

load_dotenv()
if __name__ == "__main__":
    output_path = os.getenv("OUTPUT_PATH")
    project_path = os.path.join(output_path, "hgen", "best")
    dataset_path = os.path.join(project_path, "linked_source_layer_dataset")
    trace_path = "/home/kat/git-repos/safa/tgen/datasets/dr_onboard_autonomy_trace_dataset/trace_df.csv"
    df = TraceDataFrame(pd.read_csv(trace_path))
    df.remove_duplicate_indices()
    df.to_csv(trace_path)
    # trace_dataset = TraceDatasetCreator(DataFrameProjectReader(dataset_path, overrides={
    #               "allowed_orphans": -1,
    #               "allowed_missing_sources": 1000,
    #               "allowed_missing_targets": 1000
    #             })).create()
    # SafaExporter(export_path=os.path.join(dataset_path, "safa_format"), dataset=trace_dataset).export()
