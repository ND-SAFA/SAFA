import os
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.hgen_constants import DEFAULT_LINK_THRESHOLD
from tgen.common.util.base_object import BaseObject
from tgen.common.util.dataclass_util import required_field, DataclassUtil
from tgen.common.constants.model_constants import get_best_default_llm_manager, get_efficient_default_llm_manager
from tgen.common.util.str_util import StrUtil
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.state.pipeline.pipeline_args import PipelineArgs


class PredictionStep(Enum):
    INSTRUCTIONS = auto()
    FORMAT = auto()
    GENERATION = auto()
    REFINEMENT = auto()
    NAME = auto()


DEFAULT_MAX_TOKENS = 50000
DEFAULT_MAX_TOKENS_SMALL = 2000


@dataclass
class HGenArgs(PipelineArgs, BaseObject):
    """
    The layer of the source artifacts for which higher-level artifacts will be generated
    """
    source_layer_id: str = required_field(field_name="source_layer_id")
    """
    The type of higher-level artifact that will be generated
    """
    target_type: str = required_field(field_name="target_type")
    """
    The type of source artifacts for which higher-level artifacts will be generated
    """
    source_type: str = "code"
    """
    The LLM manager to use to generate the new artifact content and other more complex tasks
    """
    hgen_llm_manager_best: AbstractLLMManager = field(default_factory=get_best_default_llm_manager)
    """
    The LLM manager to use to generate the artifact names and less complex tasks
    """
    hgen_llm_manager_efficient: AbstractLLMManager = field(default_factory=get_efficient_default_llm_manager)
    """
    Max tokens to use for predictions.
    """
    max_tokens: Dict[int, int] = field(default_factory=dict)
    """
    If True, re-summarizes artifacts with a summary of the project 
    """
    create_new_code_summaries: bool = False
    """
    If True, re-runs hgen multiple times to get the best results across runs
    """
    optimize_with_reruns: bool = False
    """
    Number of re-runs of hgen to get the best results across runs
    """
    n_reruns: int = 4
    """
    If True, automatically generates trace links between the new hgen layers and the source
    """
    generate_trace_links: bool = True
    """
    If True, creates clusters of related artifacts to create higher levels of docs for 
    """
    perform_clustering: bool = True
    """
    The llm manager to use for each prediction step
    """
    llm_managers: Dict[int, AbstractLLMManager] = field(default_factory=dict, init=False)
    """
    The threshold below which trace links will get filtered out
    """
    link_selection_threshold: float = DEFAULT_LINK_THRESHOLD

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided and converts Enum into the proper class
        :return: None
        """
        super().__post_init__()
        self.llm_managers = {e.value: (self.hgen_llm_manager_best if e != PredictionStep.NAME
                                       else self.hgen_llm_manager_efficient) for e in PredictionStep}
        self.export_dir = os.path.join(self.export_dir, self.target_type) \
            if self.export_dir and not self.export_dir.endswith(self.target_type) else self.export_dir
        self.llm_managers[PredictionStep.FORMAT.value] = OpenAIManager(OpenAIArgs(model='gpt-4-0314'))
        for e in PredictionStep:
            if e.value not in self.max_tokens:
                if e in [PredictionStep.NAME, PredictionStep.FORMAT]:
                    self.max_tokens[e.value] = DEFAULT_MAX_TOKENS_SMALL
                else:
                    self.max_tokens[e.value] = DEFAULT_MAX_TOKENS

