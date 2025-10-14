import os.path
from typing import Dict, List

import pandas as pd

from gen_common.constants.dataset_constants import NO_CHECK
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.csv_keys import CSVKeys
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader, TraceDataFramesTypes
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.dataframe_util import DataFrameUtil
from gen_common.util.enum_util import EnumDict
from gen_common.util.file_util import FileUtil
from gen_common.util.list_util import ListUtil
from gen_common.util.thread_util import ThreadUtil


class CsvProjectReader(AbstractProjectReader[TraceDataFramesTypes]):
    """
    Responsible for reading trace links and artifacts from CSV file.
    """

    LAYER_ID = "CSV_LAYER_ID"

    def __init__(self, project_path: str, overrides: dict = None):
        """
        Creates reader targeted at reading entries located at given path.
        :param project_path: Path to data file containing entity entries.
        :param overrides: Parameters to override in the project creator.
        """
        super().__init__(overrides, project_path)
        self.overrides["allowed_orphans"] = NO_CHECK

    def read_project(self, n_threads: int = 1) -> TraceDataFramesTypes:
        """
        Reads csv containing trace links and constructs separate data frames containing artifacts and trace links.
        :param n_threads: The number of threads to use to read in traces in project.
        :return: Artifact and Trace DataFrame
        """
        logger.info(f"Reading file: {self.get_full_project_path()}")
        trace_df = pd.read_csv(self.get_full_project_path())
        trace_df_entries = []
        artifact_df_entries = {}
        project_name = os.path.basename(self.get_full_project_path())

        def read_trace_row(row_batches: List[int]) -> None:
            """
            Reads rows in trace data frame and processes their artifacts.
            :param row_batches: The list of row indices to process.
            :return: None.
            """
            for row_index in row_batches:
                trace_row = trace_df.iloc[row_index]
                source_id = trace_row[CSVKeys.SOURCE_ID]
                target_id = trace_row[CSVKeys.TARGET_ID]
                self.add_artifact(source_id,
                                  trace_row[CSVKeys.SOURCE],
                                  CSVKeys.SOURCE,
                                  artifact_df_entries)
                self.add_artifact(target_id,
                                  trace_row[CSVKeys.TARGET],
                                  CSVKeys.TARGET,
                                  artifact_df_entries)
                trace_df_entries.append({
                    StructuredKeys.Trace.SOURCE.value: source_id,
                    StructuredKeys.Trace.TARGET.value: target_id,
                    StructuredKeys.Trace.LABEL.value: trace_row[CSVKeys.LABEL]
                })

        index_batches = ListUtil.batch(list(range(len(trace_df))), 1000)
        ThreadUtil.multi_thread_process(f"Reading {project_name}", index_batches, read_trace_row, n_threads)

        artifact_df = ArtifactDataFrame(artifact_df_entries)
        if self.summarizer is not None:
            artifact_df.summarize_content(self.summarizer)
        trace_df = TraceDataFrame(trace_df_entries)  # TODO: Order might be messed up because threading.
        layer_mapping_df = LayerDataFrame([EnumDict({
            StructuredKeys.LayerMapping.SOURCE_TYPE: self.get_layer_id(CSVKeys.SOURCE),
            StructuredKeys.LayerMapping.TARGET_TYPE: self.get_layer_id(CSVKeys.TARGET),
        })])
        return artifact_df, trace_df, layer_mapping_df

    def get_project_name(self) -> str:
        """
        :return: Returns the file name of the csv file.
        """
        return FileUtil.get_file_name(self.get_full_project_path())

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
        if StructuredKeys.Artifact.ID.value not in artifact_df_entries \
                or a_id not in artifact_df_entries[StructuredKeys.Artifact.ID.value]:
            DataFrameUtil.append(artifact_df_entries, EnumDict({
                StructuredKeys.Artifact.ID: a_id,
                StructuredKeys.Artifact.CONTENT: a_body,
                StructuredKeys.Artifact.LAYER_ID: CsvProjectReader.get_layer_id(artifact_type)
            }))

    @staticmethod
    def get_layer_id(artifact_type: str) -> str:
        """
        Returns the identifier for the layer containing artifact type.
        :param artifact_type: The name of the type of artifact.
        :return: Layer ID.
        """
        return f"{artifact_type}_{CsvProjectReader.LAYER_ID}"
