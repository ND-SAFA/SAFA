from typing import Tuple

import pandas as pd

from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.keys.csv_format import CSVKeys
from data.datasets.keys.structure_keys import StructureKeys


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
        artifact_df = pd.DataFrame(columns=StructureKeys.get_artifact_cols())
        trace_df = pd.DataFrame()
        for _, row in entity_df.iterrows():
            source_id = row[CSVKeys.SOURCE_ID]
            target_id = row[CSVKeys.TARGET_ID]
            artifact_df = self.add_artifact(source_id,
                                            row[CSVKeys.SOURCE],
                                            CSVKeys.SOURCE,
                                            artifact_df)
            artifact_df = self.add_artifact(target_id,
                                            row[CSVKeys.TARGET],
                                            CSVKeys.TARGET,
                                            artifact_df)
            trace_df = trace_df.append({
                StructureKeys.Trace.SOURCE: source_id,
                StructureKeys.Trace.TARGET: target_id,
                StructureKeys.Trace.LABEL: row[CSVKeys.LABEL]
            }, ignore_index=True)
        layer_mapping_df = pd.DataFrame([{
            StructureKeys.LayerMapping.SOURCE_TYPE: self.get_layer_id(CSVKeys.SOURCE),
            StructureKeys.LayerMapping.TARGET_TYPE: self.get_layer_id(CSVKeys.TARGET),
        }])
        artifact_df = artifact_df.sort_values([StructureKeys.Artifact.LAYER_ID, StructureKeys.Artifact.ID]).reset_index()
        return artifact_df, trace_df, layer_mapping_df

    @staticmethod
    def should_generate_negative_links() -> bool:
        """
        Defines that negative links are already included in trace DataFrame
        :return: False
        """
        return False

    @staticmethod
    def add_artifact(a_id: str, a_body: str, artifact_type: str, artifact_df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds artifact entry to DataFrame if not already present.
        :param a_id: The artifact id used to check if artifact entry exists.
        :param a_body: The artifact body to store in mapping if entry does not exist.
        :param artifact_type: The name of type of artifact.
        :param artifact_df: DataFrame containing entries for each artifact processed.
        :return: The artifact body of the entry added.
        """
        if a_id not in artifact_df[StructureKeys.Artifact.ID].values:
            artifact_df = artifact_df.append({
                StructureKeys.Artifact.ID: a_id,
                StructureKeys.Artifact.BODY: a_body,
                StructureKeys.Artifact.LAYER_ID: CsvProjectReader.get_layer_id(artifact_type)
            }, ignore_index=True)
        return artifact_df

    @staticmethod
    def get_layer_id(artifact_type: str) -> str:
        """
        Returns the identifier for the layer containing artifact type.
        :param artifact_type: The name of the type of artifact.
        :return: Layer ID.
        """
        return f"{artifact_type}_{CsvProjectReader.LAYER_ID}"
