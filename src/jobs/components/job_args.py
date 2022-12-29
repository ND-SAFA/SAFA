from dataclasses import dataclass
from typing import Dict, Any

from config.constants import SAVE_OUTPUT_DEFAULT
from util.base_object import BaseObject


@dataclass
class JobArgs(BaseObject):
    """
    Where model and logs will be saved to.
    """
    output_dir: str = None
    """
    If True, saves the output to the output_dir
    """
    save_job_output: bool = SAVE_OUTPUT_DEFAULT
    """
    If True, saves the dataset splits to the output_dir
    """
    save_dataset_splits: bool = False
    """
    Sets the random seed for a job
    """
    random_seed: int = None

    def as_kwargs(self) -> Dict[str, Any]:
        """
        Gets the job args as kwargs
        :return: the job args as kwargs
        """
        return {attr_name: getattr(self, attr_name) for attr_name in dir(self) if not attr_name.startswith("__")}
