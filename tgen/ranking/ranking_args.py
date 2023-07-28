import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.tgen_constants import DEFAULT_LINKS_TAG, DEFAULT_MAX_N_CHILDREN, DEFAULT_PARENT_MIN_THRESHOLD, \
    DEFAULT_PARENT_THRESHOLD, \
    DEFAULT_QUERY_TAG, DEFAULT_RANKING_MODEL, DEFAULT_SORTING_ALGORITHM, GENERATE_SUMMARY_DEFAULT
from tgen.data.prompts.supported_prompts.default_ranking_prompts import DEFAULT_RANKING_GOAL, DEFAULT_RANKING_INSTRUCTIONS
from tgen.state.pipeline.pipeline_args import PipelineArgs


@dataclass
class RankingArgs(PipelineArgs):
    """
    Maps artifact ids to content.
    """
    artifact_map: Dict
    """
    List of parent artifact ids.
    """
    parent_ids: List[str]
    """
    Path to export various checkpoints
    """
    export_dir: str = None
    """
    Optional.List of children ids to compare to each parent.
    """
    children_ids: Optional[List[str]] = None
    """
    Maps parent ids to their children ids.
    """
    parent2children: Optional[Dict[str, List[str]]] = None
    """
    The number of maximum children to give to claude
    """
    max_children_per_query: int = DEFAULT_MAX_N_CHILDREN
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
    n_completion_tokens = 1000
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
    model: str = DEFAULT_RANKING_MODEL
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
    ranking_goal: str = DEFAULT_RANKING_GOAL
    """
    The detailed task instructions. The bottom portion. 
    """
    ranking_instructions: str = DEFAULT_RANKING_INSTRUCTIONS
    """
    The tag used to encapsulate the parent or query string.
    """
    query_tag: str = DEFAULT_QUERY_TAG
    """
    The tag used to contain the final ranked artifact ids.
    """
    links_tag: str = DEFAULT_LINKS_TAG

    def save(self, obj: Any, file_name: str) -> str:
        """
        Saves object if export path is set.
        :param obj: The object to save.
        :param file_name: The file name to save under.
        :return: Path of file.
        """
        if self.export_dir is not None:
            export_path = os.path.join(self.export_dir, file_name)
            FileUtil.write_yaml(obj, export_path)
            logger.info(f"Saved object to: {export_path}")
            return export_path
