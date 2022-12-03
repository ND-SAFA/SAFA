from typing import Dict, Optional

from transformers import AutoConfig
from transformers.modeling_utils import PreTrainedModel
from transformers.models.auto import AutoModel
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizer

from config.constants import MAX_SEQ_LENGTH_DEFAULT
from models.base_models.supported_base_model import SupportedBaseModel
from models.model_properties import ModelArchitectureType, ModelSize, ModelTask


class ModelGenerator:
    """
    Represents a learning model
    """
    _max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT

    def __init__(self, model_path: str, model_task: ModelTask = ModelTask.SEQUENCE_CLASSIFICATION,
                 model_size: ModelSize = ModelSize.BASE,
                 model_architecture: ModelArchitectureType = ModelArchitectureType.SINGLE):
        """
        Handles loading model and related functions
        :param model_path: the path to the saved model
        """

        self.__tokenizer: Optional[AutoTokenizer] = None
        self.__model: Optional[PreTrainedModel] = None
        self.model_path = model_path
        self.model_task = model_task
        self.arch_type = model_architecture
        self.model_size = model_size

    def __load_model(self) -> PreTrainedModel:
        """
        Loads the model from the pretrained model path
        :return: the PreTrainedModel object
        """
        config = AutoConfig.from_pretrained(self.model_path)
        config.num_labels = 2
        return self.model_task.value.from_pretrained(self.model_path, config=config)

    def get_model(self) -> PreTrainedModel:
        """
        Gets the PreTrainedModel
        :return: the PreTrainedModel object
        """
        if self.__model is None:
            self.__model = self.__load_model()
        return self.__model

    def get_tokenizer(self) -> PreTrainedTokenizer:
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
        tokenizer = self.get_tokenizer()
        return tokenizer(truncation=True, return_attention_mask=True,
                         max_length=self._max_seq_length,
                         padding="max_length", return_token_type_ids=return_token_type_ids, **kwargs)
