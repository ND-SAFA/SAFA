import os

import pandas as pd

from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.summarizer.summarizer import Summarizer

datasets = {
    "Drone": {
        "type": "Code",
        "export_path": "drone-pl/code.csv",
    },
    "itrust": {
        "type": "JSP Code",
        "export_path": "itrust/code.csv",
    }
}
if __name__ == "__main__":
    dataset_name = "itrust"
    dataset_instructions = datasets[dataset_name]
    export_dir_name = dataset_instructions["export_path"]
    artifact_type_name = dataset_instructions["type"]

    export_path = os.path.expanduser(os.path.join("~/desktop/safa/datasets/paper", export_dir_name))
    data_path = os.path.expanduser("~/desktop/safa/datasets/open-source")

    dataset_path = os.path.join(data_path, dataset_name)
    project_reader = StructuredProjectReader(dataset_path)
    artifact_df, trace_df, layer_df = project_reader.read_project()

    artifact_types = list(artifact_df[ArtifactKeys.LAYER_ID].unique())
    code_df = artifact_df[artifact_df[ArtifactKeys.LAYER_ID] == artifact_type_name]
    code_list = list(code_df[ArtifactKeys.CONTENT.value])

    summarizer = Summarizer()
    chunker_types = [SupportedChunker.JAVA for i in range(len(code_list))]
    summarized_list = summarizer.summarize_bulk(code_list, chunker_types=chunker_types)

    summarized_df = pd.DataFrame()
    summarized_df["id"] = code_df.index
    summarized_df["content"] = summarized_list
    summarized_df.to_csv(export_path, index=False)
