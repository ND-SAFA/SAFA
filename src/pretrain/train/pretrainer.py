import multiprocessing
import os
from typing import Dict

from transformers.convert_tf_hub_seq_to_seq_bert_to_pytorch import convert_tf_checkpoint_to_pytorch

from common.api.prediction_response import PredictionResponse
from pretrain.electra.build_pretraining_dataset import write_examples
from pretrain.electra.run_pretraining import train_or_eval
from pretrain.jobs.pretrain_args import PretrainArgs


class PreTrainer:
    """
    Responsible for performing pre-training on model.
    """

    def __init__(self, config: PretrainArgs):
        """
        Handles pretraining
        :param config: configuration for pretraining
        """
        self.config = config

    # TODO - improve
    def save_vocab(self) -> str:
        """
        Saves the vocab file for the pretraining
        :return: the path to the created vocab file
        """
        tokenizer = self.config.model_generator.get_tokenizer()
        tokenizer.save_pretrained(self.config.output_dir)
        return os.path.join(self.config.output_dir, "vocab.txt")

    def build_pretraining_data(self) -> None:
        """
        Builds the pretraining dataset
        :return: None
        """
        if self.config.num_processes == 1:
            write_examples(0, self.config)
        else:
            jobs = []
            for i in range(self.config.num_processes):
                job = multiprocessing.Process(target=write_examples, args=(i, self.config))
                jobs.append(job)
                job.start()
            for job in jobs:
                job.join()

    def train(self) -> None:
        """
        Performs the pretraining
        :return: None
        """
        self.config.set_do_train(True)
        train_or_eval(self.config)
        self.tf_checkpoint_to_pytorch()

    def tf_checkpoint_to_pytorch(self) -> None:
        """
        Converts a tensor flow checkpoint to pytorch checkpoint
        :return: None
        """
        electra_config_file = os.path.join(self.config.model_dir, "config.json")
        pytorch_dump_path = os.path.join(self.config.model_dir, "pytorch_model.bin")
        convert_tf_checkpoint_to_pytorch(self.config.model_dir, electra_config_file, pytorch_dump_path, "discriminator")

    # TODO - currently unused. Should this be a new job or part of the pretrain job?
    def eval(self) -> Dict:
        """
        Performs the evaluation of pretraining
        :return: the results of the evaluation
        """
        output = {}
        self.config.set_do_train(False)
        output[PredictionResponse.METRICS] = train_or_eval(self.config)
        return output
