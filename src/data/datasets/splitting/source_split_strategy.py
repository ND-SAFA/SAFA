import random
from typing import Dict, List

from config.override import overrides
from data.datasets.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.datasets.trace_dataset import TraceDataset
from data.datasets.trace_matrix import TraceMatrixManager
from data.tree.trace_link import TraceLink


class SourceSplitStrategy(AbstractSplitStrategy):
    """
    Responsible for splitting a dataset while maximizing the number of
    source queries in validation set.
    """

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(trace_dataset: TraceDataset, percent_split: float, slice_num: int) -> "TraceDataset":
        """
        Creates a new trace data from the slice defined by the percent split.
        :param trace_dataset: The trace dataset to split.
        :param percent_split: The percentage of links included in second slice.
        :param slice_num: Whether to return first or second slice.
        :return:
        """
        slice_percent_split = 1 - percent_split if slice_num == 1 else percent_split
        split_size = round(len(trace_dataset.links.values()) * slice_percent_split)

        links = SourceSplitStrategy.create_random_trace_link_array(trace_dataset)
        slice_links = links[:split_size] if slice_num == 1 else links[split_size:]

        slice_links = {
            trace_link.id: trace_link for trace_link in slice_links
        }
        return TraceDataset(slice_links)

    @staticmethod
    def create_random_trace_link_array(trace_dataset: TraceDataset) -> List[TraceLink]:
        """
        Creates an array of trace links constructed by contiguously placing trace links
        associated with a source artifact. Note, source artifacts are randomly selected.
        :param trace_dataset: The dataset whose trace links are put in array.
        :return: Array of trace links.
        """
        source_queries = TraceMatrixManager(trace_dataset.links.values()).query_matrix
        source_names = list(source_queries.keys())
        random.shuffle(source_names)
        agg_links = []
        for source_name in source_names:
            agg_links.extend(source_queries[source_name][TraceMatrixManager.LINK_KEY])
        return agg_links
