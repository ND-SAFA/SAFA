from typing import Dict, List, Union

from transformers.configuration_utils import PretrainedConfig
from transformers.tokenization_utils_base import BatchEncoding

from data.datasets.data_key import DataKey
from models.llama.configuration_llama import LLaMAConfig
from models.llama.llama_task import LLaMATask
from models.llama.tokenization_llama import LLaMATokenizer
from models.model_manager import ModelManager
from models.model_properties import ModelArchitectureType, ModelSize


class LLaMAModelManager(ModelManager):

    def __init__(self, model_path: str, model_output_path: str = None,
                 model_task: LLaMATask = LLaMATask.SEQUENCE_CLASSIFICATION,
                 model_size: ModelSize = ModelSize.BASE,
                 model_architecture: ModelArchitectureType = ModelArchitectureType.SINGLE,
                 layers_to_freeze: List[int] = None):
        """
        Handles loading model and related functions
        :param model_path: The path to the saved model
        :param model_task: The task the model should perform (e.g. masked learning model or sequence classification)
        :param model_size: The size of the model
        :param model_architecture: Whether the model should be siamese or single
        """
        super().__init__(model_path, model_output_path, model_task, model_size, model_architecture, layers_to_freeze=layers_to_freeze)

    def _load_model(self):
        """
        Loads the model from the pretrained model path
        :return: the PreTrainedModel object
        """
        model = self.model_task.value.from_pretrained(self.model_path, config=self._config)
        model._set_gradient_checkpointing(model, True)
        return model

    def get_config(self) -> PretrainedConfig:
        """
        Gets the PreTrainedModel configuration.
        :return: the PreTrainedModel object
        """
        if self._config is None:
            self._config = LLaMAConfig.from_pretrained("decapoda-research/llama-7b-hf")
        return self._config

    def get_tokenizer(self) -> LLaMATokenizer:
        """
        Gets the pretrained Tokenizer
        :return: the Tokenizer
        """
        if self._tokenizer is None:
            self._tokenizer = LLaMATokenizer.from_pretrained("decapoda-research/llama-7b-hf")
            if self._tokenizer.pad_token is None:
                vocab = self._tokenizer.get_vocab()
                vocab_tokens, vocab_indices = list(vocab.keys()), list(vocab.values())
                self._tokenizer.add_special_tokens({'pad_token': vocab_tokens[self.get_config().pad_token_id]})
        return self._tokenizer

    def get_feature(self, return_token_type_ids: bool = False, text: Union[str, List[str]] = None,
                    text_pair: Union[str, List[str]] = None, **kwargs) -> List[Dict]:
        """
        Method to get the feature for the model
        :param return_token_type_ids: if True, returns the token type ids
        :param text: The text of 1 artifact to encode
        :param text_pair: The text of the 2nd artifact in the pair to encode
        :param kwargs: other arguments for tokenizer
        :return: feature name, value mappings
        """
        assert text and text_pair, "text and text_pair must be supplied for llama tokenization"
        text = [text] if not isinstance(text, List) else text
        text_pair = [text_pair] if not isinstance(text_pair, List) else text_pair
        assert len(text) == len(text_pair), "Must include the same number of text and text pairs"
        feature_generation_method = self.get_similarity_feature if self.model_task == LLaMATask.SEQUENCE_SIMILARITY \
            else self.get_classification_feature
        features = feature_generation_method(text, text_pair, **kwargs)
        return features

    @staticmethod
    def get_prompt(text: str = None, text_pair: str = None) -> str:
        """
        Gets the input prompt for the source and target
        :param text:
        :param text_pair:
        :return:
        """
        return f"Source: {text} \nTarget: {text_pair}"

    def get_classification_feature(self, text: List[str] = None, text_pair: List[str] = None, **kwargs) -> BatchEncoding:
        """
        Method to get the feature from the tokenization when the task is classification
        :param text: The text of 1 artifact to encode
        :param text_pair: The text of the 2nd artifact in the pair to encode
        :return: The features
        """
        prompts = [LLaMAModelManager.get_prompt(source, text_pair[i]) for i, source in enumerate(text)]
        tokenizer = self.get_tokenizer()
        return tokenizer(text=prompts, **kwargs)

    def get_similarity_feature(self, text: List[str] = None, text_pair: List[str] = None, **kwargs) -> BatchEncoding:
        """
        Method to get the feature from the tokenization when the task is similarity
        :param text: The text of 1 artifact to encode
        :param text_pair: The text of the 2nd artifact in the pair to encode
        :return: The features
        """
        features1 = self.get_classification_feature(text, text_pair, **kwargs)
        features2 = self.get_classification_feature(text_pair, text, **kwargs)

        for i in range(len(features1[DataKey.INPUT_IDS])):
            features1[DataKey.INPUT_IDS][i].extend(features2[DataKey.INPUT_IDS][i])
            features1[DataKey.ATTEN_MASK][i].extend(features2[DataKey.ATTEN_MASK][i])
        return features1
