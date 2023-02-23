from abc import ABC
from typing import List, Set, Union

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
        slice_links = {}
        for link_id in slice_link_ids:
            trace_link = trace_dataset.links[link_id]
            if trace_link.is_true_link:
                slice_pos_link_ids.append(trace_link.id)
            else:
                slice_neg_link_ids.append(trace_link.id)
            slice_links[trace_link.id] = trace_link

        return TraceDataset(slice_links, pos_link_ids=slice_pos_link_ids, neg_link_ids=slice_neg_link_ids)
