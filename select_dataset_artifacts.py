import os

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader

if __name__ == "__main__":
    dataset_name = "cchit"
    data_path = os.path.expanduser("~/desktop/safa/datasets/open-source")
    artifact_export_path = os.path.expanduser(f"~/desktop/safa/datasets/paper/{dataset_name}/sources.csv")
    trace_export_path = os.path.expanduser(f"~/desktop/safa/datasets/paper/{dataset_name}/traces.csv")
    dataset_path = os.path.join(data_path, dataset_name)
    project_reader = StructuredProjectReader(dataset_path)
    artifact_df, trace_df, layer_df = project_reader.read_project()
    artifact_types = list(artifact_df[ArtifactKeys.LAYER_ID].unique())
    trace_df = trace_df[trace_df['source'] > 1108]

    df = trace_df.reset_index().groupby("source")["target"].nunique()


    def select_with_links(n_links):
        sample_row = df[df == n_links].sample(n=1)
        return sample_row


    max_links = df.max()
    min_links = df.min()
    median_links = df.median()

    max_sample = select_with_links(max_links)
    min_sample = select_with_links(min_links)
    median_sample = select_with_links(median_links)
    artifact_names = [s.index[0] for s in [max_sample, min_sample, median_sample]]
    selected_df = artifact_df.loc[artifact_names]
    selected_df.to_csv(artifact_export_path)

    trace_df[trace_df["source"].isin(artifact_names)].to_csv(trace_export_path, index=False)
    print("hi")
