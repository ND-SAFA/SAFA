from dataclasses import dataclass

from typing import Any, Dict

from tgen.common.constants.job_constants import SAVE_OUTPUT_DEFAULT
from tgen.common.util.base_object import BaseObject
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.file_util import FileUtil
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.tdatasets.idataset import iDataset


@dataclass
class JobArgs(BaseObject):
    """
    Where model and logs will be saved to.
    """
    output_dir: str = None
    """
    Where model and logs will be saved to.
    """
    export_dir: str = None
    """
    If True, saves the output to the output_dir
    """
    save_job_output: bool = SAVE_OUTPUT_DEFAULT
    """
    Sets the random seed for a job
    """
    random_seed: int = None
    """
    Suffix to run name in weights and biases.
    """
    run_suffix: str = None
    """
    Creator to make a dataset for the job.
    """
    dataset_creator: AbstractDatasetCreator = None
    """
    Dataset for the job.
    """
    dataset: iDataset = None

    def __post_init__(self) -> None:
        """
        Performs any steps after initialize.
        :return: None
        """
        FileUtil.create_dir_safely(self.export_dir)

    def require_data(self) -> None:
        """
        Ensures data has been provided in either the form of a dataset or a dataset creator.
        :return: None
        """
        self.dataset = DataclassUtil.post_initialize_datasets(self.dataset, self.dataset_creator)

    def as_kwargs(self) -> Dict[str, Any]:
        """
        Gets the job args as kwargs
        :return: the job args as kwargs
        """
        return {attr_name: getattr(self, attr_name) for attr_name in dir(self) if not attr_name.startswith("__")}
