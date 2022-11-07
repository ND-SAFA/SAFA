import os
from typing import Dict, List

from transformers import DataCollatorForLanguageModeling

from config.constants import BLOCK_SIZE_DEFAULT, MLM_PROBABILITY_DEFAULT, TRAINING_DATA_DIR_DEFAULT
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.job_args import JobArgs
from server.storage.safa_storage import SafaStorage
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.dataset_role import DatasetRole
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.pre_processing.pre_processing_option import PreProcessingOption


class MLMPreTrainJob(AbstractTraceJob):

    def __init__(self,
                 job_args: JobArgs,
                 orig_data_path: str,
                 training_data_dir: str = TRAINING_DATA_DIR_DEFAULT,
                 pre_processing_options: List[PreProcessingOption] = None,
                 pre_processing_params: Dict = None,
                 block_size: int = BLOCK_SIZE_DEFAULT,
                 mlm_probability: float = MLM_PROBABILITY_DEFAULT):
        """
        The base job class for tracing jobs
        :param model_path: where the pretrained model will be loaded from
        :param output_dir: where the model will be saved to
        :param orig_data_path: path to the original pretraining
        :param training_data_dir: path to the directory to save the training dataset file
        :param mlm_probability: the probability for the masking a word in the learning model
        :param add_mount_directory_to_output: if True, adds mount directory to output path
        :param save_job_output: if True, saves the output to the output_dir
        """
        mounted_training_dir = SafaStorage.add_mount_directory(training_data_dir)
        datasets_map = {DatasetRole.TRAIN: (SupportedDatasetCreator.MLM_PRETRAIN, {"orig_data_path": orig_data_path,
                                                                                   "training_data_dir": mounted_training_dir,
                                                                                   "block_size": block_size})}
        if pre_processing_options and pre_processing_params:
            pre_processing_options = {DatasetRole.PRE_TRAIN: (pre_processing_options, pre_processing_params)}
            job_args.dataset_pre_processing_options = pre_processing_options
        job_args.split_train_dataset = False
        job_args.base_model = SupportedBaseModel.BERT_FOR_MASKED_LM
        job_args.datasets_map = datasets_map
        super().__init__(job_args)
        self.mlm_probability = mlm_probability

    def _run(self):
        tokenizer = self.get_model_generator().get_tokenizer()
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer, mlm=True, mlm_probability=self.mlm_probability
        )
        tokenizer.save_vocabulary(self.output_dir)
        trainer = self.get_trainer(data_collator=data_collator)
        result = trainer.perform_training(self.train_dataset)
        trainer.save_model(trainer.args.output_dir)

        os.remove(self.train_dataset.training_file_path)
        return result
