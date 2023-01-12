from config.override import overrides
from data.datasets.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.datasets.splitting.source_split_strategy import SourceSplitStrategy
from data.datasets.trace_dataset import TraceDataset


class AllSourcesSplitStrategy(AbstractSplitStrategy):
    """
    Responsible for splitting a dataset randomly while ensuring each source appears once in training
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
        source_link_ids_first_split = {link.id for link
                                       in SourceSplitStrategy.create_random_trace_link_array(trace_dataset, n_links_per_source=1)}
        return AbstractSplitStrategy.create_split_containing_specified_link_ids(trace_dataset, source_link_ids_first_split,
                                                                                percent_split, slice_num)
