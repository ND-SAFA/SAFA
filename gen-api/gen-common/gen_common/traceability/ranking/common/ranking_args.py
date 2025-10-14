import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

from gen_common.constants import environment_constants
from gen_common.constants.default_model_managers import get_best_default_llm_manager_long_context, \
    get_efficient_default_llm_manager
from gen_common.constants.environment_constants import DEFAULT_CROSS_ENCODER_MODEL, DEFAULT_EMBEDDING_MODEL
from gen_common.constants.model_constants import DEFAULT_TEST_EMBEDDING_MODEL
from gen_common.constants.ranking_constants import DEFAULT_EMBEDDINGS_SCORE_WEIGHT, DEFAULT_EXPLANATION_SCORE_WEIGHT, \
    DEFAULT_LINK_THRESHOLD, \
    DEFAULT_MAX_CONTEXT_ARTIFACTS, \
    DEFAULT_PARENT_MIN_THRESHOLD, \
    DEFAULT_PARENT_PRIMARY_THRESHOLD, \
    DEFAULT_PARENT_SECONDARY_THRESHOLD, \
    DEFAULT_SCALED_THRESHOLD, DEFAULT_SORTING_ALGORITHM, \
    GENERATE_EXPLANATIONS_DEFAULT
from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.llm.abstract_llm_manager import AbstractLLMManager
from gen_common.pipeline.args import Args
from gen_common.traceability.ranking.filters.supported_filters import SupportedFilter
from gen_common.traceability.ranking.sorters.supported_sorters import SupportedSorter
from gen_common.traceability.ranking.trace_selectors.selection_methods import SupportedSelectionMethod
from gen_common.traceability.relationship_manager.cross_encoder_manager import CrossEncoderManager
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common.util.dataclass_util import required_field
from gen_common.util.file_util import FileUtil


