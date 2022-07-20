from typing import Dict, Union

from constants import MAX_SEQ_LENGTH_DEFAULT
from data.data_key import DataKey
from models.model_generator import BaseModelGenerator, ArchitectureType
from collections.abc import Callable


class Artifact:

    def __init__(self, id_: str, token: str, feature_func: Callable):
        self.id_ = id_
        self.token = token
        self.__feature_func = feature_func  # delay execution in case not needed
        self.__feature = None

    def get_feature(self):
        if self.__feature is None:
            self.__feature = self.__feature_func(text=self.token)
        return self.__feature


class TraceLink:

    def __init__(self, source: Artifact, target: Artifact, feature_func: Callable, is_linked: bool = False):
        self.source = source
        self.target = target
        self.id_ = self.generate_link_id(self.source.id_, self.target.id_)
        self.is_linked = is_linked
        self.__feature_func = feature_func  # delay execution in case not needed
        self.__feature = None

    def get_feature(self):
        if self.__feature is None:
            self.__feature = self.__feature_func(text=self.source.token, text_pair=self.target.token, return_token_type_ids=True,
                                                 add_special_tokens=True)
        return self.__feature

    @staticmethod
    def generate_link_id(source_id: str, target_id: str) -> int:
        return hash(source_id) + hash(target_id)

    def __hash__(self):
        return hash(self.id_)
