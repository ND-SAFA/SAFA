from typing import Dict, List, Optional

from torch.nn.parameter import Parameter
from transformers import AutoConfig
from transformers.modeling_utils import PreTrainedModel
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizer

from config.constants import MAX_SEQ_LENGTH_DEFAULT
from models.model_properties import ModelArchitectureType, ModelSize, ModelTask
from util.base_object import BaseObject


class ModelManager(BaseObject):
    _max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    LAYER = List[Parameter]

    def __init__(self, model_path: str, model_output_path: str = None,
                 model_task: ModelTask = ModelTask.SEQUENCE_CLASSIFICATION,
                 model_size: ModelSize = ModelSize.BASE,
                 model_architecture: ModelArchitectureType = ModelArchitectureType.SINGLE,
                 layers_to_freeze: List[int] = None):
        """
        Handles loading model and related functions
        :param model_path: the path to the saved model
        """

        self.__tokenizer: Optional[AutoTokenizer] = None
        self.__model: Optional[PreTrainedModel] = None
        self.model_path = model_path
        self.model_output_path = model_output_path
        self.model_task = model_task
        self.arch_type = model_architecture
        self.model_size = model_size
        self.layers_to_freeze = layers_to_freeze

    def __load_model(self) -> PreTrainedModel:
        """
        Loads the model from the pretrained model path
        :return: the PreTrainedModel object
        """
        config = AutoConfig.from_pretrained(self.model_path)
        config.num_labels = 2
        model = self.model_task.value.from_pretrained(self.model_path, config=config)
        if self.layers_to_freeze:
            self._freeze_layers(model, self.layers_to_freeze)
        return model

    def get_model(self) -> PreTrainedModel:
        """
        Gets the PreTrainedModel
        :return: the PreTrainedModel object
        """
        if self.__model is None:
            self.__model = self.__load_model()
        return self.__model

    def clear_model(self) -> None:
        """
        Removes reference to model.
        :return: None
        """
        self.__model = None

    def get_tokenizer(self) -> PreTrainedTokenizer:
        """
        Gets the pretrained Tokenizer
        :return: the Tokenizer
        """
        if self.__tokenizer is None:
            print("TOKENIZER:", self.model_path)
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

    @staticmethod
    def get_encoder_layers(model: PreTrainedModel) -> List[LAYER]:
        """
        Returns a list of layers represented by a list of their parameters
        :return: a list of layers represented by a list of their parameters
        """
        layers = {}
        for name, param in model.named_parameters():
            descr = name.split(".")
            if "layer" in descr:
                layer_no = int(descr[descr.index("layer") + 1])
                if layer_no not in layers:
                    layers[layer_no] = []
                layers[layer_no].append(param)
        return [layers[i] for i in range(len(layers))]

    def _freeze_layers(self, model: PreTrainedModel, layers_to_freeze: List[int]) -> None:
        """
        Freezes the layer corresponding with the given numbers.
        :param layers_to_freeze: Number of the layers to freeze. If negative number given, layer will be that many from end
        :return: None
        """
        layers = self.get_encoder_layers(model)
        for layer_no in layers_to_freeze:
            layer = layers[layer_no]
            for param in layer:
                param.requires_grad = False
