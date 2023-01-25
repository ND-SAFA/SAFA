from config.override import overrides
from data.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.splitting.source_split_strategy import SourceSplitStrategy
from data.datasets.trace_dataset import TraceDataset


class CombinationSplitStrategy(AbstractSplitStrategy):
    """
    Responsible for splitting a dataset ensuring at least n_sources make it into the training set
    """

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(trace_dataset: TraceDataset, percent_split: float, slice_num: int, n_sources: int = 2) -> "TraceDataset":
        """
        Creates a new trace data from the slice defined by the percent split.
        :param trace_dataset: The trace dataset to split.
        :param percent_split: The percentage of links included in second slice.
        :param slice_num: Whether to return first or second slice.
        :param n_sources: Number of Source Artifacts to include
        :return: the dataset split
        """
        source_link_ids_first_split = {link.id for link
                                       in SourceSplitStrategy.create_random_trace_link_array(trace_dataset, n_sources=n_sources)}
        return AbstractSplitStrategy.create_split_containing_specified_link_ids(trace_dataset, source_link_ids_first_split,
                                                                                percent_split, slice_num)
