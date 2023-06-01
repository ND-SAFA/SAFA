import math
import os

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader

DATA_PATH = os.path.expanduser("~/desktop/safa/datasets/open-source")
if __name__ == "__main__":
    dataset_name = "cchit"
    export_dataset_name = "cchit"
    target_artifact_mask_creator = lambda df: df["source"].astype(int) > 1108
    DATASET_INPUT_PATH = os.path.join(DATA_PATH, dataset_name)
    SOURCE_EXPORT_PATH = os.path.expanduser(f"~/desktop/safa/datasets/paper/{export_dataset_name}/source.csv")
    TRACE_EXPORT_PATH = os.path.expanduser(f"~/desktop/safa/datasets/paper/{export_dataset_name}/traces.csv")

    # Read
    project_reader = StructuredProjectReader(DATASET_INPUT_PATH)
    artifact_df, trace_df, layer_df = project_reader.read_project()
    artifact_types = list(artifact_df[ArtifactKeys.LAYER_ID].unique())
    trace_df = trace_df[trace_df["source"].isin(artifact_df.index) & trace_df["target"].isin(artifact_df.index)]
    query_df = trace_df[target_artifact_mask_creator(trace_df)]
    counts_df = query_df.reset_index().groupby("source")["target"].nunique()


    def select_with_links(n_links, n_sample):
        sample_row = counts_df[counts_df == n_links].sample(n=n_sample)
        return list(sample_row.index)


    max_links = counts_df.max()
    min_links = counts_df.min()
    median_links = math.ceil(counts_df.median())

    max_sample = select_with_links(max_links, 1)
    median_sample = select_with_links(median_links, 3)
    min_sample = select_with_links(min_links, 1)

    artifact_names = [s for samples in [max_sample, median_sample, min_sample] for s in samples]
    selected_df = artifact_df.loc[artifact_names]
    selected_df.to_csv(SOURCE_EXPORT_PATH)
    trace_df[trace_df["source"].isin(artifact_names)].to_csv(TRACE_EXPORT_PATH, index=False)
    print(f"Max: {max_links}\tMedian: {median_links}\tMin: {min_links}")
    print(f"Selected artifacts: {artifact_names}")
