from abc import ABC, abstractmethod
from typing import List, Set, Tuple, TypeVar, Union

from sklearn.model_selection import train_test_split

from data.datasets.trace_dataset import TraceDataset

GenericDatum = TypeVar("GenericData")
GenericData = List[GenericDatum]


class AbstractSplitStrategy(ABC):
    """
    Representing a strategy for splitting a dataset.
    """

    @staticmethod
    @abstractmethod
    def create_split(trace_dataset: TraceDataset, percent_split: float, slice_num: int) -> TraceDataset:
        """
        Creates the split of the dataset
        :param trace_dataset: The dataset to split.
        :type percent_split: The percentage of the dataset contained in the second split.
        :type slice_num: The slice number to return.
        :return: TraceDatset containing slice of data.
        """
        raise NotImplementedError()

    @staticmethod
    def split_data(data: GenericData, percent_split: float, labels: List[int] = None, **kwargs) -> Tuple[GenericData, GenericData]:
        """
        Splits data into slices using labels to guarantee equal proportions of the labels in each split
        :param data: The data to split.
        :param percent_split: The percentage of the data to be contained in second split
        :param labels: The labels to stratify data with.
        :return: Two slices of data.
        """
        return train_test_split(data, test_size=percent_split, stratify=labels, random_state=0, **kwargs)

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

        # Adjust percentage to account for links selected for first split
        first_split_size = len(all_link_ids) * (1 - percent_split)
        remaining_links_in_first_split = first_split_size - len(link_ids_for_first_split)
        new_split_size = 1 - (remaining_links_in_first_split / len(remaining_link_ids))

        labels = [trace_dataset.links[t_id].get_label() for t_id in remaining_link_ids]
        first_split_link_ids, second_split_link_ids = AbstractSplitStrategy.split_data(remaining_link_ids, new_split_size, labels)
        random_link_ids = first_split_link_ids if slice_num == 1 else second_split_link_ids

        if slice_num == 1:
            slice_link_ids = list(link_ids_for_first_split) + random_link_ids
        else:
            slice_link_ids = random_link_ids if len(random_link_ids) > 0 else remaining_link_ids

        return AbstractSplitStrategy.create_dataset_slice(trace_dataset, slice_link_ids)

    @staticmethod
    def create_dataset_slice(trace_dataset: TraceDataset, slice_link_ids: List[int]) -> TraceDataset:
        """
        Creates dataset slice from trace dataset.
        :param trace_dataset: The dataset to extract slice from.
        :param slice_link_ids: The trace link ids in slice.
        :return: TraceDataset composed of links in split ids.
        """
        slice_pos_link_ids = []
        slice_neg_link_ids = []
        slice_links = {}
        for link_id in slice_link_ids:
            trace_link = trace_dataset.links[link_id]
            if trace_link.is_true_link:
                slice_pos_link_ids.append(trace_link.id)
            else:
                slice_neg_link_ids.append(trace_link.id)
            slice_links[trace_link.id] = trace_link

        return TraceDataset(slice_links, pos_link_ids=slice_pos_link_ids, neg_link_ids=slice_neg_link_ids)
