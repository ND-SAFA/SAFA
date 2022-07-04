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
        t_arts = self.__get_linked_targets(t_arts, true_links) if linked_targets_only else t_arts
        self.__create_links(s_arts, t_arts, true_links)

    def get_training_data(self, resample_rate: int = RESAMPLE_RATE_DEFAULT, max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT) -> List:
        dataset = self.__get_feature_entries(self.pos_link_ids, resample_rate, max_seq_length)
        reduced_neg_link_ids = self.__reduce_data_size(list(self.neg_link_ids), len(self.pos_link_ids))
        dataset.extend(self.__get_feature_entries(reduced_neg_link_ids, 1, max_seq_length))
        return dataset

    def get_validation_data(self, dataset_size: int = EVAL_DATASET_SIZE_DEFAULT, max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT) -> List:
        new_length = min(dataset_size, len(self.links))
        reduced_link_ids = self.__reduce_data_size(list(self.links.keys()), new_length, duplicates=False)
        return self.__get_feature_entries(reduced_link_ids, max_seq_length=max_seq_length)

    def __reduce_data_size(self, dataset: List, new_length: int, duplicates: bool = True):
        reduction_func = random.choices if duplicates else random.sample
        return reduction_func(dataset, k=new_length)

    def __get_linked_targets(self, t_arts: Dict, true_links: List) -> Dict:
        linked_target_ids = {t_id for _, t_id in true_links}
        return {t_id: token for t_id, token in t_arts.items() if t_id in linked_target_ids}

    def __get_feature_entries(self, link_ids, resample_rate: int = RESAMPLE_RATE_DEFAULT,
                              max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT):
        dataset = []
        for link_id in link_ids:
            feature_entry = self.__get_feature_entry(self.links[link_id], max_seq_length)
            dataset.extend([feature_entry for i in range(resample_rate)])
        return dataset

    def __get_feature_for_single_artifact(self, artifact: Artifact, max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT) -> Dict:
        feature = self.model_generator.get_feature(
            text=artifact.token,
            return_attention_mask=True,
            return_token_type_ids=False,
            truncation="longest_first",
            max_length=max_seq_length,
            padding="max_length",
        )
        return feature

    def __get_feature_for_artifact_pair(self, link: TraceLink, max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT) -> Dict:
        feature = self.model_generator.get_feature(
            text=link.source.token,
            text_pair=link.target.token,
            return_attention_mask=True,
            return_token_type_ids=True,
            add_special_tokens=True,
            padding="max_length",
            max_length=max_seq_length,
            truncation="longest_first",
        )
        return feature

    def __extract_feature_info(self, feature: Dict, prefix: str = '') -> Dict:
        feature_info = {}
        for key_ in DataKey.get_feature_info_keys():
            if key_ in feature:
                feature_info[prefix + key_] = feature[key_]
        return feature_info

    def __get_feature_entry(self, link: TraceLink, max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT) -> Dict:
        if self.model_generator.arch_type == ArchitectureType.SIAMESE:
            source_feature = self.__get_feature_for_single_artifact(link.source, max_seq_length)
            target_feature = self.__get_feature_for_single_artifact(link.target, max_seq_length)
            entry = {**self.__extract_feature_info(source_feature, DataKey.SOURCE_PRE + "_"),
                     **self.__extract_feature_info(target_feature, DataKey.TARGET_PRE + "_")}
        else:
            feature = self.__get_feature_for_artifact_pair(link, max_seq_length)
            entry = self.__extract_feature_info(feature)
        entry[DataKey.SOURCE_PRE + DataKey.ID_KEY] = link.source.id_
        entry[DataKey.TARGET_PRE + DataKey.ID_KEY] = link.target.id_
        entry[DataKey.LABEL_KEY] = int(link.is_linked)
        return entry

    def __create_links(self, s_arts: Dict, t_arts: Dict, true_links: List):
        self.links = {}
        self.pos_link_ids = set()
        for s_id, s_token in s_arts.items():
            source = Artifact(s_id, s_token)
            for t_id, t_token in t_arts.items():
                target = Artifact(t_id, t_token)
                link = TraceLink(source, target)
                self.links[link.id_] = link
        for s_id, t_id in true_links:
            link_id = TraceLink.generate_link_id(s_id, t_id)
            true_link = self.links.get(link_id)
            true_link.is_linked = True
            self.pos_link_ids.add(link_id)
        self.neg_link_ids = set(self.links.keys()).difference(self.pos_link_ids)
