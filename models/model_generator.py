from abc import abstractmethod
from typing import Dict, Type

from transformers.modeling_utils import PreTrainedModel
from transformers import AutoConfig, AutoTokenizer
from enum import IntEnum


class ArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class BaseModelGenerator:
    _tokenizer = None
    _model = None

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

    def _load_model(self) -> PreTrainedModel:
        config = AutoConfig.from_pretrained(self.model_path)
        config.num_labels = 2
        return self.base_model_class.from_pretrained(self.model_path, config=config)

    def get_model(self) -> PreTrainedModel:
        if self._model is None:
            self._model = self._load_model()
        return self._model

    def get_tokenizer(self) -> AutoTokenizer:
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        return self._tokenizer

    def get_feature(self, **kwargs) -> Dict:
        return self.get_tokenizer()(**kwargs)
