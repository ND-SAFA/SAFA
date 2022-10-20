import os
from abc import ABC
from typing import Dict

from config.constants import SAVE_OUTPUT_DEFAULT
from jobs.abstract_job import AbstractJob
from server.storage.safa_storage import SafaStorage
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.dataset_roles import DatasetRoles
from tracer.dataset.trace_dataset import TraceDataset
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.pre_processing.pre_processing_options import PreProcessingOptions
from tracer.pre_processing.pre_processor import PreProcessor
from tracer.train.trace_args import TraceArgs
from tracer.train.trace_trainer import TraceTrainer


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, model_path: str, base_model: SupportedBaseModel, output_dir: str,
                 datasets_map: Dict[str, (SupportedDatasetCreator, Dict)],
                 dataset_pre_processing_options: Dict[str, (PreProcessingOptions, Dict)] = None,
                 trace_args_params: Dict = None, save_output: bool = SAVE_OUTPUT_DEFAULT):
        """
        The base job class for tracing jobs
        :param base_model: supported base model name
        :param model_path: where the pretrained model will be loaded from
        :param output_dir: where the model will be saved to
        :param save_output: if True, saves the output to the output_dir
        :param trace_args_params: additional parameters for the trace args
        """
        model_path = SafaStorage.add_mount_directory(model_path)
        output_dir = os.path.join(output_dir, str(self.id))
        super().__init__(model_path, base_model, output_dir, save_output)
        dataset_pre_processing_options = dataset_pre_processing_options if dataset_pre_processing_options else {}
        self.train_dataset = self._make_dataset(datasets_map, dataset_pre_processing_options, DatasetRoles.TRAIN)
        self.eval_dataset = self._make_dataset(datasets_map, dataset_pre_processing_options, DatasetRoles.EVAL)
        self.trace_args = TraceArgs(**trace_args_params)
        self.__trainer = None

    @staticmethod
    def _make_dataset(datasets_map: Dict[str, (SupportedDatasetCreator, Dict)],
                      dataset_pre_processing_options: Dict[str, (PreProcessingOptions, Dict)],
                      dataset_role: DatasetRoles) -> TraceDataset:
        dataset_creator_reqs = datasets_map.get(dataset_role.value, None)
        if dataset_creator_reqs:
            pre_processor = AbstractTraceJob._make_pre_processor(dataset_pre_processing_options, dataset_role)
            dataset_creator_class, dataset_creator_params = dataset_creator_reqs
            dataset_creator = dataset_creator_class(pre_processor=pre_processor, **dataset_creator_params)
            return dataset_creator.create()

    @staticmethod
    def _make_pre_processor(dataset_pre_processing_options: Dict[str, (PreProcessingOptions, Dict)],
                            dataset_role: DatasetRoles) -> PreProcessor:
        pre_processing_reqs = dataset_pre_processing_options.get(dataset_role.value, None)
        if pre_processing_reqs:
            pre_processing_options, pre_processing_params = pre_processing_reqs
            return PreProcessor(pre_processing_options, **pre_processing_params)

    def get_trainer(self, **kwargs) -> TraceTrainer:
        if self.__trainer is None:
            self.__trainer = TraceTrainer(args=self.trace_args, model_generator=self.model_generator, **kwargs)
        return self.__trainer
