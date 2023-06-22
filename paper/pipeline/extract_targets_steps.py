import os

from paper.pipeline.base import create_artifact_map
from paper.pipeline.ranking_step import create_trace_queries, extract_prompt_artifacts
from paper.pipeline.sort_step import registered_sorters
from tgen.data.readers.structured_project_reader import StructuredProjectReader


def extract_related_target_artifacts(s):
    project_path = s.project_path
    project_path = os.path.expanduser(project_path)
    project_reader = StructuredProjectReader(project_path)
    artifact_df, _, _ = project_reader.read_project()
    artifact_map = create_artifact_map(artifact_df)
    if s.trace_entries is None:  # if using all targets, then sort them.
        source_names, target_names = extract_prompt_artifacts(artifact_df)
        target_artifact_sorter = registered_sorters[s.sorter]
        source2targets = target_artifact_sorter(source_names, target_names, artifact_map)  # sorts target names using sorter
    else:  # if filtering from previous run
        source2targets = create_trace_queries(s.trace_entries)
        source_names = list(source2targets.keys())
    s.artifact_map = artifact_map
    s.source2targets = source2targets
    s.target_ids = source2targets[source_names[0]]
    s.source_ids = source_names
