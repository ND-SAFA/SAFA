import random
from typing import Dict, Iterable, List, Tuple, Set, Sized, Callable, Optional

import torch

from trace.config.constants import EVAL_DATASET_SIZE_DEFAULT, LINKED_TARGETS_ONLY_DEFAULT, RESAMPLE_RATE_DEFAULT, \
    VALIDATION_PERCENTAGE_DEFAULT
from trace.data.artifact import Artifact
from trace.data.data_key import DataKey
from trace.data.trace_dataset import TraceDataset
from trace.data.trace_link import TraceLink
from common.models.model_generator import ModelGenerator, ArchitectureType
import random
from typing import Callable, Dict, Iterable, List, Optional, Set, Sized, Tuple

import torch

from common.models.model_generator import ArchitectureType, ModelGenerator
from trace.config.constants import EVAL_DATASET_SIZE_DEFAULT, LINKED_TARGETS_ONLY_DEFAULT, RESAMPLE_RATE_DEFAULT, \
    VALIDATION_PERCENTAGE_DEFAULT
from trace.data.artifact import Artifact
from trace.data.data_key import DataKey
from trace.data.trace_dataset import TraceDataset
from trace.data.trace_link import TraceLink


class TraceDatasetCreator:
    """
    Responsible for creating dataset in format for defined models.
    """

    def __init__(self, source_layers: List[Dict[str, str]], target_layers: List[Dict[str, str]],
                 model_generator: ModelGenerator,
                 true_links: List[Tuple[str, str]] = None,
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT):
        """
        Constructs models for trace link training and validation
        :param source_layers: a list of source artifacts across all layers
        :param target_layers: a list of target artifacts across all layers
        :param true_links: list of tuples containing linked source and target ids
        :param model_generator: the ModelGenerator
        :param validation_percentage: percentage of dataset used for validation, if no value is supplied then data will not be split
        """
        self.__training_dataset: Optional[TraceDataset] = None
        self.__validation_dataset: Optional[TraceDataset] = None
        self.__prediction_dataset: Optional[TraceDataset] = None

        self.model_generator = model_generator
        self.links = self._generate_all_links(source_layers, target_layers)
        self.pos_link_ids, self.neg_link_ids = self._get_pos_and_neg_links(true_links, self.links) if true_links else (
        None, None)
        self.validation_percentage = validation_percentage
        self.linked_target_ids = self._get_linked_targets_only(true_links) if true_links else set()

    def get_training_dataset(self, resample_rate: int = RESAMPLE_RATE_DEFAULT) -> TraceDataset:
        """
        Gets the dataset used for training
        :param resample_rate: specifies the rate to resample the links to balance the dataset
        :return: the training dataset
        """
        if self.__training_dataset is None:
            train_pos_link_ids = self._get_data_split(self.pos_link_ids)
            train_neg_link_ids = self._get_data_split(self.neg_link_ids)

            train_pos_link_ids = TraceDataset.resample_data(train_pos_link_ids, resample_rate)
            train_neg_link_ids = TraceDataset.resize_data(train_neg_link_ids, len(train_pos_link_ids),
                                                          include_duplicates=True)

            link_ids = [*train_pos_link_ids, *train_neg_link_ids]
            self.__training_dataset = self._create_dataset(link_ids)

        return self.__training_dataset

    def get_validation_dataset(self, dataset_size: int = EVAL_DATASET_SIZE_DEFAULT,
                               linked_targets_only: bool = LINKED_TARGETS_ONLY_DEFAULT) -> TraceDataset:
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
                link_ids = TraceDataset.resize_data(link_ids, dataset_size)

            self.__validation_dataset = self._create_dataset(link_ids)

        return self.__validation_dataset

    def get_prediction_dataset(self) -> TraceDataset:
        """
        Gets the dataset used for validation
        :return: the prediction dataset
        """
        if self.__prediction_dataset is None:
            self.__prediction_dataset = self._create_dataset(list(self.links.keys()))
        return self.__prediction_dataset

    def _create_dataset(self, link_ids: List[int]) -> TraceDataset:
        """
        Creates a TraceDataset from the identified links
        :param link_ids: ids of links to be in dataset
        :return: the TraceDataset created from the links
        """
        dataset = TraceDataset()
        feature_entries = self._get_feature_entries(link_ids)
        source_target_pairs = [self.links[link_id].get_source_target_ids() for link_id in link_ids]
        dataset.add_entries(feature_entries, source_target_pairs)
        return dataset

    # TODO is this needed?
    def update_embeddings(self) -> None:
        """
        Update artifact embeddings
        :return: None
        """
        artifact_types = ["source", "target"]
        updated_ids = {"source": set(), "target": set()}
        with torch.no_grad():
            self.model_generator.get_model().eval()
            for link in self.links.values():
                for artifact_type in artifact_types:
                    artifact = getattr(link, artifact_type)
                    if artifact.id_ not in updated_ids[artifact_type]:
                        self._update_artifact_embedding(artifact)
                        updated_ids[artifact_type].add(link.source.id_)

    def _update_artifact_embedding(self, artifact: Artifact) -> None:
        """
        Helper method to update an artifact embedding
        :param artifact: artifact to update
        :return: None
        """
        feature = artifact.get_feature()
        model = self.model_generator.get_model()
        input_tensor = (
            torch.tensor(feature[DataKey.INPUT_IDS]).view(1, -1).to(model.device)
        )
        mask_tensor = (
            torch.tensor(feature[DataKey.ATTEN_MASK]).view(1, -1).to(model.device)
        )
        artifact_embedding = model.get_LM(input_tensor, mask_tensor)[0]
        artifact_embedding_cpu = artifact_embedding.to("cpu")
        artifact.embedding = artifact_embedding_cpu

    def _get_feature_entry(self, link: TraceLink) -> Dict[str, any]:
        """
        Gets a representational dictionary of the feature to be used in the dataset
        :param link: link to extract features from
        :return: feature name, value mappings
        """
        if self.model_generator.arch_type == ArchitectureType.SIAMESE:
            entry = {**self._extract_feature_info(link.source.get_feature(), DataKey.SOURCE_PRE + "_"),
                     **self._extract_feature_info(link.target.get_feature(), DataKey.TARGET_PRE + "_")}
        else:
            entry = self._extract_feature_info(link.get_feature())
        entry[DataKey.LABEL_KEY] = int(link.is_true_link)
        return entry

    def _get_feature_entries(self, link_ids: Iterable[int]) -> List[Dict]:
        """
        Gets a list of link features to be used in the dataset
        :param link_ids: ids of links to create dataset from
        :return: a list of the feature entries
        """
        return [self._get_feature_entry(self.links[link_id]) for link_id in link_ids]

    def _get_data_split(self, data: List, for_validation: bool = False) -> List:
        """
        Splits the data and returns the split
        :param data: a list of the data
        :param for_validation: if True, returns the validation portion
        :return: the subsection of the data in the split
        """
        split_size = self._get_train_split_size(data)
        return data[split_size:] if for_validation else data[:split_size]

    def _get_train_split_size(self, data: Sized) -> int:
        """
        Gets the size of the data for the train split
        :param data: a list of the data
        :return: the size of the data split
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
            if link.target.id_ in self.linked_target_ids:
                reduced_links.append(link.id_)
        return reduced_links

    def _generate_all_links(self, source_layers: List[Dict[str, str]], target_layers: List[Dict[str, str]]) -> Dict[
        int, TraceLink]:
        """
        Generates Trace Links between source and target pairs within each layer
        :param source_layers: a list of source artifacts across all layers
        :param target_layers: a list of target artifacts across all layers
        :return: a dictionary of the links, a list of the positive link ids, and a list of the negative link ids
        """
        links = {}
        for layer in range(len(source_layers)):
            layer_links = self._make_links(self.model_generator.get_feature, source_layers[layer], target_layers[layer])
            links.update(layer_links)
        return links

    @staticmethod
    def _make_links(feature_func: Callable, source_artifacts: Dict[str, str],
                    target_artifacts: Dict[str, str]) -> Dict[int, TraceLink]:
        """
        Creates Trace Links from all source and target pairs
        :param feature_func: function from which the artifact features can be generated
        :param source_artifacts: source artifacts represented as id, token mappings
        :param target_artifacts: target artifacts represented as id, token mappings
        :return: a dictionary of the id, link mappings
        """
        links = {}
        for s_id, s_token in source_artifacts.items():
            source = Artifact(s_id, s_token, feature_func)
            for t_id, t_token in target_artifacts.items():
                target = Artifact(t_id, t_token, feature_func)
                link = TraceLink(source, target, feature_func)
                links[link.id_] = link
        return links

    @staticmethod
    def _get_pos_and_neg_links(true_links: List[Tuple[str, str]], all_links: Dict[int, TraceLink]) -> Tuple[List, List]:
        """
        Creates a set of all positive and negative link ids
        :param true_links: list of tuples containing linked source and target ids
        :param true_links: dictionary of all possible TraceLinks
        :return: a list of the positive link ids, and a list of the negative link ids
        """
        pos_link_ids = set()
        for s_id, t_id in true_links:
            link_id = TraceLink.generate_link_id(s_id, t_id)
            true_link = all_links.get(link_id, None)
            if true_link:
                true_link.is_true_link = True
                pos_link_ids.add(link_id)
        neg_link_ids = list(set(all_links.keys()).difference(pos_link_ids))
        pos_link_ids = list(pos_link_ids)
        random.shuffle(pos_link_ids)
        random.shuffle(neg_link_ids)
        return pos_link_ids, neg_link_ids

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
    def _get_linked_targets_only(true_links: List) -> Set:
        """
        Gets a set containing only ids of targets that are part of at least one positive link
        :param true_links: list of tuples containing linked source and target ids
        :return: a set containing only ids of targets that are part of at least one positive link
        """
        return {t_id for _, t_id in true_links}
