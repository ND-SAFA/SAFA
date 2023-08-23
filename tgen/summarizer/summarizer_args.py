import os
import uuid
from dataclasses import dataclass, field

from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.constants.model_constants import get_efficient_default_llm_manager, get_best_default_llm_manager
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.state.pipeline.pipeline_args import PipelineArgs
from tgen.summarizer.summary_types import SummaryTypes


@dataclass
class SummarizerArgs(PipelineArgs):
    """
    Dataset creator used to make dataset containing original artifacts
    """
    dataset_creator: PromptDatasetCreator = None
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
    If True, resummarizes the project with the new artifact summaries
    """
    do_resummarize_project: bool = True
    """
    Path to save to
    """
    export_dir: str = None

    def __post_init__(self) -> None:
        """
        Perform post initialization tasks such as creating datasets
        :return: None
        """
        self.export_dir = os.path.join(self.export_dir, "summaries", str(uuid.uuid4())) if self.export_dir else None
        self.dataset: PromptDataset = DataclassUtil.post_initialize_datasets(self.dataset, self.dataset_creator)
