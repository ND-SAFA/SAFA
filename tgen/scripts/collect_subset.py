import os.path

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.tracing.ranking.common.ranking_util import RankingUtil


def read_dataset(project_path: str) -> TraceDataset:
    reader = StructuredProjectReader(project_path=project_path)
    creator = TraceDatasetCreator(project_reader=reader)
    dataset = creator.create()
    return dataset


def collect_subset(full_dataset_path: str, subset_dataset_path: str, export_dir: str):
    full_dataset = read_dataset(full_dataset_path)
    subset_dataset = read_dataset(subset_dataset_path)

    all_trace_links = full_dataset.trace_df.get_links()
    source2links = RankingUtil.group_trace_predictions(all_trace_links, TraceKeys.SOURCE.value)
    code_ids = list(subset_dataset.artifact_df.index)
    code_links = [t for c in code_ids for t in source2links.get(c, [])]

    design_ids = set([t[TraceKeys.parent_label()] for t in code_links])
    design_links = [t for d in design_ids for t in source2links.get(d, [])]

    requirement_ids = set([t[TraceKeys.parent_label()] for t in design_links])

    artifact_ids = code_ids + list(design_ids) + list(requirement_ids)
    subset_artifact_df = full_dataset.artifact_df.filter_by_index(artifact_ids)

    subset_trace_links = code_links + design_links
    subset_link_ids = [t[TraceKeys.LINK_ID] for t in subset_trace_links]
    subset_trace_df = full_dataset.trace_df.filter_by_index(subset_link_ids)
    
    dataset = TraceDataset(artifact_df=subset_artifact_df, trace_df=subset_trace_df, layer_df=full_dataset.layer_df)
    exporter = SafaExporter(export_path, dataset=dataset)
    exporter.export()


if __name__ == "__main__":
    full_path = os.path.expanduser(
        "~/desktop/safa/output/hgen/baseline/papers/hgen/code/safa/full/Functional Requirement/final_generated_dataset/safa")
    subset_path = os.path.expanduser("~/desktop/safa/datasets/papers/hgen/code/safa/subset")
    export_path = os.path.expanduser("~/desktop/test")
    os.makedirs(export_path, exist_ok=True)
    collect_subset(full_path, subset_path, export_path)
