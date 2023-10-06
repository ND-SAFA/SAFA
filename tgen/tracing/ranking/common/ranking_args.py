import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from tgen.common.constants.model_constants import get_best_default_llm_manager, get_efficient_default_llm_manager
from tgen.common.constants.tracing.ranking_constants import DEFAULT_LINK_THRESHOLD, \
    DEFAULT_MAX_CONTEXT_ARTIFACTS, \
    DEFAULT_PARENT_MIN_THRESHOLD, \
    DEFAULT_PARENT_THRESHOLD, \
    DEFAULT_SORTING_ALGORITHM, GENERATE_SUMMARY_DEFAULT, DEFAULT_EMBEDDING_MODEL, DEFAULT_EXPLANATION_SCORE_WEIGHT
from tgen.common.util.dataclass_util import required_field
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.state.pipeline.pipeline_args import PipelineArgs
from tgen.tracing.ranking.common.selection_methods import SupportedSelectionMethod


@dataclass
class RankingArgs(PipelineArgs):
    """
    - dataset: The dataset containing all the project artifacts.
    """
    dataset: PromptDataset = required_field(field_name="dataset")
    """
    parent_ids: List of parent artifact ids.
    """
    parent_ids: List[str] = required_field(field_name="parent_ids")
    """
    children_ids: List of children ids to compare to each parent.
    """
    children_ids: Optional[List[str]] = required_field(field_name="children_ids")
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
    - generate_summary: Whether to generate a project summary.
    """
    generate_summary: bool = GENERATE_SUMMARY_DEFAULT
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
    - parent_primary_threshold: The threshold to establish primary parents from.
    """
    parent_primary_threshold = DEFAULT_PARENT_THRESHOLD
    """
    - parent_min_threshold: The minimum threshold to establish a parent if no primary.
    """
    parent_min_threshold = DEFAULT_PARENT_MIN_THRESHOLD
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
    selection_method: SupportedSelectionMethod = SupportedSelectionMethod.FILTER_BY_THRESHOLD
    """
    - weight_of_explanation_scores: If greater than 0, will weight the scores from the explanation in the final score
    """
    weight_of_explanation_scores: float = DEFAULT_EXPLANATION_SCORE_WEIGHT

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
