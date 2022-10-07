import json
import os
from typing import List, Tuple

import pandas as pd

from experiment.gan.constants import CONTENT_PARAM, ID_PARAM, LHP_DATA_PATH, ProjectData, SOURCE_PARAM, TARGET_PARAM
from experiment.gan.data.common import create_data_df


def read_safa_project(artifact_levels: List[Tuple[str, str, str]]):
    sources = []
    targets = []
    labels = []
    for artifact_level in artifact_levels:
        if ".csv" in artifact_level[0]:
            level_sources, level_targets, layer_labels = read_csv_layer(artifact_level[0], artifact_level[1],
                                                                        artifact_level[2])
            sources.extend(level_sources)
            targets.extend(level_targets)
            labels.extend(layer_labels)
        elif ".json" in artifact_level[0]:
            level_sources, level_targets, layer_labels = read_json_layer(artifact_level[0], artifact_level[1],
                                                                         artifact_level[2])
            sources.extend(level_sources)
            targets.extend(level_targets)
            labels.extend(layer_labels)
    return create_data_df(sources, targets, labels)


def read_csv_layer(source_file_name: str, target_file_name: str, link_file_name: str) -> ProjectData:
    source_df = pd.read_csv(os.path.join(LHP_DATA_PATH, source_file_name))
    target_df = pd.read_csv(os.path.join(LHP_DATA_PATH, target_file_name))
    links_df = pd.read_csv(os.path.join(LHP_DATA_PATH, link_file_name))

    sources = []
    targets = []
    labels = []
    for source_index, source_item in source_df.iterrows():
        for target_index, target_item in target_df.iterrows():
            query = links_df[
                (links_df[SOURCE_PARAM] == source_item[ID_PARAM]) & (links_df[TARGET_PARAM] == target_item[ID_PARAM])]
            source_text = source_item[CONTENT_PARAM]
            source_id = source_item[ID_PARAM]
            target_text = target_item[CONTENT_PARAM]
            target_id = target_item[ID_PARAM]
            label = 1 if len(query) > 0 else 0

            sources.append((source_id, source_text))
            targets.append((target_id, target_text))
            labels.append(label)

    return sources, targets, labels


def read_json_layer(source_file_name: str, target_file_name: str, link_file_name: str) -> ProjectData:
    source_df = read_json_file(os.path.join(LHP_DATA_PATH, source_file_name))
    target_df = read_json_file(os.path.join(LHP_DATA_PATH, target_file_name))
    links_df = read_json_file(os.path.join(LHP_DATA_PATH, link_file_name))

    source_texts = []
    target_texts = []
    labels = []
    seen_traces = []
    for source_artifact in source_df["artifacts"]:
        for target_artifact in target_df["artifacts"]:
            source_name = source_artifact["name"]
            target_name = target_artifact["name"]
            trace_key = "%s-%s" % (source_name, target_name)
            if trace_key in seen_traces:
                continue
            query = list(filter(lambda t: t["sourceName"] == source_name and
                                          t["targetName"] == target_name,
                                links_df["traces"]))
            source_text = source_artifact["body"]
            source_id = source_artifact["name"]
            target_text = target_artifact["body"]
            target_id = source_artifact["name"]
            label = 1 if len(query) > 0 else 0

            source_texts.append((source_id, source_text))
            target_texts.append((target_id, target_text))
            labels.append(label)
            seen_traces.append(trace_key)

    return source_texts, target_texts, labels


def read_json_file(file_path: str):
    with open(file_path, "r") as json_file:
        return json.loads(json_file.read())
