from typing import Dict, Tuple

import pandas as pd

from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.keys.csv_format import CSVKeys
from data.datasets.keys.structure_keys import StructuredKeys
from util.dataframe_util import DataFrameUtil


class CsvProjectReader(AbstractProjectReader):
    """
    Responsible for reading trace links and artifacts from CSV file.
    """
    LAYER_ID = "CSV_LAYER_ID"

    def __init__(self, data_path: str):
        """
        Creates reader targeted at reading entries located at given path.
        :param data_path: Path to data file containing entity entries.
        """
        self.data_path = data_path

    def read_project(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Reads csv containing trace links and constructs separate data frames containing artifacts and trace links.
        :return: Artifact and Trace DataFrame
        """
        entity_df = pd.read_csv(self.data_path)
        trace_df_entries = []
        artifact_df_entries = {}
        for _, row in entity_df.iterrows():
            source_id = row[CSVKeys.SOURCE_ID]
            target_id = row[CSVKeys.TARGET_ID]
            self.add_artifact(source_id,
                              row[CSVKeys.SOURCE],
                              CSVKeys.SOURCE,
                              artifact_df_entries)
            self.add_artifact(target_id,
                              row[CSVKeys.TARGET],
                              CSVKeys.TARGET,
                              artifact_df_entries)
            trace_df_entries.append({
                StructuredKeys.Trace.SOURCE: source_id,
                StructuredKeys.Trace.TARGET: target_id,
                StructuredKeys.Trace.LABEL: row[CSVKeys.LABEL]
            })
        trace_df = pd.DataFrame(trace_df_entries)
        layer_mapping_df = pd.DataFrame([{
            StructuredKeys.LayerMapping.SOURCE_TYPE: self.get_layer_id(CSVKeys.SOURCE),
            StructuredKeys.LayerMapping.TARGET_TYPE: self.get_layer_id(CSVKeys.TARGET),
        }])
        artifact_df = pd.DataFrame(artifact_df_entries)
        return artifact_df, trace_df, layer_mapping_df

    @staticmethod
    def should_generate_negative_links() -> bool:
        """
        Defines that negative links are already included in trace DataFrame
        :return: False
        """
        return False

    @staticmethod
    def add_artifact(a_id: str, a_body: str, artifact_type: str, artifact_df_entries: Dict):
        """
        Adds artifact entry to DataFrame if not already present.
        :param a_id: The artifact id used to check if artifact entry exists.
        :param a_body: The artifact body to store in mapping if entry does not exist.
        :param artifact_type: The name of type of artifact.
        :param artifact_df_entries: DataFrame containing entries for each artifact processed.
        """
        if StructuredKeys.Artifact.ID not in artifact_df_entries or a_id not in artifact_df_entries[StructuredKeys.Artifact.ID]:
            DataFrameUtil.append(artifact_df_entries, {
                StructuredKeys.Artifact.ID: a_id,
                StructuredKeys.Artifact.BODY: a_body,
                StructuredKeys.Artifact.LAYER_ID: CsvProjectReader.get_layer_id(artifact_type)
            })

    @staticmethod
    def get_layer_id(artifact_type: str) -> str:
        """
        Returns the identifier for the layer containing artifact type.
        :param artifact_type: The name of the type of artifact.
        :return: Layer ID.
        """
        return f"{artifact_type}_{CsvProjectReader.LAYER_ID}"
