import os
from typing import Dict

import pandas as pd

from data.datasets.creators.readers.entity.entity_reader import EntityReader, EntityType
from data.datasets.keys.csv_format import CSVKeys
from data.datasets.keys.structure_keys import StructureKeys
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink


class CSVEntityReader(EntityReader):
    """
    Responsible for reading trace links and artifacts from CSV file.
    """

    def __init__(self, data_path: str):
        """
        Creates reader targeted at reading entries located at given path.
        :param data_path: Path to data file containing entity entries.
        """
        base_path, file_path = os.path.split(data_path)
        super().__init__(base_path, {
            StructureKeys.PATH: file_path
        })

    @staticmethod
    def add_artifact(a_id: str, a_body: str, mapping) -> str:
        """
        Adds artifact entry to mapping if not already present.
        :param a_id: The artifact id used to check if artifact entry exists.
        :param a_body: The artifact body to store in mapping if entry does not exist.
        :param mapping: The mapping containing artifact ids as keys and artifact body's as values.
        :return: The artifact body of the entry added.
        """
        if a_id not in mapping:
            artifact = Artifact(a_id, a_body)
            mapping[a_id] = artifact
        return mapping[a_id]

    def create(self, entity_df: pd.DataFrame) -> EntityType:
        """
        Creates trace links and artifacts from data frame.
        :param entity_df: The data frame enumerating all candidate links.
        :return: Trace Links, positive link ids, and negative link ids.
        """
        source_artifact_mapping: Dict[str, Artifact] = {}
        target_artifact_mapping: Dict[str, Artifact] = {}

        trace_links: Dict[int, TraceLink] = {}
        pos_link_ids = []
        neg_link_ids = []
        for _, row in entity_df.iterrows():
            source = self.add_artifact(
                row[CSVKeys.SOURCE_ID],
                row[CSVKeys.SOURCE],
                source_artifact_mapping
            )
            target = self.add_artifact(
                row[CSVKeys.TARGET_ID],
                row[CSVKeys.TARGET],
                target_artifact_mapping
            )
            label = row[CSVKeys.LABEL]
            is_true_link = int(label) == 1
            trace_link = TraceLink(source, target, is_true_link=is_true_link)
            trace_links[trace_link.id] = trace_link
            if is_true_link:
                pos_link_ids.append(trace_link.id)
            else:
                neg_link_ids.append(trace_link.id)
        return trace_links, pos_link_ids, neg_link_ids
