from data.datasets.trace_dataset import TraceDataset
from data.splitting.abstract_trace_split_strategy import AbstractTraceSplitStrategy
from data.splitting.source_split_strategy import SourceSplitStrategy
from util.override import overrides


class AllSourcesSplitStrategy(AbstractTraceSplitStrategy):
    """
    Responsible for splitting a dataset randomly while ensuring each source appears once in training
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
        source_link_ids_first_split = {link.id for link
                                       in SourceSplitStrategy.create_trace_link_array_by_source(dataset, n_links_per_source=1)}
        return AbstractTraceSplitStrategy.create_split_containing_specified_link_ids(dataset, source_link_ids_first_split,
                                                                                     percent_split, slice_num)
