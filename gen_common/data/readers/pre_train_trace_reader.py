import os
import random
import uuid
from typing import List

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys, LayerKeys, TraceKeys
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader, TraceDataFramesTypes
from gen_common.util.file_util import FileUtil


class PreTrainTraceReader(AbstractProjectReader[TraceDataFramesTypes]):
    LAYER_ID = uuid.uuid4()

    def __init__(self, data_file: str, overrides: dict = None):
        """
        Creates reader for pre-training text documents to be converted to trace dataset format.
        :param data_file: Path to data file containing pre-training text.
        :param overrides: Parameters to override in the project creator.
        """
        super().__init__(overrides)
        self.data_file = data_file

    def read_project(self) -> TraceDataFramesTypes:
        """
        Reads a text file and converts to the trace format
        :return:
        """
        artifact_df = self._get_artifact_df(self.data_file)
        if self.summarizer is not None:
            artifact_df.summarize_content(self.summarizer)
        trace_df = self._get_trace_df(list(artifact_df.index))
        layer_df = self._get_layer_dataframe()
        return artifact_df, trace_df, layer_df

    def get_project_name(self) -> str:
        """
        Gets the name of the project
        :return: The name of the project
        """
        base_path, filename = FileUtil.split_base_path_and_filename(self.data_file)
        proj_name = os.path.splitext(filename)[0]
        return proj_name

    @staticmethod
    def _get_artifact_df(data_file: str) -> ArtifactDataFrame:
        """
        Gets the dataframe of artifacts (paragraphs)
        :param data_file: The data file to use for the project
        :return: The dataframe of artifacts (paragraphs)
        """
        content = PreTrainTraceReader._read_paragraphs_from_file(data_file)
        all_ids = [i for i in range(len(content))]
        return ArtifactDataFrame({ArtifactKeys.ID: all_ids,
                                  ArtifactKeys.CONTENT: content,
                                  ArtifactKeys.LAYER_ID: [PreTrainTraceReader.LAYER_ID for i in range(len(content))]})

    @staticmethod
    def _get_trace_df(artifact_ids: List[int]) -> TraceDataFrame:
        """
        Gets a dataframe of all project traces
        :param artifact_ids: A list of project artifact ids
        :return: A dataframe of all project traces
        """
        sources, targets, labels = [], [], []

        def add_new_link(source_id: str, target_id: str, label=1) -> None:
            """
            Adds new links between source and target with given label.
            :param source_id: ID of source artifact.
            :param target_id: ID of target artifact.
            :param label: Label between source and target.
            :return: None
            """
            sources.append(source_id)
            targets.append(target_id)
            labels.append(label)

        for s_id in artifact_ids:
            n_pos_links = 0
            prev_id, next_id = s_id - 1, s_id + 1
            if prev_id >= 0:
                add_new_link(s_id, prev_id)
                n_pos_links += 1
            if next_id < len(artifact_ids):
                add_new_link(s_id, next_id)
                n_pos_links += 1
            neg_target_ids = random.sample([*range(prev_id), *range(next_id + 1, len(artifact_ids))], k=n_pos_links)
            for t_id in neg_target_ids:
                add_new_link(s_id, t_id, label=0)

        return TraceDataFrame({TraceKeys.SOURCE: sources,
                               TraceKeys.TARGET: targets,
                               TraceKeys.LABEL: labels})

    @staticmethod
    def _get_layer_dataframe() -> LayerDataFrame:
        """
        Gets a dataframe of all layer mappings in the project
        :return: A dataframe of all layer mappings in the project
        """
        return LayerDataFrame({LayerKeys.SOURCE_TYPE: [PreTrainTraceReader.LAYER_ID],
                               LayerKeys.TARGET_TYPE: [PreTrainTraceReader.LAYER_ID]})

    @staticmethod
    def _read_paragraphs_from_file(data_file: str) -> List[str]:
        """
        Reads the file and returns the contents split by paragraphs
        :param data_file: The data file to use for the project
        :return: A list of paragraph contents
        """
        with open(data_file, encoding='unicode_escape') as file:
            return file.readlines()
