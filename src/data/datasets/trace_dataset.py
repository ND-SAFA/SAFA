import os
import random
from collections import OrderedDict
from copy import deepcopy
from typing import Callable, Dict, List, Tuple

import pandas as pd

from data.datasets.abstract_dataset import AbstractDataset
from data.datasets.data_key import DataKey
from data.datasets.keys.csv_format import CSVKeys
from data.datasets.trace_matrix import TraceMatrixManager
from data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from data.processing.augmentation.data_augmenter import DataAugmenter
from data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from models.model_properties import ModelArchitectureType


class TraceDataset(AbstractDataset):

    def __init__(self, links: Dict[int, TraceLink], randomize: bool = False):
        """
        Represents the config format for all data used by the huggingface trainer.
        :param links: The candidate links.
        """
        self.links = OrderedDict(links)
        self.pos_link_ids, self.neg_link_ids = self.__create_pos_neg_links(links)
        self.trace_matrix = TraceMatrixManager(self.links.values(), randomize=randomize)
        self._shuffle_link_ids(self.pos_link_ids)
        self._shuffle_link_ids(self.neg_link_ids)

    def to_trainer_dataset(self, model_generator: ModelManager) -> List[Dict]:
        """
        Converts trace links in data to feature entries used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data used by the HF trainer.
        """
        feature_entries = {
            link.id: self._get_feature_entry(link, model_generator.arch_type, model_generator.get_feature)
            for link in self.links.values()}
        project_links = self.get_ordered_links()
        return [feature_entries[link.id] for link in project_links]

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts trace links in data to dataframe format.
        :return: the dataset in a dataframe
        """
        link_ids_to_rows = {}
        for link in self.links.values():
            link_ids_to_rows[link.id] = [link.source.id, link.source.token, link.target.id, link.target.token,
                                         link.label]
        data = [link_ids_to_rows[link_id] for link_id in self.pos_link_ids + self.neg_link_ids]
        return pd.DataFrame(data,
                            columns=[CSVKeys.SOURCE_ID, CSVKeys.SOURCE, CSVKeys.TARGET_ID, CSVKeys.TARGET,
                                     CSVKeys.LABEL])

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
        self.trace_matrix.add_link(link=new_link)
        return new_link.id

    def augment_pos_links(self, augmenter: DataAugmenter) -> None:
        """
        Augments the positive links to balance the data using the given augmentation steps
        :param augmenter: the augmentation to use for augmentation
        :return: None
        """
        augmentation_runs = [lambda data: augmenter.run(data, n_total_expected=2 * len(data),
                                                        exclude_all_but_step_type=SourceTargetSwapStep),
                             lambda data: augmenter.run(data, n_total_expected=len(self.neg_link_ids),
                                                        include_all_but_step_type=SourceTargetSwapStep)]
        for run in augmentation_runs:
            pos_links, data_entries = self._get_data_entries_for_augmentation()
            augmentation_results = run(data_entries)
            self._create_links_from_augmentation(augmentation_results, pos_links)

    def get_ordered_links(self) -> List[TraceLink]:
        """
        Gets links in the order that they are given in the trainer dataset
        :return: a list of ordered links
        """
        return [self.links[link_id] for link_id in self.pos_link_ids + self.neg_link_ids]

    def get_source_target_pairs(self) -> List[Tuple]:
        """
        Gets the list of source target pairs in the order corresponding to the trainer data
        :return: list of tuples containing source id and target id
        """
        return [(link.source.id, link.target.id) for link in self.get_ordered_links()]

    def prepare_for_training(self, augmenter: DataAugmenter = None) -> None:
        """
        Resamples positive links and resizes negative links to create 50-50 ratio.
        :param augmenter: the augmenter to use for augmentation
        :return: Prepared trace data
        """
        if len(self.pos_link_ids) > 0:
            if augmenter:
                self.augment_pos_links(augmenter)
            self.resize_neg_links(len(self.pos_link_ids), include_duplicates=True)

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
        :param filename: name of the file (no ext)
        :return: location the file was saved to
        """
        output_path = os.path.join(output_dir, filename + ".csv")
        df = self.to_dataframe()
        df.to_csv(output_path)
        return output_path

    def _get_data_entries_for_augmentation(self) -> Tuple[List[TraceLink], List[Tuple[str, str]]]:
        """
        Gets the data entries (link source, target, token pairs) for the augmentation
        :return: all links being used for augmentation and the data entries
        """
        pos_links = [self.links[link_id] for link_id in self.pos_link_ids]
        return pos_links, [(link.source.token, link.target.token) for link in pos_links]

    def _create_links_from_augmentation(self, augmentation_results: Dict[str, AbstractDataAugmentationStep.AUGMENTATION_RESULT],
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
                                    entry_num: int) -> Tuple[str, str]:
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
            if self.links[new_id].source.token != aug_source_tokens or self.links[new_id].target.token != aug_target_tokens:
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
    def __create_pos_neg_links(links: Dict[int, TraceLink]):
        """
        Generates the list of positive and negative link ids.
        :param links: Dictionary of links to their ids.
        :return: Tuple containing positive link ids and negative link ids.
        """
        pos_link_ids = []
        neg_link_ids = []
        for link in links.values():
            if link.is_true_link:
                pos_link_ids.append(link.id)
            else:
                neg_link_ids.append(link.id)
        return pos_link_ids, neg_link_ids

    def __len__(self) -> int:
        """
        Returns the length of the dataset
        :return: the length of the dataset
        """
        return len(self.pos_link_ids) + len(self.neg_link_ids)

    def __add__(self, other: "TraceDataset") -> "TraceDataset":
        """
        Combines two datasets
        :param other: the other dataset
        :return: the combined dataset
        """
        combined_links = deepcopy(self.links)
        combined_links.update(other.links)
        return TraceDataset(combined_links)
