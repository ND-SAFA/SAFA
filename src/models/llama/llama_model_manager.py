from typing import Dict, Union, List

from models.llama.configuration_llama import LLaMAConfig
from models.llama.modeling_llama import LLaMAPreTrainedModel
from models.llama.tokenization_llama import LLaMATokenizer
from models.model_manager import ModelManager


class LLaMAModelManager(ModelManager):

    def __init__(self, model_path: str):
        """
        Handles loading model and related functions
        :param model_path: The path to the model
        """
        super().__init__(model_path)

    def _load_model(self):
        self.__config = LLaMAConfig.from_pretrained(self.model_path)
        model = LLaMAPreTrainedModel.from_pretrained(self.model_path, config=self.__config)
        return model

    def get_tokenizer(self) -> LLaMATokenizer:
        """
        Gets the pretrained Tokenizer
        :return: the Tokenizer
        """
        if self._tokenizer is None:
            self._tokenizer = LLaMATokenizer.from_pretrained(self.model_path)
        return self._tokenizer

    def get_feature(self, return_token_type_ids: bool = False, text: Union[str, List[str]] = None,
                    text_pair: Union[str, List[str]] = None, **kwargs) -> Dict:
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
        tokenizer = self.get_tokenizer()
        prompts = [f"Source: {source} \nTarget: {text_pair[i]}" for i, source in enumerate(text)]
        return tokenizer(text=prompts)