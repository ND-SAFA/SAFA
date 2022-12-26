import os
from typing import Dict

import pandas as pd

from data.datasets.creators.readers.entity.entity_reader import EntityReader, EntityType
from data.datasets.creators.readers.project.structure_keys import StructureKeys
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink


class CSVSourceData:
    source_id: str = "source_id"
    source_body: str = "source"
    target_id: str = "target_id"
    target_body: str = "target"
    label: str = "label"


class CSVEntityReader(EntityReader):
    def __init__(self, data_path: str):
        base_path, file_path = os.path.split(data_path)
        super().__init__(base_path, {
            StructureKeys.PATH: file_path
        })

    def create(self, entity_df: pd.DataFrame) -> EntityType:
        source_artifact_mapping: Dict[str, Artifact] = {}
        target_artifact_mapping: Dict[str, Artifact] = {}

        def add_artifact(a_id: str, a_body: str, mapping):
            if a_id not in mapping:
                artifact = Artifact(a_id, a_body)
                mapping[a_id] = artifact
            return mapping[a_id]

        trace_links: Dict[int, TraceLink] = {}
        for row_index, row in entity_df.iterrows():
            source = add_artifact(
                row[CSVSourceData.source_id],
                row[CSVSourceData.source_body],
                source_artifact_mapping
            )
            target = add_artifact(
                row[CSVSourceData.target_id],
                row[CSVSourceData.target_body],
                target_artifact_mapping
            )
            label = row[CSVSourceData.label]
            is_true_link = int(label) == 1
            trace_link = TraceLink(source, target, is_true_link=is_true_link)
            trace_links[trace_link.id] = trace_link
        return trace_links
