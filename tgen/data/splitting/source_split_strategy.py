import math
from typing import List, Tuple

from tgen.common.util.override import overrides
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.splitting.abstract_split_strategy import AbstractSplitStrategy
from tgen.data.splitting.abstract_trace_split_strategy import AbstractTraceSplitStrategy
from tgen.data.tdatasets.trace_dataset import TraceDataset


class SourceSplitStrategy(AbstractTraceSplitStrategy):
    """
    Responsible for splitting a dataset while maximizing the number of
    source queries in validation set.
    """

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(dataset: TraceDataset, second_split_percentage: float) -> Tuple[TraceDataset, TraceDataset]:
        """
        Creates the split of the dataset
        :param dataset: The dataset to split.
        :param second_split_percentage: The percentage of the data to be contained in second split
        :return: Dataset containing slice of data.
        """
        links = SourceSplitStrategy.create_trace_link_array_by_source(dataset)
        first_slice_links, second_slice_links = AbstractTraceSplitStrategy.split_data(links, second_split_percentage,
                                                                                      shuffle=False)
        slice1 = AbstractTraceSplitStrategy.create_dataset_slice(dataset, [t[TraceKeys.LINK_ID] for t in first_slice_links])
        slice2 = AbstractTraceSplitStrategy.create_dataset_slice(dataset, [t[TraceKeys.LINK_ID] for t in second_slice_links])
        return slice1, slice2

    @staticmethod
    def create_trace_link_array_by_source(trace_dataset: TraceDataset, n_sources: int = None, n_links_per_source: int = None) \
            -> List[TraceDataFrame]:
        """
        Creates an array of trace links constructed by contiguously placing trace links
        associated with a source artifact. Note, source artifacts are randomly selected.
        :param trace_dataset: The dataset whose trace links are put in array.
        :param n_sources: The number of sources to include
        :param n_links_per_source: The number of links per source to include
        :return: Array of trace links.
        """
        trace_matrix = trace_dataset.get_trace_matrix()
        parent_ids = list(trace_matrix.parent_ids)
        n_sources = len(parent_ids) if n_sources is None else n_sources
        n_links_per_source = math.inf if n_links_per_source is None else n_links_per_source
        agg_links = []
        for parent_id in parent_ids[:n_sources]:
            source_links = trace_matrix.query_matrix[parent_id].links  # TODO: Randomize source links
            links_per_query = min(len(source_links), n_links_per_source)
            query_links = source_links[:links_per_query]
            agg_links.extend(query_links)
        return agg_links
