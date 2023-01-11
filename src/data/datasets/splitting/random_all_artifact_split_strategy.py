import random
from typing import List

from config.override import overrides
from data.datasets.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.datasets.splitting.combination_split_strategy import CombinationSplitStrategy
from data.datasets.trace_dataset import TraceDataset
from data.tree.trace_link import TraceLink


class RandomAllArtifactSplitStrategy(AbstractSplitStrategy):
    """
    Responsible for splitting a dataset randomly while ensuring each source and target appears once in training.
    """

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(trace_dataset: TraceDataset, percent_split: float, slice_num: int) -> "TraceDataset":
        """
        Creates a new trace data from the slice defined by the percent split referencing all artifacts in trace dataset.
        :param trace_dataset: The trace dataset to split.
        :param percent_split: The percentage of links included in second slice.
        :param slice_num: Whether to return first or second slice.
        :return: the dataset split
        """

        sources_seen = []
        targets_seen = []
        required_links = []
        links: List[TraceLink] = list(trace_dataset.links.values())
        random.shuffle(links)

        for trace_link in links:
            source_id = trace_link.source.id
            target_id = trace_link.target.id
            new_source = RandomAllArtifactSplitStrategy.add_if_new(sources_seen, source_id)
            new_target = RandomAllArtifactSplitStrategy.add_if_new(targets_seen, target_id)
            if new_source or new_target:
                required_links.append(trace_link.id)
                
        if percent_split * len(links) < len(required_links):
            raise ValueError(f"Referencing all artifacts led to split greater than percentage desired: {percent_split}.")

        return CombinationSplitStrategy.create_split_containing_specified_link_ids(trace_dataset, required_links,
                                                                                   percent_split, slice_num)

    @staticmethod
    def add_if_new(seen_list, new_item) -> bool:
        """
        Adds new item if not in list.
        :param seen_list: The list to check if item is present.
        :param new_item: The new item to add to list.
        :return: True if new item added False otherwise.
        """
        if new_item not in seen_list:
            seen_list.append(new_item)
            return True
        return False
