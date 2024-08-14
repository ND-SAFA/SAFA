from dataclasses import dataclass, field
from typing import List

from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.tools.constants.default_model_managers import get_best_default_llm_manager_long_context
from common_resources.tools.state_management.args import Args
from common_resources.tools.util.dataclass_util import required_field

from tgen.common.objects.artifact import Artifact


@dataclass
class ConceptArgs(Args):
    """
    DataFrame containing only concepts to match.
    """
    concept_layer_id: str = required_field(field_name="concept_layer_id")
    """
    Artifact to match concepts against.
    """
    artifacts: List[Artifact] = required_field(field_name="artifacts")
    """"
    LLM Manager used to complete prompts
    """
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    """
    Layer ID to given extracted entities.
    """
    entity_layer_id = "Entity"
    """
    If provided, is used for defining unknown entities.
    """
    context_doc_path: str = None
    """
    If True, uses the llm for entity extraction instead of the standford analysis.
    """
    use_llm_for_entity_extraction: bool = True
