from dataclasses import dataclass

from config.constants import SAVE_OUTPUT_DEFAULT
from models.model_properties import ModelArchitectureType
from train.trainer_args import TrainerArgs


@dataclass
class JobArgs:
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

    def as_kwargs(self):
        return {attr_name: getattr(self, attr_name) for attr_name in dir(self) if not attr_name.startswith("__")}
