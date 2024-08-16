from dataclasses import dataclass
from typing import Any, Dict, Type

from gen_common.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from gen_common.data.tdatasets.idataset import iDataset
from gen_common.tools.state_management.args import Args
from gen_common.tools.util.base_object import BaseObject
from gen_common.tools.util.dataclass_util import DataclassUtil
from gen_common.tools.util.dict_util import DictUtil
from gen_common.tools.util.file_util import FileUtil
from gen_common.tools.util.reflection_util import ReflectionUtil

from tgen.infra.constants.job_constants import SAVE_OUTPUT_DEFAULT


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

    def get_args_for_pipeline(self, pipeline_args_class: Type[Args]) -> Dict[str, Any]:
        """
        Gets job args that are needed for the pipeline.
        :param pipeline_args_class: The pipeline args class.
        :return: A dictionary mapping param name to value for all job args that are in the pipeline args.
        """
        job_args_dict = DataclassUtil.convert_to_dict(self)
        args4pipeline = ReflectionUtil.get_constructor_params(pipeline_args_class, job_args_dict)
        DictUtil.get_dict_values(args4pipeline, dataset_creator=None, pop=True)
        return args4pipeline
