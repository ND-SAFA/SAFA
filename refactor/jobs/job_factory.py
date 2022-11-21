import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Type, Callable

from config.constants import SAVE_OUTPUT_DEFAULT
from jobs.abstract_job import AbstractJob
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.job_args import JobArgs
from tracer.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.datasets.dataset_role import DatasetRole
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.pre_processing.pre_processing_option import PreProcessingOption
from tracer.train.trace_args import TraceArgs


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
    Dictionary mapping datasets role (e.g. train/eval) to the desired datasets creator and its params
    """
    datasets_map: Dict[DatasetRole, Tuple[SupportedDatasetCreator, Dict]] = field(default_factory=dict)
    """
    Dictionary mapping datasets role to the desired pre-processing steps and related params
    """
    dataset_pre_processing_options: Dict[DatasetRole, Tuple[List[PreProcessingOption], Dict]] = field(
        default_factory=dict)
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

    def __init__(self, **kwargs):
        """
        Responsible for creating jobs
        :param kwargs: all necessary parameters
        """
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
        if isinstance(job_class, AbstractTraceJob):
            self._create_trace_args()
        job_args = JobArgs(**self._get_job_args_params())
        return job_class(job_args, **self.additional_job_params)

    def _create_trace_args(self) -> None:
        """
        Creates the trace args from the given datasets and trace args params
        :return: None
        """
        trainer_dataset_creator = TrainerDatasetsContainer(datasets_map=self.datasets_map,
                                                           dataset_pre_processing_options=self.dataset_pre_processing_options,
                                                           **self.additional_dataset_params)
        self.trace_args = TraceArgs(trainer_dataset_creator=trainer_dataset_creator, **self.trace_args_params)

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


def print_fields(p_class):
    print(list(filter(lambda f: f[0] != '_', p_class.__dict__.keys())))


def assert_job_factory_attr_names():
    """
    Ensures the job factory has attributes with names matching those in job args
    :return: None
    """
    print_fields(JobFactory)
    print_fields(JobArgs)

    for attr_name, attr_value in vars(JobArgs).items():
        if not isinstance(attr_value, Callable) and not hasattr(JobFactory, attr_name):
            raise NameError("Expected attr named %s in JobFactory to match attr in job args" % attr_name)


assert_job_factory_attr_names()
