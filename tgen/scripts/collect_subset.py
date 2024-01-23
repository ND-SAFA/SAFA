import os.path
import shutil
from typing import Dict, List

import numpy as np

from tgen.common.logging.logger_manager import logger
from tgen.common.objects.trace import Trace
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.structure_keys import LayerKeys, TraceKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.tracing.ranking.common.ranking_util import RankingUtil


def read_dataset(project_path: str) -> TraceDataset:
    reader = StructuredProjectReader(project_path=project_path)
    creator = TraceDatasetCreator(project_reader=reader)
    dataset = creator.create()
    return dataset


def get_links(artifact_id, source2links: Dict[str, List[Trace]], n_items: int = 5):
    artifact_links = [t for t in source2links.get(artifact_id, []) if not np.isnan(t[TraceKeys.SCORE])]
    sorted_links = sorted(artifact_links, key=lambda t: t[TraceKeys.SCORE], reverse=True)
    # artifact_links = artifact_links[:n_items]
    return sorted_links


def get_artifact_links(artifact_ids, source2links: Dict[str, List[Trace]], **kwargs):
    links = [t for a_id in artifact_ids for t in get_links(a_id, source2links, **kwargs)]
    return links


def collect_subset(full_dataset_path: str, subset_dataset_path: str, export_dir: str):
    full_dataset = read_dataset(full_dataset_path)
    subset_dataset = read_dataset(subset_dataset_path)

    all_trace_links = full_dataset.trace_df.get_links()
    source2links = RankingUtil.group_trace_predictions(all_trace_links, TraceKeys.SOURCE.value)
    target2links = RankingUtil.group_trace_predictions(all_trace_links, TraceKeys.TARGET.value)

    global_artifact_ids = list(subset_dataset.artifact_df.index)
    global_link_ids = []

    source_artifact_ids = list(subset_dataset.artifact_df.index)

    for i, layer in full_dataset.layer_df.itertuples():
        source_links = get_artifact_links(source_artifact_ids, source2links)
        source_link_ids = [t[TraceKeys.LINK_ID] for t in source_links]
        parent_ids = set([t[TraceKeys.parent_label()] for t in source_links])

        # selected_parent_ids = set()
        # for p_id in parent_ids:
        #     parent_links = sorted(target2links[p_id], key=lambda t: t[TraceKeys.SCORE], reverse=True)
        #     direct_links = [t for t in parent_links if t[TraceKeys.SCORE] >= DEFAULT_LINK_THRESHOLD]
        #     if len(direct_links) == 0:
        #         direct_links = [parent_links[0]]
        #     direct_children = [t[TraceKeys.SOURCE] for t in direct_links]
        #     if any([c in source_artifact_ids for c in direct_children]):
        #         selected_parent_ids.add(p_id)

        global_link_ids.extend(source_link_ids)
        global_artifact_ids.extend(parent_ids)

        logger.info(f"{layer[LayerKeys.TARGET_TYPE]}: {len(parent_ids)}")

        source_artifact_ids = parent_ids

    subset_artifact_df = full_dataset.artifact_df.filter_by_index(global_artifact_ids)
    subset_trace_df = full_dataset.trace_df.filter_by_index(global_link_ids)

    dataset = TraceDataset(artifact_df=subset_artifact_df, trace_df=subset_trace_df, layer_df=full_dataset.layer_df)
    exporter = SafaExporter(export_path, dataset=dataset)
    exporter.export()


if __name__ == "__main__":
    PROJECT = "dronology"
    METHOD = "baseline"
    FINAL_TYPE = {"dronology": "Functional Requirement", "safa": "Feature"}[PROJECT]

    FULL_PROJECT = f"papers/hgen/code/{PROJECT}/full/{FINAL_TYPE}"  # dataset in output path
    SUBSET_PROJECT = f"papers/hgen/code/{PROJECT}/subset"
    EXPORT_PROJECT = f"papers/hgen/official/{PROJECT}/{METHOD}"

    HGEN_OUTPUT_PATH = os.path.expanduser("~/desktop/safa/output/hgen")
    DATASET_PATH = os.path.expanduser("~/desktop/safa/datasets")

    full_path = os.path.join(HGEN_OUTPUT_PATH, METHOD, FULL_PROJECT, "final_generated_dataset/safa")
    subset_path = os.path.join(DATASET_PATH, SUBSET_PROJECT)
    export_path = os.path.join(DATASET_PATH, EXPORT_PROJECT)

    existing_files = os.listdir(export_path) if os.path.isdir(export_path) else []
    if len(existing_files) > 0:
        if "y" in input(f"{export_path} contains {len(existing_files)} files. Delete them?").lower():
            shutil.rmtree(export_path)

    os.makedirs(export_path, exist_ok=True)
    collect_subset(full_path, subset_path, export_path)
