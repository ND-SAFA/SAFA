import os
import random
from collections import Counter
from copy import deepcopy
from typing import Any, Callable, Dict, List, Tuple

import networkx as nx
import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from tqdm import tqdm

from tgen.common.util.date_time_util import DateTimeUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.thread_util import ThreadUtil
from tgen.common.constants.dataset_constants import TRACE_THRESHOLD
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.keys.csv_keys import CSVKeys
from tgen.data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from tgen.data.processing.augmentation.data_augmenter import DataAugmenter
from tgen.data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep
from tgen.data.tdatasets.data_key import DataKey
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_matrix import TraceMatrix
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType


class TraceDataset(iDataset):
    """
    Represents the config format for all data used by the huggingface trainer.
    """

    def __init__(self, artifact_df: ArtifactDataFrame, trace_df: TraceDataFrame, layer_df: LayerDataFrame,
                 pos_link_ids: List[int] = None, neg_link_ids: List[int] = None, randomize: bool = False):
        """
        Initializes trace dataset to contain links in link ids lists. 
        :param layer_df: DataFrame containing the comparisons between artifact types present in project.
        :param artifact_df: DataFrame containing information about the artifact in the project.
        :param trace_df: DataFrame containing true links present in project.
        :param pos_link_ids: List of link ids for True links
        :param neg_link_ids: List of link ids for False links
        :param randomize: Whether to randomize the trace links.
        """
        self.__assert_dataframe_types(artifact_df, trace_df, layer_df)
        self.layer_df = layer_df
        self.artifact_df = artifact_df
        if not pos_link_ids or not neg_link_ids:
            pos_link_ids, neg_link_ids = self.__create_pos_neg_links(trace_df)
        self._pos_link_ids, self._neg_link_ids = pos_link_ids, neg_link_ids
        trace_df.drop_duplicates()
        trace_df = TraceDataFrame(trace_df.sample(frac=1))
        self.__trace_matrix = None
        self.randomize = randomize
        self.trace_df = trace_df

    def get_trace_matrix(self) -> TraceMatrix:
        if self.__trace_matrix is None:
            self.__trace_matrix = TraceMatrix(self.trace_df, randomize=self.randomize)
        return self.__trace_matrix

    def to_hf_dataset(self, model_generator: ModelManager) -> Dataset:
        """
        Converts trace links in data to Huggingface (HF) dataset.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A HF dataset.
        """

        def encode(batch) -> Dict:
            """
            Encodes the batch.
            """
            features = model_generator.get_feature(text=batch[CSVKeys.SOURCE],
                                                   text_pair=batch[CSVKeys.TARGET],
                                                   return_token_type_ids=True,
                                                   add_special_tokens=True)
            features[DataKey.LABELS_KEY] = torch.as_tensor(batch[CSVKeys.LABEL])
            return features

        logger.info("Transforming to HF dataset...")
        hf_dataset = Dataset.from_pandas(self.to_dataframe(include_ids=False))
        logger.info("Dataframe has been created....")
        hf_dataset.set_transform(encode)
        logger.info(f"Trace links after processing: {hf_dataset.num_rows}")
        return hf_dataset

    def to_trainer_dataset(self, model_generator: ModelManager, n_threads=20) -> List[Dict]:
        """
        Converts trace links in data to feature entries used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :param n_threads: The number of threads to use to calculate link features.
        :return: A data used by the trace trainer.
        """
        feature_entries = {}

        def create_link_feature(target_link_id: int) -> None:
            """
            Creates and store link feature in feature_entries.
            :param target_link_id: The trace link id to generate feature for.
            :return: None
            """
            feature_entries[target_link_id] = self._get_feature_entry(target_link_id,
                                                                      model_generator.arch_type,
                                                                      model_generator.get_feature)

        ThreadUtil.multi_thread_process("Generating trace features.", list(self.trace_df.index), create_link_feature, n_threads)

        project_link_ids = self.get_ordered_link_ids()
        logger.info(f"Trace links after processing: {len(project_link_ids)}")
        return [feature_entries[link_id] for link_id in project_link_ids]

    def to_dataframe(self, include_ids: bool = True) -> pd.DataFrame:
        """
        Converts trace links in data to dataframe format.
        :return: the dataset in a dataframe
        """
        link_ids_to_rows = {}
        for index in tqdm(self.trace_df.index, desc="Converting links to trace dataframe format."):
            link = self.trace_df.get_link(index)
            source = self.artifact_df.get_artifact(link[TraceKeys.SOURCE])
            target = self.artifact_df.get_artifact(link[TraceKeys.TARGET])
            label = link[TraceKeys.LABEL]
            new_row = [source[ArtifactKeys.CONTENT], target[ArtifactKeys.CONTENT], label] if not include_ids else \
                [source[ArtifactKeys.ID], source[ArtifactKeys.CONTENT], target[ArtifactKeys.ID], target[ArtifactKeys.CONTENT], label]
            link_ids_to_rows[index] = new_row

        data = [link_ids_to_rows[link_id] for link_id in self.get_ordered_link_ids()]
        cols = [CSVKeys.SOURCE, CSVKeys.TARGET, CSVKeys.LABEL] if not include_ids else [CSVKeys.SOURCE_ID, CSVKeys.SOURCE,
                                                                                        CSVKeys.TARGET_ID, CSVKeys.TARGET,
                                                                                        CSVKeys.LABEL]
        return pd.DataFrame(data, columns=cols)

    def get_link_source_target_artifact(self, link_id: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Gets the source and target artifact making up the given link
        :param link_id: The id of the link to get the source and target of
        :return: the source and target of link
        """
        link = self.trace_df.get_link(link_id)
        source = self.artifact_df.get_artifact(link[TraceKeys.SOURCE])
        target = self.artifact_df.get_artifact(link[TraceKeys.TARGET])
        return source, target

    def create_and_add_link(self, source_id: str, target_id: str, source_tokens: str, target_tokens: str,
                            is_true_link: bool) -> int:
        """
        Adds a link to the dataset
        :param source_id: the id of the source artifact
        :param target_id: the id of the target artifact
        :param source_tokens: the content of the source artifact
        :param target_tokens: the content of the target artifact
        :param is_true_link: True if the artifact are positively linked else False
        :return: the new link id
        """
        source = self.artifact_df.add_artifact(source_id, source_tokens)
        target = self.artifact_df.add_artifact(target_id, target_tokens)
        new_link = self.trace_df.add_link(source_id, target_id, int(is_true_link))
        if is_true_link:
            self._pos_link_ids.append(new_link[TraceKeys.LINK_ID])
        else:
            self._neg_link_ids.append(new_link[TraceKeys.LINK_ID])
        return new_link[TraceKeys.LINK_ID]

    def augment_pos_links(self, augmenter: DataAugmenter) -> None:
        """
        Augments the positive links to balance the data using the given augmentation steps
        :param augmenter: the augmentation to use for augmentation
        :return: None
        """

        augmentation_runs = [lambda data: augmenter.run(data, n_total_expected=2 * len(data),
                                                        exclude_all_but_step_type=SourceTargetSwapStep),
                             lambda data: augmenter.run(data, n_total_expected=len(self._neg_link_ids),
                                                        include_all_but_step_type=SourceTargetSwapStep)]
        for run in augmentation_runs:
            pos_links, data_entries = self._get_data_entries_for_augmentation()
            augmentation_results = run(data_entries)
            self._create_links_from_augmentation(augmentation_results, pos_links)

    def get_ordered_link_ids(self) -> List[int]:
        """
        Gets link ids in the order that they are given in the trainer dataset
        :return: a list of ordered link ids
        """
        pos_link_ids = self.get_pos_link_ids()
        neg_link_ids = self.get_neg_link_ids()
        link_counts = Counter(pos_link_ids + neg_link_ids)
        link_ids = []
        for id_ in self.trace_df.index:
            aug_trace_ids = [id_ for i in range(link_counts[id_])]
            link_ids.extend(aug_trace_ids)
        return link_ids

    def get_ordered_links(self) -> List[EnumDict]:
        """
        Gets links in the order that they are given in the trainer dataset
        :return: A list of ordered links
        """
        return [self.trace_df.get_link(link_id) for link_id in self.get_ordered_link_ids()]

    def get_ordered_labels(self) -> List[EnumDict]:
        """
        Gets labels in the order that they are given in the trainer dataset
        :return: A list of ordered labels
        """
        return [link[TraceKeys.LABEL] for link in self.get_ordered_links()]

    def get_source_target_pairs(self, link_ids: List = None) -> List[Tuple]:
        """
        Gets the list of source target pairs in the order corresponding to the trainer data
        :param link_ids: List of link ids to get source target pairs for. If not provided, defaults to ordered links
        :return: list of tuples containing source id and target id
        """
        link_ids = self.get_ordered_link_ids() if link_ids is None else link_ids
        source_target_pairs = []
        for link_id in link_ids:
            link = self.trace_df.get_link(link_id)
            source_target_pairs.append((link[TraceKeys.SOURCE], link[TraceKeys.TARGET]))
        return source_target_pairs

    def prepare_for_training(self, augmenter: DataAugmenter = None) -> None:
        """
        Resamples positive links and resizes negative links to create 50-50 ratio.
        :param augmenter: the augmenter to use for augmentation
        :return: Prepared trace data
        """
        if len(self._pos_link_ids) > 0:
            if augmenter:
                self.augment_pos_links(augmenter)

    def prepare_for_testing(self) -> None:
        """
        Does nothing. TODO: Add resizing behavior.
        :return: None
        """
        return

    def construct_graph_from_traces(self) -> nx.Graph:
        """
        Constructs a graph using the artifacts as nodes and positive trace links as edges
        :return: A graph representation of the dataset
        """
        G = nx.Graph()
        G.add_nodes_from(self.artifact_df.index)
        G.add_edges_from([(row[TraceKeys.SOURCE], row[TraceKeys.TARGET],
                           {'weight': row[TraceKeys.LABEL]}) for i, row in self.trace_df.itertuples()
                          if row[TraceKeys.LABEL] > TRACE_THRESHOLD])
        return G

    def get_pos_link_ids(self, unique: bool = False) -> List[int]:
        """
        Gets the link ids that represents a positive link
        :param unique: If True, includes duplicates of the links from augmentation, else just unique ids
        :return: Link ids that are positive links
        """
        if unique:
            return self.get_link_ids_by_label(label=1)
        return self._pos_link_ids

    def get_neg_link_ids(self, unique: bool = False) -> List[int]:
        """
        Gets the link ids that represents a negative link
        :param unique: If True, returns set of unique negative links.
        :return: Link ids that are positive links
        """
        if unique:
            return self.get_link_ids_by_label(label=0)
        return self._neg_link_ids

    def get_link_ids_by_label(self, label: int = 1) -> List[int]:
        """
        Gets all link ids that have the given label
        :param label: The label representing whether the link is positive or negative
        :return: The list of link ids that have the given label
        """
        return list(self.trace_df.filter_by_row(lambda row: row[TraceKeys.LABEL.value] == label).index)

    def _get_data_entries_for_augmentation(self) -> Tuple[List[pd.DataFrame], List[Tuple[str, str]]]:
        """
        Gets the data entries (link source, target, token pairs) for the augmentation
        :return: all links being used for augmentation and the data entries
        """
        source_target_pairs = []
        for link_id in self._pos_link_ids:
            source, target = self.get_link_source_target_artifact(link_id)
            source_target_pairs.append((source[ArtifactKeys.CONTENT], target[ArtifactKeys.CONTENT]))
        return self._pos_link_ids, source_target_pairs

    def _create_links_from_augmentation(self, augmentation_results: Dict[str, AbstractDataAugmentationStep.AUGMENTATION_RESULT],
                                        orig_link_ids: List[int]) -> None:
        """
        Creates new trace links from the results of an augmentation step
        :param augmentation_results: the augmentation step id mapped to its results
        :param orig_link_ids: a list of all the original link ids (pre-augmentation) that the step was run on
        :return: None
        """
        for step_id, result in augmentation_results.items():
            id_ = AbstractDataAugmentationStep.extract_unique_id_from_step_id(step_id)
            i = 0
            for entry, reference_index in result:
                i += 1
                aug_source_id, aug_target_id = self._get_augmented_artifact_ids(augmented_tokens=entry,
                                                                                orig_link_id=orig_link_ids[reference_index],
                                                                                aug_step_id=id_, entry_num=i)
                aug_source_tokens, aug_target_tokens = entry
                self.create_and_add_link(source_id=aug_source_id, target_id=aug_target_id,
                                         source_tokens=aug_source_tokens, target_tokens=aug_target_tokens, is_true_link=True)

    def _get_augmented_artifact_ids(self, augmented_tokens: Tuple[str, str], orig_link_id: int, aug_step_id: str,
                                    entry_num: int) -> Tuple[str, str]:
        """
        Gets the augmented artifact ids for the new augmented source and target artifact
        :param augmented_tokens: the augmented tokens for source and target
        :param orig_link_id: id of the original link (pre-augmentation)
        :param aug_step_id: the unique id of the augmentation step
        :param entry_num: the number for the augmented data entry
        :return: the augmented source and target ids
        """
        orig_link = self.trace_df.get_link(orig_link_id)
        aug_source_tokens, aug_target_tokens = augmented_tokens
        aug_source_id, aug_target_id = ("%s%s" % (link_id, aug_step_id) for link_id in
                                        [orig_link[TraceKeys.SOURCE], orig_link[TraceKeys.TARGET]])

        new_id = TraceDataFrame.generate_link_id(aug_source_id, aug_target_id)
        if self.trace_df.get_link(new_id) is not None:
            source, target = self.get_link_source_target_artifact(new_id)
            if source[ArtifactKeys.CONTENT] != aug_source_tokens or target[ArtifactKeys.CONTENT] != aug_target_tokens:
                aug_source_id += str(entry_num)
                aug_target_id += str(entry_num)
        return aug_source_id, aug_target_id

    def _get_feature_entry(self, link_id: int, arch_type: ModelArchitectureType, feature_func: Callable) \
            -> Dict[str, any]:
        """
        Gets a representational dictionary of the feature to be used in the data
        :param link_id: id of link to extract features from
        :param arch_type: The model architecture determining features.
        :return: feature name, value mappings
        """
        source, target = self.get_link_source_target_artifact(link_id)
        if arch_type == ModelArchitectureType.SIAMESE:
            entry = {
                **self._extract_feature_info(feature_func(text=source[ArtifactKeys.CONTENT]), DataKey.SOURCE_PRE + DataKey.SEP),
                **self._extract_feature_info(feature_func(text=target[ArtifactKeys.CONTENT]), DataKey.TARGET_PRE + DataKey.SEP)}
        else:
            entry = self._extract_feature_info(feature_func(text=source[ArtifactKeys.CONTENT],
                                                            text_pair=target[ArtifactKeys.CONTENT],
                                                            return_token_type_ids=True,
                                                            add_special_tokens=True))
        entry[DataKey.LABEL_KEY] = self.trace_df.get_link(link_id)[TraceKeys.LABEL]
        return entry

    def resize_pos_links(self, new_length: int, include_duplicates: bool = False) -> None:
        """
        Extends or shrinks pos trace links to given size.
        :param new_length: The new size of the links.
        :param include_duplicates: Whether to include duplicate links if extending.
        :return:  None (links are automatically set in current instance).
        """
        self._pos_link_ids = self._resize_data(self._pos_link_ids, new_length, include_duplicates=include_duplicates)

    def resize_neg_links(self, new_length: int, include_duplicates: bool = False) -> None:
        """
        Extends or shrinks neg trace links to given size.
        :param new_length: The new size of the links.
        :param include_duplicates: Whether to include duplicate links if extending.
        :return:  None (links are automatically set in current instance).
        """
        self._neg_link_ids = self._resize_data(self._neg_link_ids, new_length, include_duplicates=include_duplicates)

    def get_parent_child_types(self) -> List[Tuple[str, str]]:
        """
        Returns the artifacts types of the parent and child artifacts per tracing request.
        :return: Parent type and child type.
        """
        tracing_types = []
        for _, layer_row in self.layer_df.iterrows():
            parent_type = layer_row[LayerKeys.parent_label().value]
            child_type = layer_row[LayerKeys.child_label().value]
            tracing_types.append((parent_type, child_type))
        return tracing_types

    def as_creator(self, project_path: str, dataset_dirname: str):
        """
        Converts the dataset into a creator that can remake it
        :param project_path: The path to save the dataset at for reloading
        :param dataset_dirname: The directory that the dataset will be saved to
        :return: The dataset creator
        """
        from tgen.data.exporters.safa_exporter import SafaExporter
        from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
        from tgen.data.readers.structured_project_reader import StructuredProjectReader
        project_path = os.path.join(project_path, dataset_dirname)
        SafaExporter(project_path, dataset=self).export()
        return TraceDatasetCreator(project_reader=StructuredProjectReader(project_path=project_path))

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
        reduced_data = reduction_func(data, k=new_length)
        return reduced_data

    @staticmethod
    def _extract_feature_info(feature: Dict[str, any], prefix: str = EMPTY_STRING) -> Dict[str, any]:
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
    def __create_pos_neg_links(trace_df: TraceDataFrame):
        """
        Generates the list of positive and negative link ids.
        :param trace_df: Dataframe of links to their ids.
        :return: Tuple containing positive link ids and negative link ids.
        """
        pos_link_ids = []
        neg_link_ids = []
        for index, row in trace_df.itertuples():
            label = row[TraceKeys.LABEL]
            if not np.isnan(label) and round(label) == 1:
                pos_link_ids.append(index)
            else:
                neg_link_ids.append(index)
        return pos_link_ids, neg_link_ids

    @staticmethod
    def __assert_dataframe_types(artifact_df: Any, trace_df: Any, layer_mapping_df: Any) -> None:
        """
        Asserts that all dataframes are of the proper type
        :param artifact_df: The dataframe containing artifacts
        :param trace_df: The dataframe containing traces
        :param layer_mapping_df: The artifact containing layer mappings
        :return: None
        """
        types = [(artifact_df, ArtifactDataFrame), (trace_df, TraceDataFrame), (layer_mapping_df, LayerDataFrame)]
        for var_and_type in types:
            assert isinstance(*var_and_type), f"Dataframe must be of type {var_and_type[1]}"

    def __len__(self) -> int:
        """
        Returns the length of the dataset
        :return: the length of the dataset
        """
        return len(self._pos_link_ids + self._neg_link_ids)

    def __add__(self, other: "TraceDataset") -> "TraceDataset":
        """
        Combines two trace datasets
        :param other: Dataset to combine
        :return: The combined dataset
        """
        layer_mapping_df = LayerDataFrame.concat(self.layer_df, other.layer_df, ignore_index=True)
        artifact_df = ArtifactDataFrame.concat(self.artifact_df, other.artifact_df)
        trace_df = TraceDataFrame.concat(self.trace_df, other.trace_df)
        pos_link_ids = deepcopy(self._pos_link_ids) + deepcopy(other._pos_link_ids)
        neg_link_ids = deepcopy(self._neg_link_ids) + deepcopy(other._neg_link_ids)
        return TraceDataset(artifact_df=artifact_df, trace_df=trace_df, layer_df=layer_mapping_df,
                            pos_link_ids=pos_link_ids, neg_link_ids=neg_link_ids)

    def __getitem__(self, item: Any) -> Any:
        """
        Returns the link or artifact if is in dataset else None
        :param item: The id of the link or artifact
        :return: The link or artifact if is in dataset else None
        """
        result = self.trace_df.get_link(item)
        if result is None:
            result = self.artifact_df.get_artifact(item)
        return result

    def __contains__(self, item: Any) -> bool:
        """
        Returns True if link or artifact is in dataset else False
        :param item: The id of the link or artifact
        :return: True if link or artifact is in dataset else False
        """
        return self[item] is not None
