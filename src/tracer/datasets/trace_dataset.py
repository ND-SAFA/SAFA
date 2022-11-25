import os
import random
import uuid
from collections import OrderedDict
from copy import deepcopy
from typing import Callable, Dict, List, Sized, Tuple

from tracer.datasets.abstract_dataset import AbstractDataset
from tracer.datasets.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from tracer.datasets.processing.augmentation.data_augmenter import DataAugmenter
from tracer.datasets.data_key import DataKey
from tracer.datasets.data_objects.artifact import Artifact
from tracer.datasets.data_objects.trace_link import TraceLink
from tracer.datasets.formats.csv_format import CSVFormat
from tracer.models.model_generator import ModelGenerator
from tracer.models.model_properties import ArchitectureType
import pandas as pd

SEED = 420
random.seed(SEED)


class TraceDataset(AbstractDataset):

    def __init__(self, links: Dict[int, TraceLink], pos_link_ids: List[int] = None, neg_link_ids: List[int] = None):
        """
        Represents the config format for all datasets used by the huggingface trainer.
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
        Splits trace datasets into two, with latter containing percentage of links specified.
        :param percent_split: The percent of links to include in second trace datasets.
        :return: Tuple of two trace datasets.
        """
        first_slice = self._create_new_dataset_from_slice(percent_split, slice_num=1)
        second_slice = self._create_new_dataset_from_slice(percent_split, slice_num=2)
        return first_slice, second_slice

    def to_trainer_dataset(self, model_generator: ModelGenerator) -> List[Dict]:
        """
        Converts trace links in datasets to feature entries used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A datasets used by the HF trainer.
        """
        feature_entries = {
            link.id: self._get_feature_entry(link, model_generator.arch_type, model_generator.get_feature)
            for link in self.links.values()}
        return [feature_entries[link_id] for link_id in self.pos_link_ids + self.neg_link_ids]

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts trace links in datasets to dataframe format.
        :return: the dataset in a dataframe
        """
        link_ids_to_rows = {}
        for link in self.links.values():
            link_ids_to_rows[link.id] = [link.source.id, link.source.token, link.target.id, link.target.token, int(link.is_true_link)]
        data = [link_ids_to_rows[link_id] for link_id in self.pos_link_ids + self.neg_link_ids]
        return pd.DataFrame(data,
                            columns=[CSVFormat.SOURCE_ID, CSVFormat.SOURCE, CSVFormat.TARGET_ID, CSVFormat.TARGET, CSVFormat.LABEL])

    def augment_pos_links(self, augmentation_steps: List[AbstractDataAugmentationStep]) -> None:
        """
        Augments the positive links to balance the data using the given augmentation steps
        :param augmentation_steps: the augmentation steps to run
        :return: None
        """
        processor = DataAugmenter(augmentation_steps)
        pos_links = [self.links[link_id] for link_id in self.pos_link_ids]
        data_entries = [(link.source.token, link.target.token) for link in pos_links]
        augmentation_results = processor.run(data_entries, n_total_expected=len(self.neg_link_ids))
        for aug_id, results in augmentation_results.items():
            for entry, reference_index in results:
                orig_link = pos_links[reference_index]
                aug_source_id, aug_target_id = ("%s_%s" % (link_id, aug_id) for link_id in [orig_link.source.id, orig_link.target.id])
                aug_source_tokens, aug_target_tokens = entry
                self.add_link(source_id=aug_source_id, target_id=aug_target_id,
                              source_tokens=aug_source_tokens, target_tokens=aug_target_tokens, is_true_link=True)

    def prepare_for_training(self, augmentation_steps: List[AbstractDataAugmentationStep] = None) -> None:
        """
        Resamples positive links and resizes negative links to create 50-50 ratio.
        :param augmentation_steps: steps to run to augment the training data
        :return: Prepared trace datasets
        """
        if len(self.pos_link_ids) > 0:
            if augmentation_steps:
                self.augment_pos_links(augmentation_steps)
            self.resize_neg_links(len(self.pos_link_ids), include_duplicates=True)

    def prepare_for_testing(self) -> None:
        """
        Does nothing. TODO: Add resizing behavior.
        :return: None
        """
        return

    def save(self, output_dir: str, filename: str) -> str:
        """
        Saves the dataset to the output dir
        :param output_dir: directory to save to
        :param filename: name of tthe file (no ext)
        :return: location the file was saved to
        """
        output_path = os.path.join(output_dir, filename + ".csv")
        df = self.to_dataframe()
        df.to_csv(output_path)
        return output_path

    def get_source_target_pairs(self) -> List[Tuple]:
        """
        Gets the list of source target pairs in the order corresponding to the trainer datasets
        :return: list of tuples containing source id and target id
        """
        return [(self.links[link_id].source.id, self.links[link_id].target.id) for link_id in
                self.pos_link_ids + self.neg_link_ids]

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

    def add_link(self, source_id: str, target_id: str, source_tokens: str, target_tokens: str, is_true_link: bool) -> int:
        """
        Adds a link to the dataset
        :param source_id: the id of the source artifact
        :param target_id: the id of the target artifact
        :param source_tokens: the content of the source artifact
        :param target_tokens: the content of the target artifact
        :param is_true_link: True if the artifacts are positively linked else False
        :return: the new link id
        """
        source = Artifact(source_id, source_tokens)
        target = Artifact(target_id, target_tokens)
        new_link = TraceLink(source, target, is_true_link=is_true_link)
        self.links[new_link.id] = new_link
        if is_true_link:
            self.pos_link_ids.append(new_link.id)
        else:
            self.neg_link_ids.append(new_link.id)
        return new_link.id

    @staticmethod
    def _resize_data(data: List, new_length: int, include_duplicates: bool = False) -> List:
        """
        Changes the size of the given datasets by using random choice or sample
        :param data: list of datasets
        :param new_length: desired length
        :param include_duplicates: if True, uses sampling
        :return: a list with the datasets of the new_length
        """
        if new_length == len(data):
            return data
        include_duplicates = True if new_length > len(
            data) else include_duplicates  # must include duplicates to make a bigger datasets
        reduction_func = random.choices if include_duplicates else random.sample
        return reduction_func(data, k=new_length)

    @staticmethod
    def _resample_data(data: List[dict], resample_rate: int) -> List[dict]:
        """
        Adds multiple copies of each datasets entry at the given resample rate
        :param data: a list of datasets entries
        :param resample_rate: the number of copies to make of each entry
        :return: the resampled datasets
        """
        return [entry for i in range(resample_rate) for entry in data]

    def _create_new_dataset_from_slice(self, percent_split: float, slice_num: int) -> "TraceDataset":
        """
        Creates a new trace datasets from the slice defined by the percent split.
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

    def _get_feature_entry(self, link: TraceLink, arch_type: ArchitectureType, feature_func: Callable) \
            -> Dict[str, any]:
        """
        Gets a representational dictionary of the feature to be used in the datasets
        :param link: link to extract features from
        :param arch_type: The model architecture determining features.
        :return: feature name, value mappings
        """
        if arch_type == ArchitectureType.SIAMESE:
            entry = {
                **self._extract_feature_info(link.source.get_feature(feature_func), DataKey.SOURCE_PRE + DataKey.SEP),
                **self._extract_feature_info(link.target.get_feature(feature_func), DataKey.TARGET_PRE + DataKey.SEP)}
        else:
            entry = self._extract_feature_info(link.get_feature(feature_func))
        entry[DataKey.LABEL_KEY] = int(link.is_true_link)
        return entry

    @staticmethod
    def _extract_feature_info(feature: Dict[str, any], prefix: str = '') -> Dict[str, any]:
        """
        Extracts the required info from a feature for datasets creation
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
        Splits the datasets and returns the split
        :param data: a list of the datasets
        :param percent_split: The percentage of samples in second split.
        :param for_second_split: If True, returns the second portion.
        :return: the subsection of the datasets in the split
        """
        split_size = TraceDataset._get_first_split_size(data, percent_split)
        return data[split_size:] if for_second_split else data[:split_size]

    @staticmethod
    def _get_first_split_size(data: Sized, percent_split: float) -> int:
        """
        Gets the size of the datasets for the first split
        :param data: a list of the datasets
        :param percent_split: The percentage of samples in second split.
        :return: the size of the datasets split
        """
        return len(data) - round(len(data) * percent_split)

    def __len__(self):
        return len(self.pos_link_ids) + len(self.neg_link_ids)

    def __add__(self, other: "TraceDataset"):
        combined_links = deepcopy(self.links)
        combined_links.update(other.links)
        combined_pos_link_ids = set(self.pos_link_ids).union(set(other.pos_link_ids))
        combined_neg_link_ids = set(self.neg_link_ids).union(set(other.neg_link_ids))
        return TraceDataset(combined_links, list(combined_pos_link_ids), list(combined_neg_link_ids))
