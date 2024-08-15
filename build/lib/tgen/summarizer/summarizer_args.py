from dataclasses import dataclass, field
from typing import Dict, List

from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.llm.prompts.questionnaire_prompt import QuestionnairePrompt
from common_resources.tools.constants.default_model_managers import get_best_default_llm_manager_long_context, \
    get_efficient_default_llm_manager
from common_resources.tools.state_management.args import Args
from common_resources.tools.state_management.state import State
from common_resources.tools.util.dataclass_util import DataclassUtil
from common_resources.tools.util.file_util import FileUtil

from tgen.common.constants.project_summary_constants import DEFAULT_PROJECT_SUMMARY_SECTIONS, \
    DEFAULT_PROJECT_SUMMARY_SECTIONS_DISPLAY_ORDER
from tgen.summarizer.artifact.artifact_summary_types import ArtifactSummaryTypes


@dataclass
class SummarizerArgs(Args):
    """
    LLM manager used for the individual artifact summaries
    """
    llm_manager_for_artifact_summaries: AbstractLLMManager = field(default_factory=get_efficient_default_llm_manager)
    """
    LLM manager used for the full project summary
    """
    llm_manager_for_project_summary: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    """
    The type of summary to use for the code artifacts
    """
    code_summary_type: ArtifactSummaryTypes = ArtifactSummaryTypes.CODE_BASE
    """
    The titles of the sections that make up the project summary 
    """
    project_summary_sections: List[str] = field(default_factory=lambda: DEFAULT_PROJECT_SUMMARY_SECTIONS)
    """
    Mapping of title to prompt for any non-standard sections to include in the summary
    """
    new_sections: Dict[str, QuestionnairePrompt] = field(default_factory=dict)
    """
    The list of the section titles in the order they should appear in the project summary
    """
    section_display_order: List[str] = field(default_factory=lambda: DEFAULT_PROJECT_SUMMARY_SECTIONS_DISPLAY_ORDER)
    """
    Whether to summarize the artifacts after creating the project summary.
    """
    do_resummarize_artifacts: bool = False
    """
    If True, a project summary will not be created
    """
    no_project_summary: bool = False
    """
    If True, only summarizes the code
    """
    summarize_code_only: bool = True
    """
    The name of the directory to save the summaries to
    """
    summary_dirname = "summarized"
    """
    List of file types to include when summarizing
    """
    include_subset_by_type: List[str] = field(default_factory=list)
    """
    List of directories to include when summarizing
    """
    include_subset_by_dir: List[str] = field(default_factory=list)
    """
    Includes context (dependent methods) when summarizing code.
    """
    use_context_in_code_summaries: bool = True

    def __post_init__(self) -> None:
        """
        Perform post initialization tasks such as creating datasets
        :return: None
        """
        if self.export_dir:
            self.update_export_dir(self.export_dir)

    def update_export_dir(self, new_path: str) -> None:
        """
        Updates the export dir to the new path value
        :param new_path: The new path to update the export dir to
        :return: None
        """
        self.export_dir = new_path
        if self.export_dir and not self.export_dir.endswith(self.summary_dirname):
            self.export_dir = FileUtil.safely_join_paths(self.export_dir, self.summary_dirname)

    def update_llm_managers_with_state(self, state: State) -> None:
        """
        Updates all the llm_managers to use the pipeline's state to save token counts
        :param state: The pipeline state
        :return: None
        """
        DataclassUtil.update_attr_of_type_with_vals(self, AbstractLLMManager, state=state)
