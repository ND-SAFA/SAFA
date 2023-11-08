from dataclasses import dataclass, field
from typing import Dict, Union

from tgen.common.util.dataclass_util import required_field, DataclassUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.json_util import JsonUtil
from tgen.common.constants.model_constants import get_best_default_llm_manager
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.delta.change_type import ChangeType
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.pipeline.pipeline_args import PipelineArgs


@dataclass
class DeltaArgs(PipelineArgs):
    """
    :param diffs: A dictionary mapping type of change (e.g. Added, Deleted, etc.) to a dictionary of filename to diff
    """
    change_type_to_diffs: Union[str, Union[Dict[str, Dict], EnumDict[ChangeType, Dict]]] = required_field(
        field_name="change_type_to_diffs")
    """
    :param llm_manager: The LLM Manager to use for generations
    """
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager)
    """
    :param export_path: Path to save checkpoints to
    """
    export_dir: str = None
    """
    :param load_dir: Path to load checkpoints from
    """
    load_dir: str = None

    def __post_init__(self) -> None:
        """
        Handles any standardization steps after initialization
        :return: None
        """
        super().__post_init__()
        self.dataset.artifact_df = self.dataset.artifact_df.drop_nan_indices()
        if isinstance(self.change_type_to_diffs, str):
            self.change_type_to_diffs = JsonUtil.read_json_file(self.change_type_to_diffs)
        self.change_type_to_diffs = EnumDict(self.change_type_to_diffs)

