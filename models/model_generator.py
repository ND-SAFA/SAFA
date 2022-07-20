from abc import abstractmethod
from typing import Dict, Type

from transformers.modeling_utils import PreTrainedModel
from transformers import AutoConfig, AutoTokenizer
from enum import IntEnum

from constants import MAX_SEQ_LENGTH_DEFAULT


class ArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class BaseModelGenerator:
    __tokenizer = None
    __model = None
    _max_seq_length = MAX_SEQ_LENGTH_DEFAULT

    @abstractmethod
    @property
    def base_model_class(self) -> Type[PreTrainedModel]:
        pass

    @abstractmethod
    @property
    def model_path(self) -> str:
        pass

    @abstractmethod
    @property
    def arch_type(self) -> ArchitectureType:
        pass

    def __load_model(self) -> PreTrainedModel:
        config = AutoConfig.from_pretrained(self.model_path)
        config.num_labels = 2
        return self.base_model_class.from_pretrained(self.model_path, config=config)

    def get_model(self) -> PreTrainedModel:
        if self.__model is None:
            self.__model = self.__load_model()
        return self.__model

    def get_tokenizer(self) -> AutoTokenizer:
        if self.__tokenizer is None:
            self.__tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        return self.__tokenizer

    def set_max_seq_length(self, max_seq_length):
        self._max_seq_length = max_seq_length

    def get_feature(self, return_token_type_ids=False, **kwargs) -> Dict:
        return self.get_tokenizer()(truncation="longest_first", return_attention_mask=True, max_length=self._max_seq_length,
                                    padding="max_length", return_token_type_ids=return_token_type_ids, **kwargs)
