from abc import abstractmethod
from enum import Enum, IntEnum
from typing import Dict, Type

from transformers import AutoConfig, AutoTokenizer
from transformers.modeling_utils import PreTrainedModel

from constants import MAX_SEQ_LENGTH_DEFAULT


class ArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class ModelSize(Enum):
    SMALL = "small"
    BASE = "base"
    LARGE = "large"


class AbstractModelGenerator:
    """
    Represents a learning model
    """
    __tokenizer: AutoTokenizer = None
    __model: PreTrainedModel = None
    _max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT

    @abstractmethod
    @property
    def base_model_class(self) -> Type[PreTrainedModel]:
        """
        Associated PreTrainedModel class
        :return: PreTrainedModel class
        """
        pass

    @abstractmethod
    def get_model_path(self) -> str:
        """
        Path to the model
        :return: model path
        """
        pass

    @abstractmethod
    @property
    def arch_type(self) -> ArchitectureType:
        """
        Architecture type (i.e. siamese or single)
        :return: ArchitectureType
        """
        pass

    @property
    def model_size(self) -> ModelSize:
        """
        Size of model (i.e. small, large, base...)
        :return: ModelSize
        """
        return ModelSize.BASE

    def get_model_name(self) -> str:
        """
        Name of the model
        :return: model name
        """
        return self.base_model_class.__name__

    def __load_model(self) -> PreTrainedModel:
        """
        Loads the model from the pretrained model path
        :return: the PreTrainedModel object
        """
        config = AutoConfig.from_pretrained(self.get_model_path())
        config.num_labels = 2
        return self.base_model_class.from_pretrained(self.get_model_path(), config=config)

    def get_model(self) -> PreTrainedModel:
        """
        Gets the PreTrainedModel
        :return: the PreTrainedModel object
        """
        if self.__model is None:
            self.__model = self.__load_model()
        return self.__model

    def get_tokenizer(self) -> AutoTokenizer:
        """
        Gets the pretrained Tokenizer
        :return: the Tokenizer
        """
        if self.__tokenizer is None:
            self.__tokenizer = AutoTokenizer.from_pretrained(self.get_model_path)
        return self.__tokenizer

    def set_max_seq_length(self, max_seq_length: int) -> None:
        """
        Sets the max_seq_length
        :param max_seq_length: desired max sequence length
        :return: None
        """
        self._max_seq_length = min(max_seq_length, self.get_tokenizer().model_max_length)

    def get_feature(self, return_token_type_ids: bool = False, **kwargs) -> Dict:
        """
        Method to get the feature for the model
        :param return_token_type_ids: if True, returns the token type ids
        :param kwargs: other arguments for tokenizer
        :return: feature name, value mappings
        """
        return self.get_tokenizer()(truncation="longest_first", return_attention_mask=True,
                                    max_length=self._max_seq_length,
                                    padding="max_length", return_token_type_ids=return_token_type_ids, **kwargs)
