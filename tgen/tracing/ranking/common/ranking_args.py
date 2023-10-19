import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from tgen.common.constants.model_constants import get_best_default_llm_manager, get_efficient_default_llm_manager
from tgen.common.constants.ranking_constants import DEFAULT_LINK_THRESHOLD, \
    DEFAULT_MAX_CONTEXT_ARTIFACTS, \
    DEFAULT_PARENT_MIN_THRESHOLD, \
    DEFAULT_PARENT_PRIMARY_THRESHOLD, \
    DEFAULT_SORTING_ALGORITHM, DEFAULT_EMBEDDING_MODEL, DEFAULT_EXPLANATION_SCORE_WEIGHT, \
    GENERATE_EXPLANATIONS_DEFAULT, DEFAULT_EMBEDDINGS_SCORE_WEIGHT
from tgen.common.util.dataclass_util import required_field
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.state.pipeline.pipeline_args import PipelineArgs
from tgen.tracing.ranking.selectors.selection_methods import SupportedSelectionMethod


@dataclass
class RankingArgs(PipelineArgs):
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
    run_name: str = "default_run"
    """
    - max_children_per_query: The number of maximum children to give to claude
    """
    max_children_per_query: int = None
    """ 
    - sorter: The sorting algorithm to use before ranking with claude
    """
    sorter: str = DEFAULT_SORTING_ALGORITHM
    """
    - generate_explanations: Whether to generate explanations for links.
    """
    generate_explanations: bool = GENERATE_EXPLANATIONS_DEFAULT
    """
    - ranking_llm_model: The model used to rank
    """
    ranking_llm_model_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager)
    """
    - explanation_llm_model: The model used to create explanations
    """
    explanation_llm_model: AbstractLLMManager = field(default_factory=get_efficient_default_llm_manager)
    """
    - embedding_model: The model whose embeddings are used to rank children.
    """
    embedding_model_name: str = DEFAULT_EMBEDDING_MODEL
    """
    - parent_thresholds: The threshold used to establish parents from (primary, secondary and min)
    """
    parent_thresholds: Tuple[float, float, float] = (DEFAULT_PARENT_PRIMARY_THRESHOLD, DEFAULT_PARENT_MIN_THRESHOLD,
                                                     DEFAULT_PARENT_MIN_THRESHOLD)
    """
    - max_context_artifacts: The maximum number of artifacts to consider in a context window. 
    """
    max_context_artifacts = DEFAULT_MAX_CONTEXT_ARTIFACTS
    """
    - link_threshold: The threshold at which to accept links when selecting top predictions.
    """
    link_threshold: float = DEFAULT_LINK_THRESHOLD
    """
    - selection_method: The method to use to select top predictions
    """
    selection_method: SupportedSelectionMethod = SupportedSelectionMethod.SELECT_BY_THRESHOLD
    """
    - weight_of_explanation_scores: If greater than 0, will weight the scores from the explanation in the final score
    """
    weight_of_explanation_scores: float = DEFAULT_EXPLANATION_SCORE_WEIGHT
    """
     - weight_of_embedding_scores: If greater than 0, will weight the scores from the embeddings in the final score 
     *applicable only for LLMPipeline*
     """
    weight_of_embedding_scores: float = DEFAULT_EMBEDDINGS_SCORE_WEIGHT

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
        if self.export_dir is None:
            return None
        path = os.path.join(self.export_dir, file_name)
        path = os.path.expanduser(path)
        return path
