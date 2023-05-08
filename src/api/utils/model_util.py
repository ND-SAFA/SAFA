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
            "util": OpenAIManager()
        },
        "anthropic": {
            "model": "claude-v1.3",
            "util": AnthropicManager()
        }
    }

    @staticmethod
    def get_default_model() -> str:
        """
        :return: Returns the default library key.
        """
        return "gpt"

    @staticmethod
    def get_model_manager(llm_name) -> AbstractLLMManager:
        """
        Returns the model and corresponding LLM manager for given library name.
        :param llm_name: The id of the LLM library.
        :return: The current best model and its manager.
        """
        assert llm_name in ModelUtil.model_map, f"Model should be one of {list(ModelUtil.model_map.keys())}"
        model = ModelUtil.model_map[llm_name]["model"]
        llm_manager = ModelUtil.model_map[llm_name]["util"]
        return model, llm_manager
