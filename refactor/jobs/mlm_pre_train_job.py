import os
from typing import Dict, List

from transformers import DataCollatorForLanguageModeling

from jobs.abstract_trace_job import AbstractTraceJob
from server.storage.safa_storage import SafaStorage

from config.constants import ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT, SAVE_OUTPUT_DEFAULT, TRAINING_DATA_DIR_DEFAULT, BLOCK_SIZE_DEFAULT, \
    MLM_PROBABILITY_DEFAULT
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.dataset_role import DatasetRole
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.pre_processing.pre_processing_option import PreProcessingOption


class MLMPreTrainJob(AbstractTraceJob):

    def __init__(self, model_path: str, output_dir: str, orig_data_path: str,
                 training_data_dir: str = TRAINING_DATA_DIR_DEFAULT,
                 pre_processing_options: List[PreProcessingOption] = None,
                 pre_processing_params: Dict = None,
                 block_size: int = BLOCK_SIZE_DEFAULT,
                 trace_args_params: Dict = None,
                 mlm_probability: float = MLM_PROBABILITY_DEFAULT,
                 add_mount_directory_to_output: bool = ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT,
                 save_job_output: bool = SAVE_OUTPUT_DEFAULT):
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
        pre_processing_options = {DatasetRole.TRAIN: (pre_processing_options, pre_processing_params)}
        super().__init__(model_path=model_path, base_model=SupportedBaseModel.BERT_FOR_MASKED_LM, output_dir=output_dir,
                         datasets_map=datasets_map, dataset_pre_processing_options=pre_processing_options,
                         trace_args_params=trace_args_params, save_job_output=save_job_output,
                         split_train_dataset=False,
                         add_mount_directory_to_output=add_mount_directory_to_output)
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
