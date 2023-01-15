import math
from typing import List

from config.override import overrides
from data.datasets.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.datasets.trace_dataset import TraceDataset
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
        :return: the dataset split
        """
        links = SourceSplitStrategy.create_random_trace_link_array(trace_dataset)
        labels = [t.get_label() for t in links]
        first_slice_links, second_slice_links = AbstractSplitStrategy.split_data(links, percent_split, labels)
        slice_links = first_slice_links if slice_num == 1 else second_slice_links
        slice_links = {
            trace_link.id: trace_link for trace_link in slice_links
        }
        return TraceDataset(slice_links)

    @staticmethod
    def create_random_trace_link_array(trace_dataset: TraceDataset, n_sources: int = None, n_links_per_source: int = None) \
            -> List[TraceLink]:
        """
        Creates an array of trace links constructed by contiguously placing trace links
        associated with a source artifact. Note, source artifacts are randomly selected.
        :param trace_dataset: The dataset whose trace links are put in array.
        :param n_sources: The number of sources to include
        :param n_links_per_source: The number of links per source to include
        :return: Array of trace links.
        """
        source_names = trace_dataset.trace_matrix.source_ids
        n_sources = len(source_names) if n_sources is None else n_sources
        n_links_per_source = math.inf if n_links_per_source is None else n_links_per_source
        agg_links = []
        for source_name in source_names[:n_sources]:
            links = trace_dataset.trace_matrix.query_matrix[source_name].links
            links_per_query = min(len(links), n_links_per_source)
            agg_links.extend(links[:links_per_query])
        return agg_links
