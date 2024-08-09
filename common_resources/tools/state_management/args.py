from dataclasses import dataclass

from common_resources.data.creators.prompt_dataset_creator import PromptDatasetCreator
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.constants.symbol_constants import EMPTY_STRING
from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.dataclass_util import DataclassUtil


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