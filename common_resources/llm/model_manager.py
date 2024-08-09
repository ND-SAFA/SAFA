import gc

import torch
from torch.nn.parameter import Parameter
from transformers import AutoConfig, PreTrainedModel, PretrainedConfig
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.tokenization_utils import PreTrainedTokenizer
from typing import Dict, List, Optional, Type

from common_resources.tools.constants.symbol_constants import PERIOD
from common_resources.tools.constants.hugging_face_constants import MAX_SEQ_LENGTH_DEFAULT
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.override import overrides
from common_resources.llm\
    .model_properties import ModelArchitectureType, ModelSize, ModelTask

LAYER = List[Parameter]


class ModelManager(BaseObject):
    _max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT

    def __init__(self, model_path: str, model_output_path: str = None,
                 model_task: ModelTask = ModelTask.SEQUENCE_CLASSIFICATION,
                 model_size: ModelSize = ModelSize.BASE,
                 model_architecture: ModelArchitectureType = ModelArchitectureType.SINGLE,
                 layers_to_freeze: List[int] = None):
        """
        Handles loading model and related functions
        :param model_path: The path to the saved model
        :param model_output_path: Path to contain all output related to checkpoints and training and prediction.
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

    def set_model(self, model) -> None:
        """
        Sets the current model of the manager.
        :param model: The model to set.
        :return: None
        """
        self._model = model

    def get_config(self) -> PretrainedConfig:
        """
        Gets the PreTrainedModel configuration.
        :return: the PreTrainedModel object
        """
        if self._config is None:
            self._config = AutoConfig.from_pretrained(self.model_path)
            if not self._config.num_labels:
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
        torch.cuda.empty_cache()

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
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_path, eos_token='[EOS]')
            if self._tokenizer.pad_token is None:
                config = self.get_config()
                config.pad_token_id = -1 if config.pad_token_id is None else config.pad_token_id
                vocab = self._tokenizer.get_vocab()
                vocab_tokens, vocab_indices = list(vocab.keys()), list(vocab.values())
                self._tokenizer.add_special_tokens({'pad_token': vocab_tokens[config.pad_token_id]})
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
    def get_encoder_layers(model: PreTrainedModel, layer_identifier: str = "layer") -> List[LAYER]:
        """
        Returns a list of layers represented by a list of their parameters
        :param model: The model to gather layers for
        :param layer_identifier: The identifier used to distinguish layers.
        :return: a list of layers represented by a list of their parameters
        """
        layers = {}
        for name, param in model.named_parameters():
            descr = name.split(PERIOD)
            if layer_identifier in descr:
                layer_no = int(descr[descr.index(layer_identifier) + 1])
                if layer_no not in layers:
                    layers[layer_no] = []
                layers[layer_no].append(param)
        return [layers[i] for i in range(len(layers))]

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from common_resources.llm.supported_model_manager import SupportedModelManager
        return SupportedModelManager

    def _freeze_layers(self, model: PreTrainedModel, layers_to_freeze: List[int]) -> None:
        """
        Freezes the layer corresponding with the given numbers.
        :param model: The model whose layers get frozen.
        :param layers_to_freeze: Number of the layers to freeze. If negative number given, layer will be that many from end
        :return: None
        """
        layers = self.get_encoder_layers(model)
        logger.info(f"Layers: {len(layers)}")
        for layer_no in layers_to_freeze:
            layer = layers[layer_no]
            for param in layer:
                param.requires_grad = False
        logger.info(f"Successfully froze {len(layers)} layers.")
