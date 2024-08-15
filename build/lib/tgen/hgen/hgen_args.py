from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Union

from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.llm.args.open_ai_args import OpenAIArgs
from common_resources.llm.open_ai_manager import OpenAIManager
from common_resources.tools.constants.default_model_managers import get_best_default_llm_manager_long_context, \
    get_best_default_llm_manager_short_context, get_efficient_default_llm_manager
from common_resources.tools.constants.open_ai_constants import OPEN_AI_MODEL_DEFAULT
from common_resources.tools.state_management.args import Args
from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.dataclass_util import required_field
from common_resources.tools.util.file_util import FileUtil

from tgen.common.constants.hgen_constants import DEFAULT_CLUSTER_MAX_SIZE, DEFAULT_DUPLICATE_SIMILARITY_THRESHOLD, \
    DEFAULT_LINK_THRESHOLD, DEFAULT_REDUCTION_PERCENTAGE_GENERATIONS, USE_ALL_CODE_LAYERS, USE_ALL_LAYERS
from tgen.common.constants.project_summary_constants import PS_ENTITIES_TITLE
from tgen.common.constants.ranking_constants import DEFAULT_COMPLETION_TOKENS
from tgen.hgen.common.special_doc_types import DOC_TYPE2CONSTRAINTS, DocTypeConstraints


class PredictionStep(Enum):
    INSTRUCTIONS = auto()
    FORMAT = auto()
    GENERATION = auto()
    REFINEMENT = auto()
    NAME = auto()