@dataclass
class RankingArgs(Args):
    """
    parent_ids: List of parent artifact ids.
    """
    parent_ids: List[str] = required_field(field_name="parent_ids")
    """
    children_ids: List of children ids to compare to each parent.
    """
    children_ids: List[str] = required_field(field_name="children_ids")
    """
    types_to_trace: Contains the parent_type, child_type
    """
    types_to_trace: Tuple[str, str] = required_field(field_name="types2trace")
    """
    - pre_sorted_parent2children: Maps parent ids to their children ids if there are already some sorted children ids
    """
    pre_sorted_parent2children: Optional[Dict[str, List[str]]] = None
    """
    - run_name: The unique identifier of this run.
    """
    run_name: str = EMPTY_STRING
    """
    - max_children_per_query: The number of maximum children to give to claude
    """
    max_children_per_query: int = None
    """ 
    - sorter: The sorting algorithm to use before ranking with claude
    """
    sorter: Union[str, SupportedSorter] = DEFAULT_SORTING_ALGORITHM
    """ 
    - filter: If provided, sets scores of filtered out children to 0 using provided filter.
    """
    filter: SupportedFilter = None
    """
    - generate_explanations: Whether to generate explanations for links.
    """
    generate_explanations: bool = GENERATE_EXPLANATIONS_DEFAULT
    """
    - ranking_llm_model: The model used to rank
    """
    ranking_llm_model_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    """
    - rewrite_artifacts: If True, rewrites the artifacts to be in the same format before tracing.
    """
    rewrite_artifacts: bool = False
    """
    - explanation_llm_model: The model used to create explanations
    """
    explanation_llm_model: AbstractLLMManager = field(default_factory=get_efficient_default_llm_manager)
    """
    - embedding_model: The model whose embeddings are used to rank children.
    """
    embedding_model_name: str = DEFAULT_EMBEDDING_MODEL
    """
    - ranking_model_name: The model whose predictions are used to re-rank children.
    """
    ranking_model_name: str = DEFAULT_CROSS_ENCODER_MODEL
    """
    - parent_thresholds: The threshold used to establish parents from (primary, secondary and min)
    """
    parent_thresholds: Tuple[float, float, float] = (DEFAULT_PARENT_PRIMARY_THRESHOLD,
                                                     DEFAULT_PARENT_SECONDARY_THRESHOLD,
                                                     DEFAULT_PARENT_MIN_THRESHOLD)
    """
    - max_context_artifacts: The maximum number of artifacts to consider in a context window. 
    """
    max_context_artifacts: int = DEFAULT_MAX_CONTEXT_ARTIFACTS
    """
    - link_threshold: The threshold at which to accept links when selecting top predictions.
    """
    link_threshold: float = DEFAULT_LINK_THRESHOLD
    """
    - selection_method: The method to use to select top predictions
    """
    selection_method: Optional[SupportedSelectionMethod] = SupportedSelectionMethod.SELECT_BY_THRESHOLD
    """
    - use_chunks: If True, uses the chunks of the artifacts.
    """
    use_chunks: bool = False
    """
    - weight_of_explanation_scores: If greater than 0, will weight the scores from the explanation in the final score
    """
    weight_of_explanation_scores: float = DEFAULT_EXPLANATION_SCORE_WEIGHT
    """
     - weight_of_embedding_scores: If greater than 0, will weight the scores from the embeddings in the final score 
     *applicable only for LLMPipeline*
     """
    weight_of_embedding_scores: float = DEFAULT_EMBEDDINGS_SCORE_WEIGHT
    """
    - relationship_manager: If provided, will be used in the sorting step if using an transformer sorter
    """
    embeddings_manager: EmbeddingsManager = None
    """
    - cross_encoder_manager: If provided, used to calculate rankings predictions.
    """
    cross_encoder_manager: CrossEncoderManager = None
    """
    - re_rank_children: If True, will re rank the children using a cross encoder
    """
    re_rank_children: bool = False
    """
    use_rag: If True, uses optimal parameters for RAG
    """
    use_rag_defaults: bool = False

    def save(self, obj: Any, file_name: str) -> str:
        """
        Saves object if export path is set.
        :param obj: The object to save.
        :param file_name: The file name to save under.
        :return: Path of file.
        """
        if self.export_dir is not None:
            self.export_dir = os.path.expanduser(self.export_dir)
            os.makedirs(self.export_dir, exist_ok=True)
            export_path = self.get_path(file_name)
            FileUtil.write_yaml(obj, export_path)
            logger.info(f"Saved object to: {export_path}")
            return export_path

    def load(self, file_name: str) -> Any:
        """
        Reads the object with given file name in export directory.
        :param file_name: The file name to load.
        :return: The loaded object.
        """
        file_path = self.get_path(file_name)
        obj = FileUtil.read_yaml(file_path)
        return obj

    def get_path(self, file_name: str):
        """
        Returns path to file in run.
        :param file_name: The name of the file.
        :return: Path to file in output directory.
        """
        path = FileUtil.safely_join_paths(self.export_dir, file_name)
        if path:
            path = os.path.expanduser(path)
        return path

    def parent_type(self) -> str:
        """
        Gets the parent type being traces
        :return: The parent type being traces
        """
        return self.types_to_trace[0]

    def child_type(self) -> str:
        """
        Gets the child type being traces
        :return: The child type being traces
        """
        return self.types_to_trace[1]

    @staticmethod
    def get_run_name(child_type: str, children_ids: List, parent_type: str, parent_ids: List) -> str:
        """
        Gets the run name for the child and parent type
        :param child_type: The type of the child artifacts
        :param children_ids: The list of ids of each possible child
        :param parent_type: The type of the parent artifacts
        :param parent_ids: The list of ids of each parent being linked
        :return: The run name
        """
        return f"{child_type}({len(children_ids)}) --> {parent_type}({len(parent_ids)})"

    def __post_init__(self) -> None:
        """
        Initializes ranking args with default embedding model if in production.
        :return: None
        """
        if not self.run_name:
            self.run_name = self.get_run_name(self.child_type(), self.children_ids, self.parent_type(), self.parent_ids)
        super().__post_init__()
        self.embedding_model_name = DEFAULT_TEST_EMBEDDING_MODEL if environment_constants.IS_TEST else self.embedding_model_name
        if self.use_rag_defaults:
            self.selection_method = SupportedSelectionMethod.SELECT_BY_THRESHOLD_SCALED
            self.link_threshold = DEFAULT_SCALED_THRESHOLD
            logger.warning(f"Selected a threshold of {DEFAULT_SCALED_THRESHOLD} for RAG.")
