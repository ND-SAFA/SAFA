from typing import Dict, List

from constants import MAX_SEQ_LENGTH
from data.trace_link import TraceLink, Artifact
from transformers import AutoTokenizer, default_data_collator, DataCollatorWithPadding

from models.model_generator import BaseModelGenerator, ArchitectureType


class TraceDataset:
    links = {}
    pos_link_ids = {}
    neg_link_ids = {}
    SOURCE_PRE = 's'
    TARGET_PRE = 't'
    ID_KEY = 'id'
    LABEL_KEY = 'label'
    FEATURE_INFO_KEYS = ["input_ids", "token_type_ids", "attention_mask"]

    def __init__(self, s_arts: Dict, t_arts: Dict, true_links: List, model_generator: BaseModelGenerator):
        self.model_generator = model_generator
        self.__create_links(s_arts, t_arts, true_links)

    def get_training_data(self, resample_rate: int = 1):
        data_collator = self.__get_data_collator()
        dataset = []
        for pos_link_id in self.pos_link_ids:
            link = self.links[pos_link_id]
            for i in range(resample_rate):
                dataset.append(self.get_feature_for_artifact_pair(link))

    def _get_feature_for_single_artifact(self, artifact: Artifact) -> Dict:
        feature = self.model_generator.get_feature(
            text=artifact.token,
            return_attention_mask=True,
            return_token_type_ids=False,
            truncation="longest_first",
            max_length=MAX_SEQ_LENGTH,
            padding="max_length",
        )
        return feature

    def get_feature_for_artifact_pair(self, link: TraceLink) -> Dict:
        feature = self.model_generator.get_feature(
            text=link.source.token,
            text_pair=link.target.token,
            return_attention_mask=True,
            return_token_type_ids=True,
            add_special_tokens=True,
            padding="max_length",
            max_length=MAX_SEQ_LENGTH,
            truncation="longest_first",
        )
        return feature

    def extract_feature_info(self, feature: Dict, prefix: str = '') -> Dict:
        feature_info = {}
        for key_ in self.FEATURE_INFO_KEYS:
            if key_ in feature:
                feature_info[prefix + key_] = feature[key_]
        return feature_info

    def get_feature_entry(self, link: TraceLink) -> Dict:
        if self.model_generator.arch_type == ArchitectureType.SIAMESE:
            source_feature = self._get_feature_for_single_artifact(link.source)
            target_feature = self._get_feature_for_single_artifact(link.target)
            entry = {**self.extract_feature_info(source_feature, self.SOURCE_PRE + "_"),
                     **self.extract_feature_info(target_feature, self.TARGET_PRE + "_")}
        else:
            feature = self.get_feature_for_artifact_pair(link)
            entry = self.extract_feature_info(feature)
        entry[self.SOURCE_PRE + self.ID_KEY] = link.source.id_
        entry[self.TARGET_PRE + self.ID_KEY] = link.target.id_
        entry[self.LABEL_KEY] = int(link.is_linked)
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

    def __get_data_collator(self, **kwargs):
        data_collator = (
            default_data_collator
            if kwargs['pad_to_max_length']
            else DataCollatorWithPadding(
                self.model_generator.get_tokenizer(), pad_to_multiple_of=8 if kwargs['fp16'] else None
            )
        )
        return data_collator
