import math
import random
from typing import Dict, List, Tuple, Iterable

from data.trace_link import TraceLink, Artifact
from data.data_key import DataKey
from constants import RESAMPLE_RATE_DEFAULT, EVAL_DATASET_SIZE_DEFAULT, LINKED_TARGETS_ONLY_DEFAULT
from models.model_generator import BaseModelGenerator, ArchitectureType

import torch


class TraceDatasetCreator:
    links: Dict = {}
    pos_link_ids: set = set()
    neg_link_ids: set = set()
    __training_dataset: List[Dict] = None
    __prediction_dataset: List[Dict] = None

    def __init__(self, s_arts: Dict[str, str], t_arts: Dict[str, str], true_links: List[Tuple[str, str]],
                 model_generator: BaseModelGenerator, linked_targets_only: bool = LINKED_TARGETS_ONLY_DEFAULT):
        """
        Constructs datasets for trace link training and validation
        :param s_arts: source artifacts represented as id, token mappings
        :param t_arts: target artifacts represented as id, token mappings
        :param true_links: list of tuples containing linked source and target ids
        :param model_generator: the ModelGenerator
        :param linked_targets_only: if True, uses only targets that have at least one true link to a source
        """
        self.model_generator = model_generator
        t_arts = self._get_linked_targets_only(t_arts, true_links) if linked_targets_only else t_arts
        self._create_links(s_arts, t_arts, true_links)

    def get_training_dataset(self, resample_rate: int = RESAMPLE_RATE_DEFAULT) -> List[Dict]:
        """
        Gets the dataset used for training
        :param resample_rate: specifies the rate to resample the links to balance the dataset
        :return: the training dataset
        """
        if self.__training_dataset is None:
            self.__training_dataset = self._get_feature_entries(self.pos_link_ids, resample_rate)
            reduced_neg_link_ids = self._reduce_data_size(list(self.neg_link_ids), len(self.pos_link_ids) * resample_rate)
            self.__training_dataset.extend(self._get_feature_entries(reduced_neg_link_ids, 1))
        return self.__training_dataset

    def get_prediction_dataset(self, dataset_size: int = EVAL_DATASET_SIZE_DEFAULT) -> List[Dict]:
        """
        Gets the dataset used for prediction/validation
        :param dataset_size: desired size for dataset (if larger than original dataset, the entire dataset is used)
        :return: the prediction/validation dataset
        """
        if self.__prediction_dataset is None:
            new_length = min(dataset_size, len(self.links))
            reduced_link_ids = self._reduce_data_size(list(self.links.keys()), new_length, include_duplicates=False)
            self.__prediction_dataset = self._get_feature_entries(reduced_link_ids)
        return self.__prediction_dataset

    # TODO is this needed? incorporate into training/validation?
    # TODO clean this up
    def split_links(self, weights: Dict[str, int]) -> Dict[str, List[TraceLink]]:
        """
        Splits the links to divide dataset
        :param weights: split name, weight mappings specifying what proportion of links each split should take
        :return: split name, list of links mappings
        """
        total_w = sum(weights.values())
        links_by_splice = {slice_name: [] for slice_name in weights.keys()}
        link_ids_lists = [list(self.neg_link_ids), list(self.pos_link_ids)]
        n_link_ids = [len(self.neg_link_ids), len(self.pos_link_ids)]
        start = [0, 0]
        end = [0, 0]
        for slice_name, weight in weights.items():
            for i, link_ids_list in enumerate(link_ids_lists):
                end[i] = end[i] + min(math.ceil(weight * n_link_ids[i] / total_w), n_link_ids[i])
                subset = link_ids_list[start[i]:end[i]]
                links_by_splice[slice_name].extend([self.links[link_id] for link_id in subset])
                start[i] = end[i]
        return links_by_splice

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
                        self._updated_embd(artifact)
                        updated_ids[artifact_type].add(link.source.id_)

    def _updated_embd(self, artifact: Artifact) -> None:
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
        embd = model.get_LM(input_tensor, mask_tensor)[0]
        embd_cpu = embd.to("cpu")
        artifact.embd = embd_cpu

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
        entry[DataKey.SOURCE_PRE + DataKey.ID_KEY] = link.source.id_
        entry[DataKey.TARGET_PRE + DataKey.ID_KEY] = link.target.id_
        entry[DataKey.LABEL_KEY] = int(link.is_true_link)
        return entry

    def _get_feature_entries(self, link_ids: Iterable[str], resample_rate: int = RESAMPLE_RATE_DEFAULT) -> List[Dict]:
        """
        Gets a list of link features to be used in the dataset
        :param link_ids: ids of links to create dataset from
        :param resample_rate: specifies the rate to resample the links to balance the dataset
        :return: a list of the feature entries
        """
        feature_entries = []
        for link_id in link_ids:
            feature_entry = self._get_feature_entry(self.links[link_id])
            feature_entries.extend([feature_entry for i in range(resample_rate)])
        return feature_entries

    def _create_links(self, s_arts: Dict[str, str], t_arts: Dict, true_links: List[Tuple[str, str]]) -> None:
        """
        Creates Trace Links from all source and target pairs
        :param s_arts: source artifacts represented as id, token mappings
        :param t_arts: target artifacts represented as id, token mappings
        :param true_links: list of tuples containing linked source and target ids
        :return: None
        """
        self.links = {}
        for s_id, s_token in s_arts.items():
            source = Artifact(s_id, s_token, self.model_generator.get_feature)
            for t_id, t_token in t_arts.items():
                target = Artifact(t_id, t_token, self.model_generator.get_feature)
                link = TraceLink(source, target, self.model_generator.get_feature)
                self.links[link.id_] = link
        self._create_pos_and_neg_links(true_links)

    def _create_pos_and_neg_links(self, true_links: List[Tuple[str, str]]) -> None:
        """
          Creates a set of all positive and negative link ids
          :param true_links: list of tuples containing linked source and target ids
          :return: None
          """
        self.pos_link_ids = set()
        for s_id, t_id in true_links:
            link_id = TraceLink.generate_link_id(s_id, t_id)
            true_link = self.links.get(link_id)
            true_link.is_linked = True
            self.pos_link_ids.add(link_id)
        self.neg_link_ids = set(self.links.keys()).difference(self.pos_link_ids)

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
    def _reduce_data_size(data: List, new_length: int, include_duplicates: bool = True) -> List:
        """
        Reduces the size of the given dataset by using random choice or sample
        :param data: list of data
        :param new_length: desired length
        :param include_duplicates: if True, uses sampling
        :return: a list with the reduced data
        """
        reduction_func = random.choices if include_duplicates else random.sample
        return reduction_func(data, k=new_length)

    @staticmethod
    def _get_linked_targets_only(t_arts: Dict, true_links: List) -> Dict:
        """
        Gets a dictionary containing only targets that are part of at least one positive link
        :param t_arts: original target artifacts represented as id, token mappings
        :param true_links: list of tuples containing linked source and target ids
        :return: dictionary containing only targets that are part of at least one positive link
        """
        linked_target_ids = {t_id for _, t_id in true_links}
        return {t_id: token for t_id, token in t_arts.items() if t_id in linked_target_ids}
