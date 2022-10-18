import random
from typing import Dict, List, Sized, Tuple

from config.constants import RESAMPLE_RATE_DEFAULT
from tracer.dataset.data_key import DataKey
from tracer.dataset.trace_link import TraceLink
from tracer.models.model_properties import ArchitectureType


class TraceDataset:
    def __init__(self, links: Dict[int, TraceLink],
                 pos_link_ids: List[int] = None, neg_link_ids: List[int] = None):
        """
        Represents the common format for all datasets used by the huggingface trainer.
        :param links: The candidate links.
        :param pos_link_ids: The set of trace link ids representing positive links.
        :param neg_link_ids: The set of trace link ids representing negative links.
        """
        self.links = links
        self.pos_link_ids = pos_link_ids if pos_link_ids else list()
        self.neg_link_ids = neg_link_ids if neg_link_ids else list()

    def split(self, percent_split: float) -> Tuple["TraceDataset", "TraceDataset"]:
        """
        Splits trace dataset into two, with latter containing percentage of links specified.
        :param percent_split: The percent of links to include in second trace dataset.
        :return: Tuple of two trace datasets.
        """
        random_pos_link_ids = self._shuffle_link_ids(self.pos_link_ids)
        random_neg_link_ids = self._shuffle_link_ids(self.neg_link_ids)

        first_slice = self._create_new_dataset_from_slice(self.links, random_pos_link_ids, random_neg_link_ids,
                                                          percent_split, False)
        second_slice = self._create_new_dataset_from_slice(self.links, random_pos_link_ids, random_neg_link_ids,
                                                           percent_split, True)
        return first_slice, second_slice

    def to_trainer_dataset(self, arch_type: ArchitectureType) -> List[Dict]:
        """
        Converts trace links in dataset to feature entries used by Huggingface (HF) trainer.
        :param arch_type: The model architecture determining features.
        :return: A dataset used by the HF trainer.
        """
        return [self._get_feature_entry(self.links[link_id], arch_type) for link_id in self.links]

    def train_test_split(self, percent_test: float, resample_rate: int = RESAMPLE_RATE_DEFAULT):
        train, test = self.split(percent_test)
        train = self._prepare_train_split(train, resample_rate)
        test = self._prepare_test_split(test)
        return train, test

    def resize_links(self, new_length: int, include_duplicates: bool = False, use_neg_links: bool = True) -> None:
        """
        Extends or shrinks specified trace links to given size.
        :param new_length: The new size of the links.
        :param include_duplicates: Whether to include duplicate links if extending.
        :param use_neg_links: Whether to reference negative links, otherwise positive links assumed.
        :return:  None (links are automatically set in current instance).
        """
        link_ids = self.neg_link_ids if use_neg_links else self.pos_link_ids
        resized_link_ids = self._resize_data(link_ids, new_length, include_duplicates=include_duplicates)
        if use_neg_links:
            self.neg_link_ids = resized_link_ids
        else:
            self.pos_link_ids = resized_link_ids

    def resample_links(self, resample_rate: int, use_neg_links: bool = True) -> None:
        """
        Copies specified links as many times defined by resample rate.
        :param resample_rate: How many copies of each link to make.
        :param use_neg_links: Whether to reference negative links, otherwise positive links assumed.
        :return:  None (links are automatically set in current instance).
        """
        link_ids = self.neg_link_ids if use_neg_links else self.pos_link_ids
        resized_link_ids = self._resample_data(link_ids, resample_rate)
        if use_neg_links:
            self.neg_link_ids = resized_link_ids
        else:
            self.pos_link_ids = resized_link_ids

    @staticmethod
    def _resize_data(data: List, new_length: int, include_duplicates: bool = False) -> List:
        """
        Changes the size of the given dataset by using random choice or sample
        :param data: list of dataset
        :param new_length: desired length
        :param include_duplicates: if True, uses sampling
        :return: a list with the dataset of the new_length
        """
        include_duplicates = True if new_length > len(
            data) else include_duplicates  # must include duplicates to make a bigger dataset
        reduction_func = random.choices if include_duplicates else random.sample
        return reduction_func(data, k=new_length)

    @staticmethod
    def _resample_data(data: List[dict], resample_rate: int) -> List[dict]:
        """
        Adds multiple copies of each dataset entry at the given resample rate
        :param data: a list of dataset entries
        :param resample_rate: the number of copies to make of each entry
        :return: the resampled dataset
        """
        return [entry for i in range(resample_rate) for entry in data]

    @staticmethod
    def _create_new_dataset_from_slice(links: Dict[int, TraceLink], pos_link_ids: List[int],
                                       neg_link_ids: List[int],
                                       percent_split: float, second_slice: bool) -> "TraceDataset":
        """
        Creates a new trace dataset from the slice defined by the percent split.
        :param links: Map of trace link id to trace link.
        :param pos_link_ids: List of trace link ids representing positive links.
        :param neg_link_ids: List of trace link ids representing negative links.
        :param percent_split: The percentage of links included in second slice.
        :param second_slice: Whether to return second slice.
        :return:
        """
        slice_pos_link_ids = TraceDataset._get_data_split(pos_link_ids, percent_split, second_slice)
        slice_neg_link_ids = TraceDataset._get_data_split(neg_link_ids, percent_split, second_slice)
        slice_links = {
            link_id: links[link_id] for link_id in slice_pos_link_ids + slice_neg_link_ids
        }
        return TraceDataset(slice_links, slice_pos_link_ids, slice_neg_link_ids)

    def _get_feature_entry(self, link: TraceLink, arch_type: ArchitectureType) -> Dict[str, any]:
        """
        Gets a representational dictionary of the feature to be used in the dataset
        :param link: link to extract features from
        :param arch_type: The model architecture determining features.
        :return: feature name, value mappings
        """
        if arch_type == ArchitectureType.SIAMESE:
            entry = {**self._extract_feature_info(link.source.get_feature(), DataKey.SOURCE_PRE + "_"),
                     **self._extract_feature_info(link.target.get_feature(), DataKey.TARGET_PRE + "_")}
        else:
            entry = self._extract_feature_info(link.get_feature())
        entry[DataKey.LABEL_KEY] = int(link.is_true_link)
        return entry

    @staticmethod
    def _extract_feature_info(feature: Dict[str, any], prefix: str = '') -> Dict[str, any]:
        """
        Extracts the required info from a feature for dataset creation
        :param feature: dictionary of features
        :param prefix: prefix to add to key (i.e. s_)
        :return: feature name, value mappings
        """
        feature_info = {}
        for key_ in DataKey.get_feature_entry_keys():
            if key_ in feature:
                feature_info[prefix + key_] = feature[key_]
        return feature_info

    @staticmethod
    def _shuffle_link_ids(link_ids: List) -> List:
        """
        Shuffles the link ids
        :param link_ids: a set of link ids
        """
        return random.shuffle(link_ids)

    @staticmethod
    def _get_data_split(data: List, percent_split: float, for_second_split: bool = False) -> List:
        """
        Splits the dataset and returns the split
        :param data: a list of the dataset
        :param percent_split: The percentage of samples in second split.
        :param for_second_split: If True, returns the second portion.
        :return: the subsection of the dataset in the split
        """
        split_size = TraceDataset._get_first_split_size(data, percent_split)
        return data[split_size:] if for_second_split else data[:split_size]

    @staticmethod
    def _get_first_split_size(data: Sized, percent_split: float) -> int:
        """
        Gets the size of the dataset for the first split
        :param data: a list of the dataset
        :param percent_split: The percentage of samples in second split.
        :return: the size of the dataset split
        """
        return len(data) - round(len(data) * percent_split)

    def _prepare_train_split(self, train_split: "TraceDataset", resample_rate: int) -> "TraceDataset":
        """
        Resamples positive links and resizes negative links to create 50-50 ratio.
        :param train_split: The split to prepare.
        :param resample_rate: The number of copies of each positive link.
        :return: Prepared trace dataset
        """
        train_split.resample_links(resample_rate, use_neg_links=False)
        train_split.resize_links(len(self.pos_link_ids), include_duplicates=True, use_neg_links=True)
        return train_split

    def _prepare_test_split(self, test_split: "TraceDataset") -> "TraceDataset":
        """
        Does nothing. TODO: Add resizing behavior.
        :param test_split: The split to prepare.
        :return: Prepared trace dataset.
        """
        return test_split
