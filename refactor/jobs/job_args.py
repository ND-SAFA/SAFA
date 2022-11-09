from dataclasses import dataclass
from typing import Dict, List, Tuple

from constants.constants import ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT, SAVE_OUTPUT_DEFAULT, \
    VALIDATION_PERCENTAGE_DEFAULT
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.dataset_role import DatasetRole
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.pre_processing.pre_processing_option import PreProcessingOption


@dataclass
class JobArgs:
    """
    Where model and logs will be saved to.
    """
    output_dir: str
    """
    Path to the model weights (e.g. loading pretrained model).
    """
    model_path: str
    """
    The model used to load the architecture.
    """
    base_model: SupportedBaseModel = None
    """
    Dictionary mapping dataset role (e.g. train/eval) to the desired dataset creator and its params
    """
    datasets_map: Dict[DatasetRole, Tuple[SupportedDatasetCreator, Dict]] = None
    """
    Dictionary mapping dataset role to the desired pre-processing steps and related params
    """
    dataset_pre_processing_options: Dict[DatasetRole, Tuple[List[PreProcessingOption], Dict]] = None
    """
    Additional parameters for the trace args
    """
    trace_args_params: Dict = None
    validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT
    """
    If True, splits the training dataset for eval
    """
    split_train_dataset: bool = False
    """
    If True, adds mount directory to output path
    """
    add_mount_directory_to_output: bool = ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT
    """
    If True, saves the output to the output_dir
    """
    save_job_output: bool = SAVE_OUTPUT_DEFAULT
