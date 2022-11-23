from dataclasses import dataclass

from config.constants import SAVE_OUTPUT_DEFAULT, SAVE_DATASET_SPLITS_DEFAULT
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.train.trace_args import TraceArgs


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
    base_model: SupportedBaseModel = None
    """
    Initialized post-init to contain all arguments for tracing jobs
    """
    trace_args: TraceArgs = None
    """
    If True, saves the output to the output_dir
    """
    save_job_output: bool = SAVE_OUTPUT_DEFAULT
    """
    If True, saves the dataset splits to output_dir
    """
    save_dataset_splits: bool = SAVE_DATASET_SPLITS_DEFAULT

    def as_kwargs(self):
        return {attr_name: getattr(self, attr_name) for attr_name in dir(self) if not attr_name.startswith("__")}
