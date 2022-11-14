from dataclasses import dataclass, field

from constants.constants import ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT, SAVE_OUTPUT_DEFAULT
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.train.trace_args import TraceArgs


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
    Initialized post-init to contain all arguments for tracing jobs
    """
    trace_args: TraceArgs = None
    """
    If True, adds mount directory to output path
    """
    add_mount_directory_to_output: bool = ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT
    """
    If True, saves the output to the output_dir
    """
    save_job_output: bool = SAVE_OUTPUT_DEFAULT
