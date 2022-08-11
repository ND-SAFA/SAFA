import os
from typing import Dict

from transformers import AutoConfig, AutoTokenizer
from transformers.modeling_utils import PreTrainedModel

from config.constants import MAX_SEQ_LENGTH_DEFAULT
from models.base_models.supported_base_model import SupportedBaseModel
from models.model_properties import ArchitectureType, ModelSize
from pretrain.corpuses.domain import Domain


class ModelGenerator:
    """
    Represents a learning model
    """
    __tokenizer: AutoTokenizer = None
    __model: PreTrainedModel = None
    _max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT

    def __init__(self, base_model_name: str, model_path: str, model_size: ModelSize = ModelSize.BASE):
        """
        Handles loading model and related functions
        :param model_path: the path to the saved model
        """
        self.model_path = model_path
        self.model_name = base_model_name
        self.base_model = self._get_supported_base_model(self.model_name)
        self.base_model_class = self.base_model.value
        self.arch_type = self._get_model_architecture_type(self.model_name)
        self.model_size = model_size

    @staticmethod
    def _get_supported_base_model(model_name: str) -> SupportedBaseModel:
        """
        Gets the supported base model
        :param model_name: the name of the model
        :return: the SupportedBaseModel
        """
        try:
            return SupportedBaseModel[model_name]
        except KeyError:
            raise NameError("Model name %s unknown" % model_name)

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

    # this may not be needed but keeping for now...
    @staticmethod
    def create_path(domain: Domain, base_model: SupportedBaseModel, project_id: str, ) -> str:
        """
        Creates the path to the saved model
        :param domain: domain used for pretraining
        :param project_id: id of current project
        :param base_model: the base model for training
        :return: the model path
        """
        return os.path.join(domain.value, base_model.value, project_id)

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
        return self.get_tokenizer()(truncation="longest_first", return_attention_mask=True,
                                    max_length=self._max_seq_length,
                                    padding="max_length", return_token_type_ids=return_token_type_ids, **kwargs)
