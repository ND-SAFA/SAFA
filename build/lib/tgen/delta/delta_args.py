from dataclasses import dataclass, field
from typing import Dict, Union

from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.tools.constants.default_model_managers import get_best_default_llm_manager_long_context
from common_resources.tools.state_management.args import Args
from common_resources.tools.util.dataclass_util import required_field
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.json_util import JsonUtil

from tgen.delta.change_type import ChangeType


@dataclass
class DeltaArgs(Args):
    """
    :param diffs: A dictionary mapping type of change (e.g. Added, Deleted, etc.) to a dictionary of filename to diff
    """
    change_type_to_diffs: Union[str, Union[Dict[str, Dict], EnumDict[ChangeType, Dict]]] = required_field(
        field_name="change_type_to_diffs")
    """
    :param llm_manager: The LLM Manager to use for generations
    """
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
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
