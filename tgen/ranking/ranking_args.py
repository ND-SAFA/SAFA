import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from tgen.common.util.dataclass_util import required_field
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.model_constants import get_best_default_llm_manager
from tgen.constants.ranking_constants import DEFAULT_ARTIFACT_HEADER, DEFAULT_COMPLETION_TOKENS, DEFAULT_MAX_CONTEXT_ARTIFACTS, \
    DEFAULT_PARENT_MIN_THRESHOLD, \
    DEFAULT_PARENT_THRESHOLD, \
    DEFAULT_RANKING_MODEL, DEFAULT_SORTING_ALGORITHM, DEFAULT_SUMMARY_TOKENS, GENERATE_SUMMARY_DEFAULT, RANKING_PARENT_TAG
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.prompts.supported_prompts.default_ranking_prompts import DEFAULT_RANKING_GOAL, DEFAULT_RANKING_INSTRUCTIONS, \
    DEFAULT_RANKING_QUESTIONS
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.ranking.common.vsm_sorter import DEFAULT_EMBEDDING_MODEL
from tgen.state.pipeline.pipeline_args import PipelineArgs


@dataclass
class RankingArgs(PipelineArgs):
    """
    artifact_df: The data-frame containing all the project aritfacts.
    parent_ids: List of parent artifact ids.
    children_ids: List of children ids to compare to each parent.
    """
    artifact_df: ArtifactDataFrame = required_field(field_name="artifact_df")
    parent_ids: List[str] = required_field(field_name="parent_ids")
    children_ids: Optional[List[str]] = required_field(field_name="children_ids")
    """
    - run_name: The unique identifier of this run.
    - export_dir: Path to export various checkpoints
    - artifact_map: Maps artifact ids to content.
    - project_summary: A pre-existing project summary to use.
    - parent2children: Maps parent ids to their children ids.
    - max_children_per_query: The number of maximum children to give to claude
    - sorter: The sorting algorithm to use before ranking with claude
    - n_summary_tokens: The maximum number of tokens to use for summarizing project
    - n_completion_tokens: The maximum number of tokens per source artifacts.
    - generate_summary: Whether to generate a project summary.
    - ranking_llm_model: The model used to rank
    - embedding_model: The model whose embeddings are used to rank children.
    - parent_primary_threshold: The threshold to establish primary parents from.
    - parent_min_threshold: The minimum threshold to establish a parent if no primary.
    - ranking_goal: The goal of the ranking prompt. The top portion.
    - ranking_instructions: The detailed task instructions. The bottom portion. 
    - ranking_questions: The list of questions to answer for the ranking task.
    - query_tag: The tag used to encapsulate the parent or query string.
    - artifact_header: The header to put above all the software artifacts.
    - max_context_artifacts: The maximum number of artifacts to consider in a context window. 
    - llm_manager: A custom llm manager to use throughout the pipeline.
    """
    run_name: str = "default_run"
    export_dir: str = None
    artifact_map: Dict = None
    project_summary: str = None
    parent2children: Optional[Dict[str, List[str]]] = None
    max_children_per_query: int = None
    sorter: str = DEFAULT_SORTING_ALGORITHM
    n_summary_tokens = DEFAULT_SUMMARY_TOKENS
    n_completion_tokens = DEFAULT_COMPLETION_TOKENS
    generate_summary: bool = GENERATE_SUMMARY_DEFAULT
    ranking_llm_model: str = DEFAULT_RANKING_MODEL
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    parent_primary_threshold = DEFAULT_PARENT_THRESHOLD
    parent_min_threshold = DEFAULT_PARENT_MIN_THRESHOLD
    ranking_goal: str = DEFAULT_RANKING_GOAL
    ranking_instructions: str = DEFAULT_RANKING_INSTRUCTIONS
    ranking_questions: List[Tuple] = None
    query_tag: str = RANKING_PARENT_TAG
    artifact_header: str = DEFAULT_ARTIFACT_HEADER
    max_context_artifacts = DEFAULT_MAX_CONTEXT_ARTIFACTS
    llm_manager: AbstractLLMManager = None

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

    def __post_init__(self) -> None:
        """
        Creates the necessary data structures for operation.
        :return: None
        """
        self.artifact_map = self.artifact_df.to_map()
        if self.ranking_questions is None:
            self.ranking_questions = DEFAULT_RANKING_QUESTIONS
        if self.llm_manager is None:
            self.llm_manager = get_best_default_llm_manager()
