import math
import random
from typing import Dict, List

from data.trace_link import TraceLink, Artifact
from data.data_key import DataKey
from constants import MAX_SEQ_LENGTH_DEFAULT, RESAMPLE_RATE_DEFAULT, EVAL_DATASET_SIZE_DEFAULT, LINKED_TARGETS_ONLY_DEFAULT
from models.model_generator import BaseModelGenerator, ArchitectureType


class TraceDataset:
    links = {}
    pos_link_ids = set()
    neg_link_ids = set()

    def __init__(self, s_arts: Dict, t_arts: Dict, true_links: List, model_generator: BaseModelGenerator,
                 linked_targets_only=LINKED_TARGETS_ONLY_DEFAULT):
        self.model_generator = model_generator
        t_arts = self._get_linked_targets_only(t_arts, true_links) if linked_targets_only else t_arts
        self._create_links(s_arts, t_arts, true_links, )

    def get_training_data(self, resample_rate: int = RESAMPLE_RATE_DEFAULT) -> List:
        dataset = self._get_feature_entries(self.pos_link_ids, resample_rate)
        reduced_neg_link_ids = self._reduce_data_size(list(self.neg_link_ids), len(self.pos_link_ids) * resample_rate)
        dataset.extend(self._get_feature_entries(reduced_neg_link_ids, 1))
        return dataset

    def get_validation_data(self, dataset_size: int = EVAL_DATASET_SIZE_DEFAULT) -> List:
        new_length = min(dataset_size, len(self.links))
        reduced_link_ids = self._reduce_data_size(list(self.links.keys()), new_length, include_duplicates=False)
        return self._get_feature_entries(reduced_link_ids)

    def _get_feature_entry(self, link: TraceLink) -> Dict:
        if self.model_generator.arch_type == ArchitectureType.SIAMESE:
            entry = {**self._extract_feature_info(link.source.get_feature(), DataKey.SOURCE_PRE + "_"),
                     **self._extract_feature_info(link.target.get_feature(), DataKey.TARGET_PRE + "_")}
        else:
            entry = self._extract_feature_info(link.get_feature())
        entry[DataKey.SOURCE_PRE + DataKey.ID_KEY] = link.source.id_
        entry[DataKey.TARGET_PRE + DataKey.ID_KEY] = link.target.id_
        entry[DataKey.LABEL_KEY] = int(link.is_linked)
        return entry

    def _get_feature_entries(self, link_ids, resample_rate: int = RESAMPLE_RATE_DEFAULT):
        feature_entries = []
        for link_id in link_ids:
            feature_entry = self._get_feature_entry(self.links[link_id])
            feature_entries.extend([feature_entry for i in range(resample_rate)])
        return feature_entries

    def _create_links(self, s_arts: Dict, t_arts: Dict, true_links: List):
        self.links = {}
        self.pos_link_ids = set()
        for s_id, s_token in s_arts.items():
            source = Artifact(s_id, s_token, self.model_generator.get_feature)
            for t_id, t_token in t_arts.items():
                target = Artifact(t_id, t_token, self.model_generator.get_feature)
                link = TraceLink(source, target, self.model_generator.get_feature)
                self.links[link.id_] = link
        for s_id, t_id in true_links:
            link_id = TraceLink.generate_link_id(s_id, t_id)
            true_link = self.links.get(link_id)
            true_link.is_linked = True
            self.pos_link_ids.add(link_id)
        self.neg_link_ids = set(self.links.keys()).difference(self.pos_link_ids)

    @staticmethod
    def _extract_feature_info(feature: Dict, prefix: str = '') -> Dict:
        feature_info = {}
        for key_ in DataKey.get_feature_info_keys():
            if key_ in feature:
                feature_info[prefix + key_] = feature[key_]
        return feature_info

    @staticmethod
    def _reduce_data_size(dataset: List, new_length: int, include_duplicates: bool = True):
        reduction_func = random.choices if include_duplicates else random.sample
        return reduction_func(dataset, k=new_length)

    @staticmethod
    def _get_linked_targets_only(t_arts: Dict, true_links: List) -> Dict:
        linked_target_ids = {t_id for _, t_id in true_links}
        return {t_id: token for t_id, token in t_arts.items() if t_id in linked_target_ids}


