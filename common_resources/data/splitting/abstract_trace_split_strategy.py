from abc import ABC
from typing import List

from tqdm import tqdm

from common_resources.tools.constants.logging_constants import TQDM_NCOLS
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys, TraceKeys
from common_resources.data.splitting.abstract_split_strategy import AbstractSplitStrategy
from common_resources.data.tdatasets.trace_dataset import TraceDataset


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
        traces = {col: [] for col in TraceDataFrame.required_column_names()}
        artifacts = {col: [] for col in ArtifactDataFrame.required_column_names()}
        artifact_ids = set()
        for link_id in tqdm(slice_link_ids, desc="Creating data slices", ncols=TQDM_NCOLS):
            trace_link = trace_dataset.trace_df.get_link(link_id)
            source = trace_dataset.artifact_df.get_artifact(trace_link[TraceKeys.SOURCE])
            target = trace_dataset.artifact_df.get_artifact(trace_link[TraceKeys.TARGET])
            if trace_link[TraceKeys.LABEL] == 1:
                slice_pos_link_ids.append(trace_link[TraceKeys.LINK_ID])
            else:
                slice_neg_link_ids.append(trace_link[TraceKeys.LINK_ID])
            for col in TraceDataFrame.required_column_names():
                traces[col].append(trace_link[col])
            for artifact in [source, target]:
                if artifact[ArtifactKeys.ID] not in artifact_ids:
                    artifact_ids.add(artifact[ArtifactKeys.ID])
                    for col in ArtifactDataFrame.required_column_names():
                        artifacts[col].append(artifact[col])
        return TraceDataset(artifact_df=ArtifactDataFrame(artifacts), trace_df=TraceDataFrame(traces),
                            layer_df=trace_dataset.layer_df, pos_link_ids=slice_pos_link_ids,
                            neg_link_ids=slice_neg_link_ids)
