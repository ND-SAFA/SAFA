from dataclasses import dataclass

from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.llm.abstract_llm_manager import AbstractLLMManager
from gen_common.infra.base_object import BaseObject
from gen_common.util.dataclass_util import DataclassUtil


@dataclass
class Args(BaseObject):
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

    def __post_init__(self):
        """
        Updates the load dir to match export dir if none is provided
        :return: None
        """
        self.dataset: PromptDataset = DataclassUtil.post_initialize_datasets(self.dataset,
                                                                             self.dataset_creator)

    def update_llm_managers_with_state(self, state: "State") -> None:
        """
        Updates all the llm_managers to use the pipeline's state to save token counts
        :param state: The pipeline state
        :return: None
        """

        DataclassUtil.update_attr_of_type_with_vals(self, AbstractLLMManager, state=state)
