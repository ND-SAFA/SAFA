from dataclasses import field, dataclass

from tgen.common.constants.model_constants import get_best_default_llm_manager_long_context
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.pipeline.pipeline_args import PipelineArgs


@dataclass
class ContradictionsArgs(PipelineArgs):
    """
     :param llm_manager: The LLM manager to use to make decisions.
    """
    max_context: int = None
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
