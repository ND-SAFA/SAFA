from typing import List, Tuple

import math

from data.datasets.trace_dataset import TraceDataset
from data.splitting.abstract_trace_split_strategy import AbstractTraceSplitStrategy
from data.tree.trace_link import TraceLink
from util.override import overrides


class SourceSplitStrategy(AbstractTraceSplitStrategy):
    """
    Responsible for splitting a dataset while maximizing the number of
    source queries in validation set.
    """

    @staticmethod
    @overrides(AbstractTraceSplitStrategy)
    def create_split(dataset: TraceDataset, percent_split: float, slice_num: int) -> TraceDataset:
        """
        Creates a new trace data from the slice defined by the percent split.
        :param dataset: The trace dataset to split.
        :param percent_split: The percentage of links included in second slice.
        :param slice_num: Whether to return first or second slice.
        :return: the dataset split
        """
        first_slice_links, second_slice_links = SourceSplitStrategy.create_source_splits(dataset, percent_split)
        slice_links = first_slice_links if slice_num == 1 else second_slice_links
        slice_link_ids = [t.id for t in slice_links]
        return AbstractTraceSplitStrategy.create_dataset_slice(dataset, slice_link_ids)

    @staticmethod
    def create_source_splits(trace_dataset: TraceDataset, percent_split) \
            -> Tuple[List[TraceLink], List[TraceLink]]:
        """
        Creates an array of trace links constructed by contiguously placing trace links
        associated with a source artifact. Note, source artifacts are randomly selected.
        :param trace_dataset: The dataset whose trace links are put in array.
        :param percent_split: Percentage of source artifacts to include in second split.
        :return: Array of trace links.
        """
        source_names = trace_dataset.trace_matrix.source_ids
        slice_1_names, slice_2_names = AbstractTraceSplitStrategy.split_data(source_names, percent_split=percent_split)

        def create_slice(artifact_names):
            slice = []
            for source_name in artifact_names:
                source_links = trace_dataset.trace_matrix.query_matrix[source_name].links
                slice.extend(source_links)
            return slice

        return create_slice(slice_1_names), create_slice(slice_2_names)

    @staticmethod
    def create_trace_link_array_by_source(trace_dataset: TraceDataset, n_sources: int = None, n_links_per_source: int = None) \
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
            source_links = trace_dataset.trace_matrix.query_matrix[source_name].links
            links_per_query = min(len(source_links), n_links_per_source)
            query_links = source_links[:links_per_query]
            agg_links.extend(query_links)
        return agg_links
