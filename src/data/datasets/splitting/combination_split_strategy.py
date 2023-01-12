from typing import List, Set, Union

from sklearn.model_selection import train_test_split

from config.override import overrides
from data.datasets.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.datasets.splitting.source_split_strategy import SourceSplitStrategy
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
        return CombinationSplitStrategy.create_split_containing_specified_link_ids(trace_dataset, source_link_ids_first_split,
                                                                                   percent_split, slice_num)

    @staticmethod
    def create_split_containing_specified_link_ids(trace_dataset: TraceDataset, link_ids_for_first_split: Union[Set[str], List[str]],
                                                   percent_split: float, slice_num: int) -> "TraceDataset":
        """
        Creates a new trace data from the slice defined by the percent split.
        :param trace_dataset: The trace dataset to split.
        :param link_ids_for_first_split: A set of link ids to include in the first split
        :param percent_split: The percentage of links included in second slice.
        :param slice_num: Whether to return first or second slice.
        :return: the dataset split
        """
        all_link_ids = (trace_dataset.pos_link_ids + trace_dataset.neg_link_ids)
        remaining_link_ids = [link_id for link_id in all_link_ids if link_id not in link_ids_for_first_split]
        labels = [1 if trace_dataset.links[t_id].is_true_link else 0 for t_id in remaining_link_ids]
        first_split_link_ids, second_split_link_ids = train_test_split(remaining_link_ids, test_size=percent_split, stratify=labels)
        random_link_ids = first_split_link_ids if slice_num == 1 else second_split_link_ids

        if slice_num == 1:
            split_links_ids = list(link_ids_for_first_split) + random_link_ids
        else:
            split_links_ids = random_link_ids if len(random_link_ids) > 0 else remaining_link_ids
        slice_links = {
            link_id: trace_dataset.links[link_id] for link_id in split_links_ids
        }
        return TraceDataset(slice_links)
