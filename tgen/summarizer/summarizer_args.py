import os
from dataclasses import dataclass, field

from typing import List, Dict

from tgen.common.constants.model_constants import get_best_default_llm_manager, get_efficient_default_llm_manager
from tgen.common.constants.project_summary_constants import DEFAULT_PROJECT_SUMMARY_SECTIONS, \
    DEFAULT_PROJECT_SUMMARY_SECTIONS_DISPLAY_ORDER
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.state.pipeline.pipeline_args import PipelineArgs
from tgen.summarizer.summary_types import SummaryTypes


@dataclass
class SummarizerArgs(PipelineArgs):
    """
    Dataset creator used to make dataset containing original artifacts
    """
    dataset: PromptDataset = None
    """
    LLM manager used for the individual artifact summaries
    """
    llm_manager_for_artifact_summaries: AbstractLLMManager = field(default_factory=get_efficient_default_llm_manager)
    """
    LLM manager used for the full project summary
    """
    llm_manager_for_project_summary: AbstractLLMManager = field(default_factory=get_best_default_llm_manager)
    """
    The type of summary to use for the code artifacts
    """
    code_summary_type: SummaryTypes = SummaryTypes.CODE_BASE
    """
    A manual project summary to use instead of creating one
    """
    project_summary: str = None
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
    section_order: List[str] = field(default_factory=lambda: DEFAULT_PROJECT_SUMMARY_SECTIONS_DISPLAY_ORDER)
    """
    If True, resummarizes the project with the new artifact summaries
    """
    do_resummarize_project: bool = True
    """
    Whether to summarize the artifacts before creating the project summary.
    """
    summarize_artifacts: bool = True
    """
    Path to save to
    """
    export_dir: str = None
    """
    If True, only summarizes the code
    """
    summarize_code_only: bool = True
    """
    The name of the directory to save the summaries to
    """
    summary_dirname = "summaries"

    def __post_init__(self) -> None:
        """
        Perform post initialization tasks such as creating datasets
        :return: None
        """
        if self.export_dir:
            if not self.export_dir.endswith(self.summary_dirname):
                self.export_dir = os.path.join(self.export_dir, self.summary_dirname)
        super().__post_init__()
