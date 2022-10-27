from abc import ABC
from typing import Dict, Optional, Tuple, List

from config.constants import SAVE_OUTPUT_DEFAULT, ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT, VALIDATION_PERCENTAGE_DEFAULT
from jobs.abstract_job import AbstractJob
from server.storage.safa_storage import SafaStorage
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.dataset_role import DatasetRole
from tracer.dataset.trace_dataset import TraceDataset
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.pre_processing.pre_processing_option import PreProcessingOption
from tracer.pre_processing.pre_processor import PreProcessor
from tracer.train.trace_args import TraceArgs
from tracer.train.trace_trainer import TraceTrainer


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, output_dir: str, model_path: str, base_model: SupportedBaseModel,
                 datasets_map: Dict[DatasetRole, Tuple[SupportedDatasetCreator, Dict]],
                 dataset_pre_processing_options: Dict[DatasetRole, Tuple[List[PreProcessingOption], Dict]] = None,
                 trace_args_params: Dict = None,
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT,
                 add_mount_directory_to_output: bool = ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT,
                 save_job_output: bool = SAVE_OUTPUT_DEFAULT):
        """
        The base job class for tracing jobs
       :param base_model: supported base model name
        :param model_path: where the pretrained model will be loaded from
        :param output_dir: where the model will be saved to
        :param datasets_map: dictionary mapping dataset role (e.g. train/eval) to the desired dataset creator and its params
        :param dataset_pre_processing_options: dictionary mapping dataset role to the desired pre-processing steps and related params
        :param trace_args_params: additional parameters for the trace args
        :param add_mount_directory_to_output: if True, adds mount directory to output path
        :param save_job_output: if True, saves the output to the output_dir
        """
        model_path = SafaStorage.add_mount_directory(model_path)
        super().__init__(output_dir, model_path, base_model, add_mount_directory_to_output, save_job_output)
        dataset_pre_processing_options = dataset_pre_processing_options if dataset_pre_processing_options else {}
        self.train_dataset = self._make_dataset(datasets_map, dataset_pre_processing_options, DatasetRole.TRAIN)
        self.eval_dataset = self._make_dataset(datasets_map, dataset_pre_processing_options, DatasetRole.EVAL)
        if self.train_dataset and not self.eval_dataset:
            self.train_dataset, self.eval_dataset = self.train_dataset.split(validation_percentage)
        self.train_args = TraceArgs(output_dir, **(trace_args_params if trace_args_params else {}))
        self.__trainer = None

    @staticmethod
    def _make_dataset(datasets_map: Dict[DatasetRole, Tuple[SupportedDatasetCreator, Dict]],
                      dataset_pre_processing_options: Dict[DatasetRole, Tuple[List[PreProcessingOption], Dict]],
                      dataset_role: DatasetRole) -> Optional[TraceDataset]:
        """
        Handles making the dataset for a specified role and the given parameters
        :param datasets_map: dictionary mapping dataset role (e.g. train/eval) to the desired dataset creator and its params
        :param dataset_pre_processing_options: dictionary mapping dataset role to the desired pre-processing steps and related params
        :param dataset_role: the role of the dataset (e.g. trail/eval)
        :return: the dataset
        """
        dataset_creator_reqs = datasets_map.get(dataset_role, None)
        if dataset_creator_reqs:
            dataset_creator_class, dataset_creator_params = dataset_creator_reqs
            pre_processing_params = dataset_pre_processing_options.get(dataset_role)
            dataset_creator = dataset_creator_class.value(pre_processing_params=pre_processing_params, **dataset_creator_params)
            return dataset_creator.create()

    def get_trainer(self, **kwargs) -> TraceTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self.__trainer is None:
            self.__trainer = TraceTrainer(args=self.train_args, model_generator=self.get_model_generator(), **kwargs)
        return self.__trainer
