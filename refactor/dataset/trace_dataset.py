import random
from typing import Dict, List, Set, Sized, Tuple

from dataset.data_key import DataKey
from dataset.trace_link import TraceLink
from models.model_properties import ArchitectureType


class TraceDataset:
    def __init__(self, links: Dict[int, TraceLink],
                 pos_link_ids: Set[int] = None, neg_link_ids: Set[int] = None):
        """
        Represents the common format for all datasets used by the huggingface trainer.
        :param links: The candidate links.
        :param pos_link_ids: The set of trace link ids representing positive links.
        :param neg_link_ids: The set of trace link ids representing negative links.
        """
        self.links = links
        self.pos_link_ids = pos_link_ids if pos_link_ids else set()
        self.neg_link_ids = neg_link_ids if neg_link_ids else set()

    def split(self, percent_split: float) -> Tuple["TraceDataset", "TraceDataset"]:
        """
        Splits trace dataset into two, with latter containing percentage of links specified.
        :param percent_split: The percent of links to include in second trace dataset.
        :return: Tuple of two trace datasets.
        """
        random_pos_link_ids = self._shuffle_link_ids(self.pos_link_ids)
        random_neg_link_ids = self._shuffle_link_ids(self.neg_link_ids)

        first_slice = self.__create_new_dataset_from_slice(self.links, random_pos_link_ids, random_neg_link_ids,
                                                           percent_split, False)
        second_slice = self.__create_new_dataset_from_slice(self.links, random_pos_link_ids, random_neg_link_ids,
                                                            percent_split, True)
        return first_slice, second_slice

    @staticmethod
    def __create_new_dataset_from_slice(links: Dict[int, TraceLink], pos_link_ids: List[int],
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
        return TraceDataset(slice_links, set(slice_pos_link_ids), set(slice_neg_link_ids))

    def to_trainer_dataset(self, arch_type: ArchitectureType) -> List[Dict]:
        """
        Converts trace links in dataset to feature entries used by Huggingface (HF) trainer.
        :param arch_type: The model architecture determining features.
        :return: A dataset used by the HF trainer.
        """
        return [self._get_feature_entry(self.links[link_id], arch_type) for link_id in self.links]

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
    def _shuffle_link_ids(link_ids: Set) -> List:
        """
        Shuffles the link ids
        :param link_ids: a set of link ids
        """
        link_ids_list = list(link_ids)
        random.shuffle(link_ids_list)
        return link_ids_list

    def _get_data_split(self, data: List, percent_split: float, for_second_split: bool = False) -> List:
        """
        Splits the dataset and returns the split
        :param data: a list of the dataset
        :param percent_split: The percentage of samples in second split.
        :param for_second_split: If True, returns the second portion.
        :return: the subsection of the dataset in the split
        """
        split_size = self._get_train_split_size(data, percent_split)
        return data[split_size:] if for_second_split else data[:split_size]

    def _get_train_split_size(self, data: Sized, percent_split: float) -> int:
        """
        Gets the size of the dataset for the train split
        :param data: a list of the dataset
        :param percent_split: The percentage of samples in second split.
        :return: the size of the dataset split
        """
        return len(data) - round(len(data) * percent_split)