@dataclass
class HGenArgs(Args, BaseObject):
    # ================ REQUIRED PARAMS ================
    """
    The layer of the source artifacts for which higher-level artifacts will be generated
    """
    source_layer_ids: Union[str, List[str]] = required_field(field_name="source_layer_id")
    """
    The type of higher-level artifact that will be generated
    """
    target_type: str = required_field(field_name="target_type")

    # ================ OPTIONAL PARAMS (ALPHABETIZED) ================
    """
    Adds clusters as artifacts
    """
    add_linked_artifacts_to_cluster: bool = False
    """
    If True, allows orphans in the clustering process
    """
    allow_orphans: bool = True
    """
    The maximum size of a cluster
    """
    cluster_max_size: int = DEFAULT_CLUSTER_MAX_SIZE
    """
    If True, creates clusters of related artifacts to create higher levels of docs for 
    """
    perform_clustering: bool = True
    """
    If True, adds already linked artifacts to the cluster that their parent is in
    """
    add_seeds_as_artifacts: bool = False
    """
    The sections of the project summary to include in content generation.
    """
    content_generation_project_summary_sections: List[str] = field(default_factory=lambda: [PS_ENTITIES_TITLE])
    """
    If True, re-summarizes artifacts with a summary of the project 
    """
    create_new_code_summaries: bool = False
    """
    Threshold for which generated artifacts are deemed duplicates.
    """
    duplicate_similarity_threshold: float = DEFAULT_DUPLICATE_SIMILARITY_THRESHOLD
    """
    Whether to only export the content produced by HGEN, otherwise, original dataset is exported too.
    """
    export_hgen_artifacts_only: bool = False
    """
    If True, automatically generates trace links explanations
    """
    generate_explanations: bool = True
    """
    The LLM manager to use to generate the new artifact content and other more complex, longer tasks
    """
    hgen_llm_manager_best_long_context: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    """
    The LLM manager to use to generate the artifact for short context windows
    """
    hgen_llm_manager_best_short_context: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_short_context)
    """
    The LLM manager to use to generate the artifact less complex tasks
    """
    hgen_llm_manager_efficient: AbstractLLMManager = field(default_factory=get_efficient_default_llm_manager)
    """
    If True, seed will be provided to model when generating.
    """
    include_seed_in_prompt: bool = False
    """
    The LLM manager to use to generate the inputs during step 2
    """
    inputs_llm_manager: AbstractLLMManager = field(default_factory=lambda: OpenAIManager(OpenAIArgs(model=OPEN_AI_MODEL_DEFAULT)))
    """
    True if lowest layer (generally code).
    """
    is_first_layer: bool = True
    """
    The threshold below which trace links will get filtered out
    """
    link_selection_threshold: float = DEFAULT_LINK_THRESHOLD
    """
    The llm manager to use for each prediction step
    """
    llm_managers: Dict[int, AbstractLLMManager] = field(default_factory=dict, init=False)
    """
    Max tokens to use for predictions.
    """
    max_tokens: Dict[int, int] = field(default_factory=dict)
    """
    Threshold for which all orphan links have to exceed or equal.
    """
    min_orphan_score_threshold: float = None
    """
    Percent of the number of children artifacts that will be the number generated.
    """
    reduction_percentage: float = DEFAULT_REDUCTION_PERCENTAGE_GENERATIONS
    """
    If True, detects and potentially removes overlapping artifacts.
    """
    detect_duplicates: bool = True
    """
    If True, re-runs hgen multiple times to get the best results across runs
    """
    run_refinement: bool = True
    """
    The layer_id of the artifacts to use as seeds
    """
    seed_layer_id: str = None
    """
    The section of the project summary to use as seeds for clustering.
    """
    seed_project_summary_section: str = None
    """
    The type of source artifacts for which higher-level artifacts will be generated
    """
    source_type: str = None

    def __post_init__(self) -> None:
        """
        Asserts necessary params have been provided and converts Enum into the proper class
        :return: None
        """
        super().__post_init__()
        self._replace_constants_in_source_layer_ids()
        if not self.source_type:
            self._determine_source_type()
        self._set_export_dir()
        self._set_llm_variables()

        if isinstance(self.source_layer_ids, str):
            self.source_layer_ids = [self.source_layer_ids]

        if self.check_target_type_constraints(DocTypeConstraints.ONE_TARGET_PER_SOURCE):
            self.generate_explanations = False
            self.detect_duplicates = False
            self.run_refinement = False

    def _set_llm_variables(self) -> None:
        """
        Sets the llm manager map and the max tokens for each hgen step.
        :return: None
        """
        self.llm_managers = {e.value: (self.hgen_llm_manager_best_long_context
                                       if e != PredictionStep.NAME else self.hgen_llm_manager_best_long_context
                                       ) for e in PredictionStep}
        self.llm_managers[PredictionStep.FORMAT.value] = self.inputs_llm_manager
        for e in PredictionStep:
            if e.value not in self.max_tokens:
                self.max_tokens[e.value] = DEFAULT_COMPLETION_TOKENS

    def _set_export_dir(self) -> None:
        """
        Sets the export dir to the appropriate sub folder to save to.
        :return: None
        """
        self.export_dir = FileUtil.safely_join_paths(self.export_dir, self.target_type) \
            if not self.export_dir.endswith(self.target_type) else self.export_dir

    def _determine_source_type(self) -> None:
        """
        Determines and sets the source type using the source layer ids.
        :return: None
        """
        is_code = all([layer_id in self.dataset.artifact_df.get_code_layers() for layer_id in self.source_layer_ids])
        self.source_type = "code" if is_code else self.source_layer_ids[0]

    def _replace_constants_in_source_layer_ids(self) -> None:
        """
        Replaces any constant values in the source layer ids.
        :return: None.
        """
        if USE_ALL_CODE_LAYERS in self.source_layer_ids:
            self.source_layer_ids.remove(USE_ALL_CODE_LAYERS)
            self.source_layer_ids.extend(self.dataset.artifact_df.get_code_layers())
        elif USE_ALL_LAYERS in self.source_layer_ids:
            self.source_layer_ids.remove(USE_ALL_LAYERS)
            self.source_layer_ids.extend(self.dataset.artifact_df.get_artifact_types())

    def get_seed_id(self, raise_exception: bool = True) -> str:
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

    def check_target_type_constraints(self, constraint: DocTypeConstraints) -> bool:
        """
        Checks whether the target type has the given constraint.
        :param constraint: A possible constraint on the target type.
        :return: True if the target type has the given constraint else False.
        """
        return constraint in DOC_TYPE2CONSTRAINTS.get(self.target_type.upper(), set())
