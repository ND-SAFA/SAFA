from typing import Tuple

from tgen.core.args.anthropic_args import AnthropicArgs
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager


class ModelUtil:
    """
    Contains utility methods for selecting models
    """
    model_map = {
        "gpt": {
            "model": "text-davinci-003",
            "util": OpenAIManager,
        },
        "anthropic": {
            "model": "claude-instant-v1-100k",
            "util": AnthropicManager
        }
    }

    @staticmethod
    def is_llm(model: str) -> bool:
        """
        Returns true if model is LLM, false otherwise.
        :param model: The model identifier.
        :return: Whether model is LLM.
        """
        return model.lower().strip() in ModelUtil.model_map

    @staticmethod
    def get_model_manager(llm_name: str) -> Tuple[str, AbstractLLMManager]:
        """
        Returns the model and corresponding LLM manager for given library name.
        :param llm_name: The id of the LLM library.
        :return: The current best model and its manager.
        """
        llm_name = llm_name.lower()
        assert llm_name in ModelUtil.model_map, f"Model should be one of {list(ModelUtil.model_map.keys())}"
        model = ModelUtil.model_map[llm_name]["model"]
        llm_manager = None
        if llm_name == "anthropic":
            llm_manager = AnthropicManager(llm_args=AnthropicArgs(model=model))
        elif llm_name == "gpt":
            llm_manager = OpenAIManager(llm_args=OpenAIArgs(model=model))

        return model, llm_manager
