from dataclasses import dataclass

from config.constants import SAVE_OUTPUT_DEFAULT
from models.model_properties import ModelArchitectureType, ModelTask
from train.trace_args import TraceArgs


@dataclass
class JobArgs:
    """
    Where model and logs will be saved to.
    """
    output_dir: str = None
    """
    Path to the model weights (e.g. loading pretrained model).
    """
    model_path: str = None
    """
    The model used to load the architecture.
    """
    model_architecture: ModelArchitectureType = None
    """
    Defines the task architecture.
    """
    model_task: ModelTask = None
    """
    Initialized post-init to contain all arguments for tracing jobs
    """
    trace_args: TraceArgs = None
    """
    If True, saves the output to the output_dir
    """
    save_job_output: bool = SAVE_OUTPUT_DEFAULT
    """
    Sets the random seed for a job
    """
    random_seed: int = None

    def as_kwargs(self):
        return {attr_name: getattr(self, attr_name) for attr_name in dir(self) if not attr_name.startswith("__")}
