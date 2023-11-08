from dataclasses import dataclass

from typing import List

from tgen.common.constants import environment_constants
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.base_object import BaseObject
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.param_specs import ParamSpecs
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.pipeline.state import State


@dataclass
class PipelineArgs(BaseObject):
    """
    :param dataset: The dataset used in the pipeline
    """
    dataset: PromptDataset = None
    """
    :param dataset_creator: Used to create the dataset if None is provided
    """
    dataset_creator: PromptDatasetCreator = None
    """
    :param export_dir: The directory to export to
    """
    export_dir: str = EMPTY_STRING
    """
    :param load_dir: The directory to load from
    """
    load_dir: str = EMPTY_STRING
    """
    :param interactive_mode: If True, enters interactive mode
    """
    interactive_mode: bool = False

    def __post_init__(self):
        """
        Updates the load dir to match export dir if none is provided
        :return: None
        """
        self.dataset: PromptDataset = DataclassUtil.post_initialize_datasets(self.dataset,
                                                                             self.dataset_creator)
        self.interactive_mode = self.interactive_mode or environment_constants.IS_INTERACTIVE

    def update_llm_managers_with_state(self, state: State) -> None:
        """
        Updates all the llm_managers to use the pipeline's state to save token counts
        :param state: The pipeline state
        :return: None
        """
        DataclassUtil.update_attr_of_type_with_vals(self, AbstractLLMManager, state=state)
