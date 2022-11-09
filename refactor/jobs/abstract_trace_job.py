from abc import ABC
from typing import Dict, List, Optional, Tuple

from jobs.abstract_job import AbstractJob
from jobs.job_args import JobArgs
from server.storage.safa_storage import SafaStorage
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.dataset_map import DatasetMap
from tracer.dataset.dataset_role import DatasetRole
from tracer.dataset.trace_dataset import TraceDataset
from tracer.pre_processing.pre_processing_option import PreProcessingOption
from tracer.train.trace_args import TraceArgs
from tracer.train.trace_trainer import TraceTrainer


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, job_args: JobArgs):
        """
        The base job class for tracing jobs
        """
        job_args.model_path = SafaStorage.add_mount_directory(job_args.model_path)
        super().__init__(job_args)
        dataset_pre_processing_options = job_args.dataset_pre_processing_options if job_args.dataset_pre_processing_options else {}
        self.train_dataset = self._make_dataset(job_args.datasets_map, dataset_pre_processing_options,
                                                DatasetRole.TRAIN)
        self.eval_dataset = self._make_dataset(job_args.datasets_map, dataset_pre_processing_options, DatasetRole.EVAL)
        if self.train_dataset and job_args.split_train_dataset:
            self.train_dataset, self.eval_dataset = self.train_dataset.split(job_args.validation_percentage)
        self.train_args = TraceArgs(job_args.output_dir,
                                    **(job_args.trace_args_params if job_args.trace_args_params else {}))
        self._trainer = None
        self.dataset_map = self._make_datasets(job_args.datasets_map, dataset_pre_processing_options)

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
            dataset_creator = dataset_creator_class.value(pre_processing_params=pre_processing_params,
                                                          **dataset_creator_params)
            return dataset_creator.create()

    @staticmethod
    def _make_datasets(datasets_map: Dict[DatasetRole, Tuple[SupportedDatasetCreator, Dict]],
                       dataset_pre_processing_options: Dict[DatasetRole, Tuple[List[PreProcessingOption], Dict]]
                       ):
        role2dataset: DatasetMap = DatasetMap()
        for dataset_role, dataset_creator_reqs in datasets_map.items():
            dataset_creator_class, dataset_creator_params = dataset_creator_reqs
            pre_processing_params = dataset_pre_processing_options.get(dataset_role)
            dataset_creator = dataset_creator_class.value(pre_processing_params=pre_processing_params,
                                                          **dataset_creator_params)
            role2dataset[dataset_role] = dataset_creator.create()
        return role2dataset

    def get_trainer(self, **kwargs) -> TraceTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = TraceTrainer(args=self.train_args, model_generator=self.get_model_generator(),
                                         **kwargs)
        return self._trainer
