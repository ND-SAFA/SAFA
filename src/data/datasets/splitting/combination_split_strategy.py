from config.override import overrides
from data.datasets.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.datasets.splitting.source_split_strategy import SourceSplitStrategy
from data.datasets.trace_dataset import TraceDataset


class CombinationSplitStrategy(AbstractSplitStrategy):
    """
    Responsible for splitting a dataset while maximizing the number of
    source queries in validation set.
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
        all_link_ids = (trace_dataset.pos_link_ids + trace_dataset.neg_link_ids)
        remaining_link_ids = [link_id for link_id in all_link_ids if link_id not in source_link_ids_first_split]
        split_size = CombinationSplitStrategy.get_first_split_size(all_link_ids, percent_split) - len(source_link_ids_first_split)
        random_link_ids = CombinationSplitStrategy.get_data_split(remaining_link_ids, for_second_split=slice_num == 2,
                                                                  split_size=split_size) if split_size > 0 else []
        if slice_num == 1:
            split_links_ids = list(source_link_ids_first_split) + random_link_ids
        else:
            split_links_ids = random_link_ids if len(random_link_ids) > 0 else remaining_link_ids
        slice_links = {
            link_id: trace_dataset.links[link_id] for link_id in split_links_ids
        }
        return TraceDataset(slice_links)
