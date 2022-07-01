from typing import Dict, Any, Union

from transformers import Trainer

from data.trace_dataset import TraceDataset
from jobs.job_args import JobArgs
from models.model_generator import BaseModelGenerator
from results.base_results import BaseResults


class LMTrainer(Trainer):

    def __init__(self, args: JobArgs, model_generator: BaseModelGenerator, dataset: TraceDataset):
        self.args = args
        self.model_generator = model_generator
        self.dataset = dataset

    # TODO
    def train(self, checkpoint: str = None) -> BaseResults:
        data = self.dataset.get_training_data(self.args.resample_rate, self.args.max_seq_length)
        return BaseResults()

    def predict(self) -> BaseResults:
        data = self.dataset.get_validation_data(self.args.dataset_size, self.args.max_seq_length)
        return BaseResults()
