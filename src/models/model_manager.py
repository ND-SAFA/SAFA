import gc
from typing import Dict, List, Optional

from torch.nn.parameter import Parameter
from transformers import AutoConfig, PretrainedConfig
from transformers.modeling_utils import PreTrainedModel
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizer

from constants import MAX_SEQ_LENGTH_DEFAULT
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
        :param model_path: The path to the saved model
        :param model_task: The task the model should perform (e.g. masked learning model or sequence classification)
        :param model_size: The size of the model
        :param model_architecture: Whether the model should be siamese or single
        :param layers_to_freeze: The layers to freeze during training
        """

        self._tokenizer: Optional[AutoTokenizer] = None
        self._model: Optional[PreTrainedModel] = None
        self._config: Optional[PretrainedConfig] = None
        self.model_path = model_path
        self.model_output_path = model_output_path
        self.model_task = model_task
        self.arch_type = model_architecture
        self.model_size = model_size
        self.layers_to_freeze = layers_to_freeze

    def _load_model(self) -> PreTrainedModel:
        """
        Loads the model from the pretrained model path
        :return: the PreTrainedModel object
        """
        config = self.get_config()
        model = self.model_task.value.from_pretrained(self.model_path, config=config)
        if self.layers_to_freeze:
            self._freeze_layers(model, self.layers_to_freeze)
        return model

    def get_model(self) -> PreTrainedModel:
        """
        Gets the PreTrainedModel
        :return: the PreTrainedModel object
        """
        if self._model is None:
            self._model = self._load_model()
        return self._model

    def get_config(self) -> PretrainedConfig:
        """
        Gets the PreTrainedModel configuration.
        :return: the PreTrainedModel object
        """
        if self._config is None:
            self._config = AutoConfig.from_pretrained(self.model_path)
            self._config.num_labels = 2
        return self._config

    def clear_model(self) -> None:
        """
        Removes reference to model.
        :return: None
        """
        del self._model  # need delete because other pointers exist in trainer
        del self._tokenizer
        self._model = None
        self._tokenizer = None
        gc.collect()

    def update_model(self, model_path: str) -> PreTrainedModel:
        """
        Updates the model path and reloads the model
        :param model_path: The path to the model
        :return: The updated model
        """
        self.clear_model()
        self.model_path = model_path
        return self.get_model()

    def get_tokenizer(self) -> PreTrainedTokenizer:
        """
        Gets the pretrained Tokenizer
        :return: the Tokenizer
        """
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_path, eos_token='[EOS]', pad_token="[PAD]")
        return self._tokenizer

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
        feature = tokenizer(truncation=True, return_attention_mask=True,
                            max_length=self._max_seq_length,
                            padding="max_length", return_token_type_ids=return_token_type_ids, **kwargs)
        return feature

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
