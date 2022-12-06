import os
import random
from collections import OrderedDict
from copy import deepcopy
from typing import Callable, Dict, List, Sized, Tuple

import pandas as pd

from data.datasets.abstract_dataset import AbstractDataset
from data.datasets.data_key import DataKey
from data.formats.csv_format import CSVFormat
from data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from data.processing.augmentation.data_augmenter import DataAugmenter
from data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_generator import ModelGenerator
from models.model_properties import ModelArchitectureType


class TraceDataset(AbstractDataset):

    def __init__(self, links: Dict[int, TraceLink], pos_link_ids: List[int] = None, neg_link_ids: List[int] = None):
        """
        Represents the config format for all data used by the huggingface trainer.
        :param links: The candidate links.
        :param pos_link_ids: The set of trace link ids representing positive links.
        :param neg_link_ids: The set of trace link ids representing negative links.
        """
        self.links = OrderedDict(links)
        self.pos_link_ids = pos_link_ids if pos_link_ids else list()
        self.neg_link_ids = neg_link_ids if neg_link_ids else list()

        self._shuffle_link_ids(self.pos_link_ids)
        self._shuffle_link_ids(self.neg_link_ids)

    def to_trainer_dataset(self, model_generator: ModelGenerator) -> List[Dict]:
        """
        Converts trace links in data to feature entries used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data used by the HF trainer.
        """
        feature_entries = {
            link.id: self._get_feature_entry(link, model_generator.arch_type, model_generator.get_feature)
            for link in self.links.values()}
        project_links = (self.pos_link_ids + self.neg_link_ids)
        return [feature_entries[link_id] for link_id in project_links]

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts trace links in data to dataframe format.
        :return: the dataset in a dataframe
        """
        link_ids_to_rows = {}
        for link in self.links.values():
            link_ids_to_rows[link.id] = [link.source.id, link.source.token, link.target.id, link.target.token,
                                         int(link.is_true_link)]
        data = [link_ids_to_rows[link_id] for link_id in self.pos_link_ids + self.neg_link_ids]
        return pd.DataFrame(data,
                            columns=[CSVFormat.SOURCE_ID, CSVFormat.SOURCE, CSVFormat.TARGET_ID, CSVFormat.TARGET,
                                     CSVFormat.LABEL])

    def add_link(self, source_id: str, target_id: str, source_tokens: str, target_tokens: str,
                 is_true_link: bool) -> int:
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

    def augment_pos_links(self, augmentation_steps: List[AbstractDataAugmentationStep]) -> None:
        """
        Augments the positive links to balance the data using the given augmentation steps
        :param augmentation_steps: the augmentation steps to run
        :return: None
        """
        augmenter = DataAugmenter(augmentation_steps)
        augmentation_runs = [lambda data: augmenter.run(data, n_total_expected=2 * len(data),
                                                        exclude_all_but_step_type=SourceTargetSwapStep),
                             lambda data: augmenter.run(data, n_total_expected=len(self.neg_link_ids),
                                                        include_all_but_step_type=SourceTargetSwapStep)]
        for run in augmentation_runs:
            pos_links, data_entries = self._get_data_entries_for_augmentation()
            augmentation_results = run(data_entries)
            self._create_links_from_augmentation(augmentation_results, pos_links)

    def get_source_target_pairs(self) -> List[Tuple]:
        """
        Gets the list of source target pairs in the order corresponding to the trainer data
        :return: list of tuples containing source id and target id
        """
        return [(self.links[link_id].source.id, self.links[link_id].target.id) for link_id in
                self.pos_link_ids + self.neg_link_ids]

    def split(self, percent_split: float) -> Tuple["TraceDataset", "TraceDataset"]:
        """
        Splits trace data into two, with latter containing percentage of links specified.
        :param percent_split: The percent of links to include trace data.
        :return: Tuple of two trace data.
        """
        first_slice = self._create_new_dataset_from_slice(percent_split, slice_num=1)
        second_slice = self._create_new_dataset_from_slice(percent_split, slice_num=2)
        return first_slice, second_slice

    def split_multiple(self, percent_splits: List[float]) -> Tuple["TraceDataset"]:
        """
         Splits trace data into multiple data, with each part containing the corresponding percentage of links specified.
         :param percent_splits: The percent of links to include trace data for each split.
         :return: Tuple of trace data for each split specified
         """
        percent_splits = [1 - sum(percent_splits)] + percent_splits
        return self._split_multiple_helper(percent_splits, splits=[self])

    def prepare_for_training(self, augmentation_steps: List[AbstractDataAugmentationStep] = None) -> None:
        """
        Resamples positive links and resizes negative links to create 50-50 ratio.
        :param augmentation_steps: steps to run to augment the training data
        :return: Prepared trace data
        """
        if len(self.pos_link_ids) > 0:
            if augmentation_steps:
                self.augment_pos_links(augmentation_steps)
            self.resize_neg_links(len(self.pos_link_ids), include_duplicates=True)
            print("# Pos:", len(self.pos_link_ids))
            print("# Neg:", len(self.neg_link_ids))

    def prepare_for_testing(self) -> None:
        """
        Does nothing. TODO: Add resizing behavior.
        :return: None
        """
        return

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

    def _split_multiple_helper(self, percent_splits: List, splits: List) -> Tuple["TraceDataset"]:
        """
        Recursive method to split a dataset into multiple parts fir all percentages provided
        :param percent_splits: a list of all split percentages (should sum to 1)
        :param splits: list of already split data (the last element should be the portion remaining to split)
        :return: Tuple of trace data for each split specified
        """
        if len(percent_splits) <= 1:
            return tuple(splits)
        dataset_to_split = splits.pop()
        total_percent_to_split = 1 - percent_splits.pop(0)
        slices = dataset_to_split.split(total_percent_to_split)
        splits.extend(slices)
        updated_percent_splits = [percent_split / total_percent_to_split for percent_split in percent_splits]
        return self._split_multiple_helper(updated_percent_splits, splits)

    def _get_data_entries_for_augmentation(self) -> Tuple[List[TraceLink], List[Tuple[str, str]]]:
        """
        Gets the data entries (link source, target, token pairs) for the augmentation
        :return: all links being used for augmentation and the data entries
        """
        pos_links = [self.links[link_id] for link_id in self.pos_link_ids]
        return pos_links, [(link.source.token, link.target.token) for link in pos_links]

    def _create_links_from_augmentation(self, augmentation_results: Dict[
        str, AbstractDataAugmentationStep.AUGMENTATION_RESULT],
                                        orig_links: List[TraceLink]) -> None:
        """
        Creates new trace links from the results of an augmentation step
        :param augmentation_results: the augmentation step id mapped to its results
        :param orig_links: a list of all the original links (pre-augmentation) that the step was run on
        :return: None
        """
        for step_id, result in augmentation_results.items():
            id_ = AbstractDataAugmentationStep.extract_unique_id_from_step_id(step_id)
            i = 0
            for entry, reference_index in result:
                i += 1
                aug_source_id, aug_target_id = self._get_augmented_artifact_ids(augmented_tokens=entry,
                                                                                orig_link=orig_links[reference_index],
                                                                                aug_step_id=id_, entry_num=i)
                aug_source_tokens, aug_target_tokens = entry
                self.add_link(source_id=aug_source_id, target_id=aug_target_id,
                              source_tokens=aug_source_tokens, target_tokens=aug_target_tokens, is_true_link=True)

    def _get_augmented_artifact_ids(self, augmented_tokens: Tuple[str, str], orig_link: TraceLink, aug_step_id: str,
                                    entry_num: int) \
            -> Tuple[str, str]:
        """
        Gets the augmented artifact ids for the new augmented source and target artifact
        :param augmented_tokens: the augmented tokens for source and target
        :param orig_link: the original link (pre-augmentation)
        :param aug_step_id: the unique id of the augmentation step
        :param entry_num: the number for the augmented data entry
        :return: the augmented source and target ids
        """
        aug_source_tokens, aug_target_tokens = augmented_tokens
        aug_source_id, aug_target_id = ("%s%s" % (link_id, aug_step_id) for link_id in
                                        [orig_link.source.id, orig_link.target.id])

        new_id = TraceLink.generate_link_id(aug_source_id, aug_target_id)
        if new_id in self.links:
            if self.links[new_id].source.token != aug_source_tokens or self.links[
                new_id].target.token != aug_target_tokens:
                aug_source_id += str(entry_num)
                aug_target_id += str(entry_num)
        return aug_source_id, aug_target_id

    @staticmethod
    def _resize_data(data: List, new_length: int, include_duplicates: bool = False) -> List:
        """
        Changes the size of the given data by using random choice or sample
        :param data: list of data
        :param new_length: desired length
        :param include_duplicates: if True, uses sampling
        :return: a list with the data of the new_length
        """
        if new_length == len(data):
            return data
        include_duplicates = True if new_length > len(
            data) else include_duplicates  # must include duplicates to make a bigger data
        reduction_func = random.choices if include_duplicates else random.sample
        return reduction_func(data, k=new_length)

    def _create_new_dataset_from_slice(self, percent_split: float, slice_num: int) -> "TraceDataset":
        """
        Creates a new trace data from the slice defined by the percent split.
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

    def _get_feature_entry(self, link: TraceLink, arch_type: ModelArchitectureType, feature_func: Callable) \
            -> Dict[str, any]:
        """
        Gets a representational dictionary of the feature to be used in the data
        :param link: link to extract features from
        :param arch_type: The model architecture determining features.
        :return: feature name, value mappings
        """
        if arch_type == ModelArchitectureType.SIAMESE:
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
        Extracts the required info from a feature for data creation
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
        Splits the data and returns the split
        :param data: a list of the data
        :param percent_split: The percentage of samples in second split.
        :param for_second_split: If True, returns the second portion.
        :return: the subsection of the data in the split
        """
        split_size = TraceDataset._get_first_split_size(data, percent_split)
        return data[split_size:] if for_second_split else data[:split_size]

    @staticmethod
    def _get_first_split_size(data: Sized, percent_split: float) -> int:
        """
        Gets the size of the data for the first split
        :param data: a list of the data
        :param percent_split: The percentage of samples in second split.
        :return: the size of the data split
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
