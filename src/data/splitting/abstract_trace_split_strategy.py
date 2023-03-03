from abc import ABC
from typing import List, Set, Union

from data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from data.dataframes.layer_dataframe import LayerDataFrame
from data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
from data.datasets.trace_dataset import TraceDataset
from data.splitting.abstract_split_strategy import AbstractSplitStrategy


class AbstractTraceSplitStrategy(AbstractSplitStrategy, ABC):
    """
    Representing a strategy for splitting a dataset.
    """

    @staticmethod
    def create_dataset_slice(trace_dataset: TraceDataset, slice_link_ids: List[int]) -> TraceDataset:
        """
        Creates dataset slice from trace dataset.
        :param trace_dataset: The dataset to extract slice from.
        :param slice_link_ids: The trace link ids in slice.
        :return: TraceDataset composed of links in split ids.
        """
        slice_pos_link_ids = []
        slice_neg_link_ids = []
        traces = {col: [] for col in TraceDataFrame.column_names()}
        artifacts = {col: [] for col in ArtifactDataFrame.column_names()}
        artifact_ids = set()
        for link_id in slice_link_ids:
            trace_link = trace_dataset.trace_df.get_link(link_id)
            source = trace_dataset.artifact_df.get_artifact(trace_link[TraceKeys.SOURCE])
            target = trace_dataset.artifact_df.get_artifact(trace_link[TraceKeys.TARGET])
            if trace_link[TraceKeys.LABEL]:
                slice_pos_link_ids.append(trace_link[TraceKeys.LINK_ID])
            else:
                slice_neg_link_ids.append(trace_link[TraceKeys.LINK_ID])
            for col in TraceDataFrame.column_names():
                traces[col].append(trace_link[col])
            for artifact in [source, target]:
                if artifact[ArtifactKeys.ID] not in artifact_ids:
                    artifact_ids.add(artifact[ArtifactKeys.ID])
                    for col in ArtifactDataFrame.column_names():
                        artifacts[col].append(artifact[col])
        return TraceDataset(artifact_df=ArtifactDataFrame(artifacts), trace_df=TraceDataFrame(traces),
                            layer_mapping_df=trace_dataset.layer_mapping_df, pos_link_ids=slice_pos_link_ids,
                            neg_link_ids=slice_neg_link_ids)
