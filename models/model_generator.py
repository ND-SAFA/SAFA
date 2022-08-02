from bert_trace_single import BertTraceSingle
from models.bert_trace_siamese import BertTraceSiamese
from models.electra_trace_single import ElectraTraceSingle

from typing import Dict
import os
from transformers.modeling_utils import PreTrainedModel
from transformers import AutoConfig, AutoTokenizer
from enum import IntEnum, Enum

from constants import MAX_SEQ_LENGTH_DEFAULT
from pretrain.corpuses.domain import Domain


class SupportedBaseModel(Enum):
    BERT_TRACE_SINGLE = BertTraceSingle
    BERT_TRACE_SIAMESE = BertTraceSiamese
    ELECTRA_TRACE_SINGLE = ElectraTraceSingle


class ArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class ModelSize(Enum):
    SMALL = "small"
    BASE = "base"
    LARGE = "large"


class ModelGenerator:
    __tokenizer: AutoTokenizer = None
    __model: PreTrainedModel = None
    _max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT

    def __init__(self, model_path: str):
        """
        Handles loading model and related functions
        :param model_path: the path to the saved model
        """
        self.model_path = model_path
        self.model_name = self._get_model_name_from_path(self.model_path)
        self.base_model_class = self._get_base_model_class(self.model_name)
        self.arch_type = self._get_model_architecture_type(self.model_name)

    @staticmethod
    def _get_model_name_from_path(model_path: str) -> str:
        """
        Extracts the model name from the model path
        :param model_path: location of model
        :return: the model_name
        """
        return model_path.split(os.sep)[-1]

    @staticmethod
    def _get_base_model_class(model_name: str) -> PreTrainedModel:
        """
        Gets the base model class
        :param model_name: the name of the model
        :return: PreTrainedModel class
        """
        try:
            return SupportedBaseModel[model_name].value
        except KeyError:
            raise KeyError("Model %s is not supported" % model_name)

    @staticmethod
    def _get_model_architecture_type(model_name: str) -> ArchitectureType:
        """
        Gets the architecture type of model
        :param model_name: the name of the model
        :return: the ArchitectureType of model
        """
        arch_type = model_name.split("_")[-1]
        try:
            return ArchitectureType[arch_type]
        except KeyError:
            return ArchitectureType.SINGLE

    @staticmethod
    def create_path(domain: Domain, project_id: str, base_model: SupportedBaseModel):
        """
        Creates the path to the saved model
        :param domain: domain used for pretraining
        :param project_id: id of current project
        :param base_model: the base model for training
        :return: the model path
        """
        return os.path.join(domain.value, project_id, base_model.value)

    def __load_model(self) -> PreTrainedModel:
        """
        Loads the model from the pretrained model path
        :return: the PreTrainedModel object
        """
        config = AutoConfig.from_pretrained(self.model_path)
        config.num_labels = 2
        return self.base_model_class.from_pretrained(self.model_path, config=config)

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
            self.__tokenizer = AutoTokenizer.from_pretrained(self.model_path)
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
        return self.get_tokenizer()(truncation="longest_first", return_attention_mask=True, max_length=self._max_seq_length,
                                    padding="max_length", return_token_type_ids=return_token_type_ids, **kwargs)
