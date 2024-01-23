import os.path
from os.path import dirname
from typing import Dict, List

import numpy as np

from tgen.common.logging.logger_manager import logger
from tgen.common.objects.trace import Trace
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.structure_keys import LayerKeys, TraceKeys, ArtifactKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hierarchy_generator import HierarchyGenerator
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


def collect_subset(full_dataset_path: str, subset_dataset_path: str, export_dir: str, state_path: str):
    full_dataset = read_dataset(full_dataset_path)
    subset_dataset = read_dataset(subset_dataset_path)
    state = HGenState.load_latest(state_path, [s.get_step_name() for s in HierarchyGenerator.steps])
    source_clusters = state.get_cluster2artifacts(ids_only=True)
    parent_clusters = {}
    for c_id, generations in state.get_cluster2generation().items():
        for g in generations:
            parent_clusters[g] = c_id

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

        selected_parent_ids = set()
        if i == 0:
            for p_id in parent_ids:
                content = full_dataset.artifact_df.get_artifact(p_id)[ArtifactKeys.CONTENT]
                c_id = parent_clusters[content]
                sources_from_cluster = source_clusters[c_id]
                if any([c in source_artifact_ids for c in sources_from_cluster]):
                    selected_parent_ids.add(p_id)
        else:
            selected_parent_ids = parent_ids

        global_link_ids.extend(source_link_ids)
        global_artifact_ids.extend(selected_parent_ids)

        logger.info(f"{layer[LayerKeys.TARGET_TYPE]}: {len(selected_parent_ids)}")

        source_artifact_ids = selected_parent_ids

    subset_artifact_df = full_dataset.artifact_df.filter_by_index(global_artifact_ids)
    subset_trace_df = full_dataset.trace_df.filter_by_index(global_link_ids)

    dataset = TraceDataset(artifact_df=subset_artifact_df, trace_df=subset_trace_df, layer_df=full_dataset.layer_df)
    exporter = SafaExporter(export_path, dataset=dataset)
    exporter.export()


if __name__ == "__main__":
    PROJECT = "safa"
    METHOD = "clustering"
    FINAL_TYPE = {"dronology": "Functional Requirement", "safa": "Feature"}[PROJECT]
    FIRST_TYPE = {"safa": "Functional Requirement", "dronology": "Design Requirement"}[PROJECT]

    FULL_PROJECT = f"papers/hgen/code/{PROJECT}/full/{FINAL_TYPE}"  # dataset in output path
    SUBSET_PROJECT = f"papers/hgen/code/{PROJECT}/subset"
    EXPORT_PROJECT = f"papers/hgen/official/{PROJECT}/{METHOD}"

    HGEN_OUTPUT_PATH = os.path.expanduser("~/desktop/safa/output/hgen")
    DATASET_PATH = os.path.expanduser("~/desktop/safa/datasets")

    full_path = os.path.join(HGEN_OUTPUT_PATH, METHOD, FULL_PROJECT, "final_generated_dataset/safa")
    state_path = os.path.join(dirname(dirname(dirname(full_path))), FIRST_TYPE)
    subset_path = os.path.join(DATASET_PATH, SUBSET_PROJECT)
    export_path = os.path.join(DATASET_PATH, EXPORT_PROJECT)
    os.makedirs(export_path, exist_ok=True)

    collect_subset(full_path, subset_path, export_path, state_path)
