import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.tgen_constants import DEFAULT_PARENT_MIN_THRESHOLD, \
    DEFAULT_PARENT_THRESHOLD, \
    DEFAULT_RANKING_MODEL, DEFAULT_SORTING_ALGORITHM, GENERATE_SUMMARY_DEFAULT
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.prompts.supported_prompts.default_search_prompts import DEFAULT_SEARCH_GOAL, DEFAULT_SEARCH_INSTRUCTIONS, \
    DEFAULT_SEARCH_LINK_TAG, DEFAULT_SEARCH_QUERY_TAG, RANKING_INSTRUCTIONS
from tgen.ranking.common.vsm_sorter import DEFAULT_EMBEDDING_MODEL
from tgen.state.pipeline.pipeline_args import PipelineArgs


@dataclass
class RankingArgs(PipelineArgs):
    """
    The data-frame containing all the project aritfacts.
    """
    artifact_df: ArtifactDataFrame
    """
    List of parent artifact ids.
    """
    parent_ids: List[str]
    """
    Optional.List of children ids to compare to each parent.
    """
    children_ids: Optional[List[str]]
    """
    Path to export various checkpoints
    """
    export_dir: str = "~/desktop/safa/output/hgen/roboflow/explanations"
    """
    Maps artifact ids to content.
    """
    artifact_map: Dict = None
    """
    Maps parent ids to their children ids.
    """
    parent2children: Optional[Dict[str, List[str]]] = None
    """
    The number of maximum children to give to claude
    """
    max_children_per_query: int = None
    """
    The sorting algorithm to use before ranking with claude
    """
    sorter: str = DEFAULT_SORTING_ALGORITHM
    """
    Whether to load previous responses.
    """
    load_response: bool = False
    """
    The maximum number of tokens to use for summarizing project
    """
    n_summary_tokens = 5000
    """
    The maximum number of tokens per source artifacts.
    """
    n_completion_tokens = 20000
    """
    Whether to generate a project summary.
    """
    generate_summary: bool = GENERATE_SUMMARY_DEFAULT
    """
    A pre-existing project summary to use.
    """
    project_summary: str = None
    """
    The model used to rank
    """
    ranking_llm_model: str = DEFAULT_RANKING_MODEL
    """
    The model whose embeddings are used to rank children.
    """
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    """
    The threshold to establish primary parents from.
    """
    parent_primary_threshold = DEFAULT_PARENT_THRESHOLD
    """
    The minimum threshold to establish a parent if no primary.
    """
    parent_min_threshold = DEFAULT_PARENT_MIN_THRESHOLD
    """
    The goal of the ranking prompt. The top portion.
    """
    ranking_goal: str = DEFAULT_SEARCH_GOAL
    """
    The detailed task instructions. The bottom portion. 
    """
    ranking_instructions: str = RANKING_INSTRUCTIONS
    """
    The list of questions to answer for the ranking task.
    """
    ranking_questions: List[Tuple] = None
    """
    The tag used to encapsulate the parent or query string.
    """
    query_tag: str = DEFAULT_SEARCH_QUERY_TAG
    """
    The tag used to contain the final ranked artifact ids.
    """
    links_tag: str = DEFAULT_SEARCH_LINK_TAG

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
            self.ranking_questions = DEFAULT_SEARCH_INSTRUCTIONS
