from dataclasses import dataclass, field

from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.tools.constants.default_model_managers import get_best_default_llm_manager_long_context
from common_resources.tools.state_management.args import Args


@dataclass
class ContradictionsArgs(Args):
    """
     :param llm_manager: The LLM manager to use to make decisions.
    """
    max_context: int = None
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
