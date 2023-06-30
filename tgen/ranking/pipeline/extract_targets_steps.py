import os
import random

from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.ranking.pipeline.base import RankingStore, create_artifact_map
from tgen.ranking.pipeline.sort_step import registered_sorters
from tgen.ranking.pipeline.utils import extract_prompt_artifacts


def extract_related_target_artifacts(s: RankingStore):
    project_path = s.project_path
    project_path = os.path.expanduser(project_path)
    project_reader = StructuredProjectReader(project_path)
    artifact_df, trace_df, _ = project_reader.read_project()
    artifact_map = create_artifact_map(artifact_df)
    total = 15
    if s.experiment:
        source_names, target_names = extract_prompt_artifacts(artifact_df)
        source2targets = {}
        for source in source_names:
            positive_targets, negative_targets = [], []
            for target in target_names:
                source_query = trace_df[TraceKeys.SOURCE.value] == source
                target_query = trace_df[TraceKeys.TARGET.value] == target
                query = trace_df[source_query & target_query]
                if len(query) == 0:
                    negative_targets.append(target)
                    continue
                label = query[TraceKeys.LABEL.value].iloc[0]
                if label == 0:
                    negative_targets.append(target)
                else:
                    positive_targets.append(target)

            source2targets[source] = positive_targets
            n_missing = total - len(source2targets[source])
            source2targets[source] += negative_targets[:n_missing]
            random.shuffle(source2targets[source])
        source_names = list(source2targets.keys())
    elif s.sorter is not None:  # if using all targets, then sort them.
        source_names, target_names = extract_prompt_artifacts(artifact_df)
        target_artifact_sorter = registered_sorters[s.sorter]
        source2targets = target_artifact_sorter(source_names, target_names, artifact_map)  # sorts target names using sorter
    else:  # if filtering from previous run
        source2targets = create_trace_queries(s.trace_entries)
        source_names = list(source2targets.keys())
    s.artifact_map = artifact_map
    s.source2targets = source2targets
    s.all_target_ids = target_names
    s.source_ids = source_names


def create_trace_queries(entries):
    entry_map = {}
    for entry in entries:
        source = entry["source"]
        target = entry["target"]
        if source not in entry_map:
            entry_map[source] = []
        entry_map[source].append(target)
    return entry_map
