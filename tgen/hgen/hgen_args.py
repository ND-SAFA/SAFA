from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Union

from tgen.common.constants.hgen_constants import DEFAULT_DUPLICATE_SIMILARITY_THRESHOLD, DEFAULT_LINK_THRESHOLD, \
    DEFAULT_ORPHAN_THRESHOLD, DEFAULT_REDUCTION_PERCENTAGE_GENERATIONS
from tgen.common.constants.model_constants import get_best_default_llm_manager, get_efficient_default_llm_manager
from tgen.common.constants.open_ai_constants import OPEN_AI_MODEL_DEFAULT
from tgen.common.constants.project_summary_constants import PS_ENTITIES_TITLE
from tgen.common.util.base_object import BaseObject
from tgen.common.util.dataclass_util import required_field
from tgen.common.util.file_util import FileUtil
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.pipeline.pipeline_args import PipelineArgs


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
    source_layer_ids: Union[str, List[str]] = required_field(field_name="source_layer_id")
    """
    The type of higher-level artifact that will be generated
    """
    target_type: str = required_field(field_name="target_type")
    """
    The type of source artifacts for which higher-level artifacts will be generated
    """
    source_type: str = None
    """
    The LLM manager to use to generate the new artifact content and other more complex tasks
    """
    hgen_llm_manager_best: AbstractLLMManager = field(default_factory=get_best_default_llm_manager)
    """
    The LLM manager to use to generate the artifact names and less complex tasks
    """
    hgen_llm_manager_efficient: AbstractLLMManager = field(default_factory=get_efficient_default_llm_manager)
    """
    The LLM manager to use to generate the inputs during step 2
    """
    inputs_llm_manager: AbstractLLMManager = field(default_factory=lambda: OpenAIManager(OpenAIArgs(model=OPEN_AI_MODEL_DEFAULT)))
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
    run_refinement: bool = True
    """
    If True, automatically generates trace links between the new hgen layers and the source
    """
    generate_trace_links: bool = True
    """
    If True, automatically generates trace links explanations
    """
    generate_explanations: bool = True
    """
    If True, creates clusters of related artifacts to create higher levels of docs for 
    """
    perform_clustering: bool = True
    """
    If True, adds already linked artifacts to the cluster that their parent is in
    """
    add_linked_artifacts_to_cluster: bool = False
    """
    The llm manager to use for each prediction step
    """
    llm_managers: Dict[int, AbstractLLMManager] = field(default_factory=dict, init=False)
    """
    The threshold below which trace links will get filtered out
    """
    link_selection_threshold: float = DEFAULT_LINK_THRESHOLD
    """
    Threshold for which all orphan links have to exceed or equal.
    """
    min_orphan_score_threshold: float = DEFAULT_ORPHAN_THRESHOLD
    """
    Threshold for which generated artifacts are deemed duplicates.
    """
    duplicate_similarity_threshold: float = DEFAULT_DUPLICATE_SIMILARITY_THRESHOLD
    """
    Percent of the number of children artifacts that will be the number generated.
    """
    reduction_percentage: float = DEFAULT_REDUCTION_PERCENTAGE_GENERATIONS
    """
    The section of the project summary to use as seeds for clustering.
    """
    seed_project_summary_section: str = None
    """
    The layer_id of the artifacts to use as seeds
    """
    seed_layer_id: str = None
    """
    Adds clusters as artifacts
    """
    add_seeds_as_artifacts: bool = False
    """
    Whether to only export the content produced by HGEN, otherwise, original dataset is exported too.
    """
    export_original_dataset: bool = False
    """
    The sections of the project summary to include in content generation.
    """
    content_generation_project_summary_sections: List[str] = field(default_factory=lambda: [PS_ENTITIES_TITLE])

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided and converts Enum into the proper class
        :return: None
        """
        super().__post_init__()
        if not self.source_type:
            is_code = all([layer_id in self.dataset.artifact_df.get_code_layers() for layer_id in self.source_layer_ids])
            self.source_type = "code" if is_code else self.source_layer_ids[0]
        self.llm_managers = {e.value: (self.hgen_llm_manager_best if e != PredictionStep.NAME
                                       else self.hgen_llm_manager_efficient) for e in PredictionStep}
        self.export_dir = FileUtil.safely_join_paths(self.export_dir, self.target_type) \
            if not self.export_dir.endswith(self.target_type) else self.export_dir
        self.llm_managers[PredictionStep.FORMAT.value] = self.inputs_llm_manager
        for e in PredictionStep:
            if e.value not in self.max_tokens:
                if e in [PredictionStep.NAME, PredictionStep.FORMAT]:
                    self.max_tokens[e.value] = DEFAULT_MAX_TOKENS_SMALL
                else:
                    self.max_tokens[e.value] = DEFAULT_MAX_TOKENS

        if isinstance(self.source_layer_ids, str):
            self.source_layer_ids = [self.source_layer_ids]

    def get_seed_id(self, raise_exception: bool=True) -> str:
        """
        Gets the id of the seed layer.
        :param raise_exception: If True, raises an exception if no seed args are set.
        :return: The current seed layer id.
        """
        if self.seed_project_summary_section:
            return self.seed_project_summary_section
        if self.seed_layer_id:
            return self.seed_layer_id
        if raise_exception:
            raise Exception("No seed id available. Seed project Summary and layer_id are none.")
