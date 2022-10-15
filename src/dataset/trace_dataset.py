import random
from typing import Dict, Iterable, List, Optional, Set, Sized

from config.constants import EVAL_DATASET_SIZE_DEFAULT, LINKED_TARGETS_ONLY_DEFAULT, RESAMPLE_RATE_DEFAULT, \
    VALIDATION_PERCENTAGE_DEFAULT
from dataset.data_key import DataKey
from dataset.data_slice import DataSlice
from dataset.trace_link import TraceLink
from models.model_properties import ArchitectureType


class TraceDataset:

    def __init__(self, links: Dict[int, TraceLink], arch_type: ArchitectureType,
                 pos_link_ids: Set[int] = None, neg_link_ids: Set[int] = None,
                 linked_target_ids=Set[int],
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT):
        self.__training_dataset: Optional[DataSlice] = None
        self.__validation_dataset: Optional[DataSlice] = None
        self.__prediction_dataset: Optional[DataSlice] = None

        self.links = links
        self.arch_type = arch_type
        self.pos_link_ids = self._shuffle_link_ids(pos_link_ids)
        self.neg_link_ids = self._shuffle_link_ids(neg_link_ids)
        self.linked_target_ids = linked_target_ids
        self.validation_percentage = validation_percentage

    @staticmethod
    def _shuffle_link_ids(link_ids: Set) -> List:
        """
        Shuffles the link ids
        :param link_ids: a set of link ids
        """
        link_ids_list = list(link_ids)
        random.shuffle(link_ids_list)
        return link_ids_list

    def _get_data_split(self, data: List, for_validation: bool = False) -> List:
        """
        Splits the dataset and returns the split
        :param data: a list of the dataset
        :param for_validation: if True, returns the validation portion
        :return: the subsection of the dataset in the split
        """
        split_size = self._get_train_split_size(data)
        return data[split_size:] if for_validation else data[:split_size]

    def _get_train_split_size(self, data: Sized) -> int:
        """
        Gets the size of the dataset for the train split
        :param data: a list of the dataset
        :return: the size of the dataset split
        """
        return len(data) - round(len(data) * self.validation_percentage)

    def _reduce_to_linked_targets_only(self, orig_link_ids: Iterable) -> List[int]:
        """
        Reduces a list of link ids to only those that use a target with at least one true link
        :param orig_link_ids: a list of link ids
        :return: a list of link ids to only those that use a target with at least one true link
        """
        reduced_links = []
        for link_id in orig_link_ids:
            link = self.links[link_id]
            if link.target.id in self.linked_target_ids:
                reduced_links.append(link.id)
        return reduced_links

    def get_training_dataset(self, resample_rate: int = RESAMPLE_RATE_DEFAULT) -> DataSlice:
        """
        Gets the dataset used for training
        :param resample_rate: specifies the rate to resample the links to balance the dataset
        :return: the training dataset
        """
        if self.__training_dataset is None:
            train_pos_link_ids = self._get_data_split(self.pos_link_ids)
            train_neg_link_ids = self._get_data_split(self.neg_link_ids)

            train_pos_link_ids = self.resample_data(train_pos_link_ids, resample_rate)
            train_neg_link_ids = self.resize_data(train_neg_link_ids, len(train_pos_link_ids),
                                                  include_duplicates=True)

            link_ids = [*train_pos_link_ids, *train_neg_link_ids]
            self.__training_dataset = self._create_data_slice(link_ids)

        return self.__training_dataset

    def get_validation_dataset(self, dataset_size: int = EVAL_DATASET_SIZE_DEFAULT,
                               linked_targets_only: bool = LINKED_TARGETS_ONLY_DEFAULT) -> DataSlice:
        """
        Gets the dataset used for validation
        :param dataset_size: desired size for dataset (if larger than original dataset, the entire dataset is used)
        :param linked_targets_only: reduce dataset size to include only targets that have at least one true link
        :return: the validation dataset
        """
        if self.__validation_dataset is None:
            val_pos_link_ids = self._get_data_split(self.pos_link_ids, for_validation=True)
            val_neg_link_ids = self._get_data_split(self.neg_link_ids, for_validation=True)

            if linked_targets_only:
                val_neg_link_ids = self._reduce_to_linked_targets_only(val_neg_link_ids)

            link_ids = [*val_pos_link_ids, *val_neg_link_ids]

            if dataset_size < len(link_ids):
                link_ids = self.resize_data(link_ids, dataset_size)

            self.__validation_dataset = self._create_data_slice(link_ids)

        return self.__validation_dataset

    def get_prediction_dataset(self) -> DataSlice:
        """
        Gets the dataset used for validation
        :return: the prediction dataset
        """
        if self.__prediction_dataset is None:
            self.__prediction_dataset = self._create_data_slice(list(self.links.keys()))
        return self.__prediction_dataset

    def _create_data_slice(self, link_ids: List[int]) -> DataSlice:
        """
        Creates a TraceDataset from the identified links
        :param link_ids: ids of links to be in dataset
        :return: the TraceDataset created from the links
        """
        dataset = DataSlice()
        feature_entries = self._get_feature_entries(link_ids)
        source_target_pairs = [self.links[link_id].get_source_target_ids() for link_id in link_ids]
        dataset.add_entries(feature_entries, source_target_pairs)
        return dataset

    def _get_feature_entries(self, link_ids: Iterable[int]) -> List[Dict]:
        """
        Gets a list of link features to be used in the dataset
        :param link_ids: ids of links to create dataset from
        :return: a list of the feature entries
        """
        return [self._get_feature_entry(self.links[link_id]) for link_id in link_ids]

    def _get_feature_entry(self, link: TraceLink) -> Dict[str, any]:
        """
        Gets a representational dictionary of the feature to be used in the dataset
        :param link: link to extract features from
        :return: feature name, value mappings
        """
        if self.arch_type == ArchitectureType.SIAMESE:
            entry = {**self._extract_feature_info(link.source.get_feature(), DataKey.SOURCE_PRE + "_"),
                     **self._extract_feature_info(link.target.get_feature(), DataKey.TARGET_PRE + "_")}
        else:
            entry = self._extract_feature_info(link.get_feature())
        entry[DataKey.LABEL_KEY] = int(link.is_true_link)
        return entry

    @staticmethod
    def resize_data(data: List, new_length: int, include_duplicates: bool = False) -> List:
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
    def resample_data(data: List[dict], resample_rate: int) -> List[dict]:
        """
        Adds multiple copies of each dataset entry at the given resample rate
        :param data: a list of dataset entries
        :param resample_rate: the number of copies to make of each entry
        :return: the resampled dataset
        """
        return [entry for i in range(resample_rate) for entry in data]

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
