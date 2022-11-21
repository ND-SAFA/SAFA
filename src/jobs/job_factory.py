import re
from dataclasses import dataclass, field
from typing import Callable, Dict, Type

from config.constants import SAVE_OUTPUT_DEFAULT, SAVE_DATASET_SPLITS_DEFAULT
from jobs.abstract_job import AbstractJob
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.job_args import JobArgs
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.train.trace_args import TraceArgs
from util.reflection_util import ReflectionUtil


@dataclass
class JobFactory:
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
    Container for datasets used for any training, prediction, or evaluation.
    """
    trainer_dataset_container: TrainerDatasetsContainer = None
    """
    Any additional parameters for making datasets including test/train split info
    """
    additional_dataset_params: Dict = field(default_factory=dict)
    """
    If True, saves the output to the output_dir
    """
    save_job_output: bool = SAVE_OUTPUT_DEFAULT
    """
    Additional parameters for the trace args
    """
    trace_args_params: Dict = field(default_factory=dict)
    """
    args used for TraceTrainer, initialized from traceArgsParams
    """
    trace_args: TraceArgs = field(init=False, default=None)
    """
    any additional args needed for the job
    """
    additional_job_params: Dict = field(init=False, default=None)
    """
    If True, saves the dataset splits to output_dir
    """
    save_dataset_splits: bool = SAVE_DATASET_SPLITS_DEFAULT

    def __init__(self, **kwargs):
        """
        Responsible for creating jobs
        :param kwargs: all necessary parameters
        """
        self.trace_args_params = {}  # TODO: Fix default factory using field
        self.set_args(**kwargs)

    def set_args(self, **kwargs) -> None:
        """
        Sets class args
        :param kwargs: optional arguments for Trainer
        :return: None
        """
        self.additional_job_params = {}
        for arg_name, arg_value in kwargs.items():
            snake_case_name = self._to_snake_case(arg_name)
            if hasattr(self, snake_case_name):
                setattr(self, snake_case_name, arg_value)
            else:
                self.additional_job_params[snake_case_name] = arg_value

    def build(self, job_class: Type[AbstractJob]) -> AbstractJob:
        """
        Creates job using job argument and any additional parameters.
        :param job_class: the class of job to build
        :return: Job
        """
        if ReflectionUtil.is_instance_or_subclass(job_class, AbstractTraceJob):
            self._create_trace_args()
        job_args = JobArgs(**self._get_job_args_params())
        return job_class(job_args, **self.additional_job_params)

    def _create_trace_args(self) -> None:
        """
        Creates the trace args from the given datasets and trace args params
        :return: None
        """
        if self.trainer_dataset_container is None:
            raise ValueError("TrainerDatasetCreator is not instantiated in JobFactory.")
        trace_args_params = self.trace_args_params if self.trace_args_params else {}
        self.trace_args = TraceArgs(trainer_dataset_container=self.trainer_dataset_container,
                                    output_dir=self.output_dir,
                                    **trace_args_params)

    def _get_job_args_params(self) -> Dict[str, any]:
        """
        Gets the params necessary for creating JobArgs
        :return: the params
        """
        params = {}
        for key, val in self.__dict__.items():
            if hasattr(JobArgs, key) and val is not None:
                params[key] = val
        return params

    @staticmethod
    def _to_snake_case(camel_case_str: str):
        """
        Converts the given camel case string to snake case
        :param camel_case_str: a string in camel case
        :return: the string as snake case
        """
        return "_".join([s.lower() for s in re.split("([A-Z][^A-Z]*)", camel_case_str) if s])


def assert_job_factory_attr_names():
    """
    Ensures the job factory has attributes with names matching those in job args
    :return: None
    """

    for attr_name, attr_value in vars(JobArgs).items():
        if not isinstance(attr_value, Callable) and not hasattr(JobFactory, attr_name):
            raise NameError("Expected attr named %s in JobFactory to match attr in job args" % attr_name)


assert_job_factory_attr_names()
