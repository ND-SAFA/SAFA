import random
from collections import OrderedDict
from copy import deepcopy
from typing import Callable, Dict, List, Sized, Tuple

from config.constants import RESAMPLE_RATE_DEFAULT
from tracer.dataset.abstract_dataset import AbstractDataset
from tracer.dataset.data_key import DataKey
from tracer.dataset.data_objects.trace_link import TraceLink
from tracer.models.model_generator import ModelGenerator
from tracer.models.model_properties import ArchitectureType

SEED = 420
random.seed(SEED)


class TraceDataset(AbstractDataset):

    def __init__(self, links: Dict[int, TraceLink], pos_link_ids: List[int] = None, neg_link_ids: List[int] = None):
        """
        Represents the common format for all datasets used by the huggingface trainer.
        :param links: The candidate links.
        :param pos_link_ids: The set of trace link ids representing positive links.
        :param neg_link_ids: The set of trace link ids representing negative links.
        """
        self.links = OrderedDict(links)
        self.pos_link_ids = pos_link_ids if pos_link_ids else list()
        self.neg_link_ids = neg_link_ids if neg_link_ids else list()

        self._shuffle_link_ids(self.pos_link_ids)
        self._shuffle_link_ids(self.neg_link_ids)

    def split(self, percent_split: float) -> Tuple["TraceDataset", "TraceDataset"]:
        """
        Splits trace dataset into two, with latter containing percentage of links specified.
        :param percent_split: The percent of links to include in second trace dataset.
        :return: Tuple of two trace datasets.
        """
        first_slice = self._create_new_dataset_from_slice(percent_split, slice_num=1)
        second_slice = self._create_new_dataset_from_slice(percent_split, slice_num=2)
        return first_slice, second_slice

    def to_trainer_dataset(self, model_generator: ModelGenerator) -> List[Dict]:
        """
        Converts trace links in dataset to feature entries used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A dataset used by the HF trainer.
        """
        return [self._get_feature_entry(self.links[link_id], model_generator.arch_type, model_generator.get_feature) for
                link_id in self.links]

    def get_source_target_pairs(self) -> List[Tuple]:
        """
        Gets the list of source target pairs in the order corresponding to the trainer dataset
        :return: list of tuples containing source id and target id
        """
        return [(link.source.id, link.target.id) for link in self.links.values()]

    def get_train_test_split(self, percent_test: float, resample_rate: int = RESAMPLE_RATE_DEFAULT):
        """

        :param percent_test:
        :param resample_rate:
        :return:
        """
        train, test = self.split(percent_test)
        train = self._prepare_train_split(train, resample_rate)
        test = self._prepare_test_split(test)
        return train, test

    def resize_pos_links(self, new_length: int, include_duplicates: bool = False) -> None:
        """
        Extends or shrinks pos trace links to given size.
        :param new_length: The new size of the links.
        :param include_duplicates: Whether to include duplicate links if extending.
        :return:  None (links are automatically set in current instance).
        """
        self.pos_link_ids = self._resize_data(self.pos_link_ids, new_length, include_duplicates=include_duplicates)

    def resize_neg_links(self, new_length: int, include_duplicates: bool = False) -> None:
        """
        Extends or shrinks neg trace links to given size.
        :param new_length: The new size of the links.
        :param include_duplicates: Whether to include duplicate links if extending.
        :return:  None (links are automatically set in current instance).
        """
        self.neg_link_ids = self._resize_data(self.neg_link_ids, new_length, include_duplicates=include_duplicates)

    def resample_pos_links(self, resample_rate: int) -> None:
        """
        Copies pos links as many times defined by resample rate.
        :param resample_rate: How many copies of each link to make.
        :return:  None (links are automatically set in current instance).
        """
        self.pos_link_ids = self._resample_data(self.pos_link_ids, resample_rate)

    def resample_neg_links(self, resample_rate: int) -> None:
        """
        Copies neg links as many times defined by resample rate.
        :param resample_rate: How many copies of each link to make.
        :return:  None (links are automatically set in current instance).
        """
        self.neg_link_ids = self._resample_data(self.neg_link_ids, resample_rate)

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

    def _create_new_dataset_from_slice(self, percent_split: float, slice_num: int) -> "TraceDataset":
        """
        Creates a new trace dataset from the slice defined by the percent split.
        :param percent_split: The percentage of links included in second slice.
        :param slice_num: Whether to return first or second slice.
        :return:
        """
        slice_pos_link_ids = TraceDataset._get_data_split(self.pos_link_ids, percent_split, slice_num == 2)
        slice_neg_link_ids = TraceDataset._get_data_split(self.neg_link_ids, percent_split, slice_num == 2)
        slice_links = {
            link_id: self.links[link_id] for link_id in slice_pos_link_ids + slice_neg_link_ids
        }
        return TraceDataset(slice_links, slice_pos_link_ids, slice_neg_link_ids)

    def _get_feature_entry(self, link: TraceLink, arch_type: ArchitectureType, feature_func: Callable) -> Dict[
        str, any]:
        """
        Gets a representational dictionary of the feature to be used in the dataset
        :param link: link to extract features from
        :param arch_type: The model architecture determining features.
        :return: feature name, value mappings
        """
        if arch_type == ArchitectureType.SIAMESE:
            entry = {**self._extract_feature_info(link.source.get_feature(feature_func), DataKey.SOURCE_PRE + DataKey.SEP),
                     **self._extract_feature_info(link.target.get_feature(feature_func), DataKey.TARGET_PRE + DataKey.SEP)}
        else:
            entry = self._extract_feature_info(link.get_feature(feature_func))
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
    def _shuffle_link_ids(link_ids: List) -> None:
        """
        Shuffles the link ids
        :param link_ids: a set of link ids
        """
        random.shuffle(link_ids)

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
        if len(self.pos_link_ids) > 0:
            train_split.resample_pos_links(resample_rate)
            train_split.resize_neg_links(len(self.pos_link_ids), include_duplicates=True)
        return train_split

    def _prepare_test_split(self, test_split: "TraceDataset") -> "TraceDataset":
        """
        Does nothing. TODO: Add resizing behavior.
        :param test_split: The split to prepare.
        :return: Prepared trace dataset.
        """
        return test_split

    def __len__(self):
        return len(self.links)

    def __add__(self, other: "TraceDataset"):
        combined_links = deepcopy(self.links)
        combined_links.update(other.links)
        combined_pos_link_ids = set(self.pos_link_ids).union(set(other.pos_link_ids))
        combined_neg_link_ids = set(self.neg_link_ids).union(set(other.neg_link_ids))
        return TraceDataset(combined_links, list(combined_pos_link_ids), list(combined_neg_link_ids))
