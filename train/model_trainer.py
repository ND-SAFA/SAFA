from typing import Dict, List

import numpy as np
from datasets import load_metric
from torch.utils.data import DataLoader, RandomSampler
from torch.utils.data.distributed import DistributedSampler
from transformers.trainer import Trainer
from transformers.trainer_pt_utils import get_tpu_sampler, is_torch_tpu_available
from transformers.trainer_utils import PredictionOutput

from data.trace_dataset_creator import TraceDatasetCreator
from jobs.fine_tune.model_fine_tune_args import ModelFineTuneArgs
from models.model_generator import ModelGenerator
from train.metrics.supported_metrics import get_metric_path


class ModelTrainer(Trainer):
    """
    Responsible for using given model for training and prediction using given dataset.
    """

    def __init__(self, args: ModelFineTuneArgs, model_generator: ModelGenerator,
                 dataset_creator: TraceDatasetCreator):
        """
        Handles the training and evaluation of learning models
        :param args: the learning model arguments
        :param model_generator: the ModelGenerator
        :param dataset_creator: the TraceDatasetCreator
        """
        model = model_generator.get_model()
        tokenizer = model_generator.get_tokenizer()
        self.args = args
        self.model_generator = model_generator
        self.model_generator.set_max_seq_length(self.args.max_seq_length)
        self.dataset = dataset_creator
        super().__init__(model=model, args=args, tokenizer=tokenizer)

    # TODO
    def perform_training(self, checkpoint: str = None) -> Dict:
        """
        Performs the model training
        :param checkpoint: path to checkpoint
        :return: a dictionary containing the results
        """
        self.train_dataset = self.dataset.get_training_dataset(self.args.resample_rate)
        output = self.train(resume_from_checkpoint=checkpoint)
        self.save_model()
        return dict(output)

    # TODO
    def perform_prediction(self) -> Dict:
        """
        Performs the prediction and (optionally) evaluation for the model
        :return: a dictionary containing the results
        """
        self.eval_dataset = self.dataset.get_prediction_dataset(self.args.dataset_size)
        output = self.predict(self.eval_dataset)
        if self.args.metrics:
            output.metrics = self._eval(output, self.args.metrics)
        return dict(output)

    def _eval(self, output: PredictionOutput, metric_names: List) -> Dict:
        """
        Performs the evaluation of the model (use this instead of Trainer.evaluation to utilize predefined metrics from datasets)
        :param output: the output from predictions
        :param metric_names: name of metrics desired for evaluation
        :return: metric name, result mappings
        """
        metric_paths = [get_metric_path(name) for name in metric_names]
        metric = load_metric(*metric_paths)
        preds = np.argmax(output.predictions, axis=-1)
        return metric.compute(predictions=preds, references=output.predictions.label_ids)

    def get_train_dataloader(self) -> DataLoader:
        """
        Gets the dataloader for training
        :return: the DataLoader
        """
        if is_torch_tpu_available():
            train_sampler = get_tpu_sampler(self.train_dataset, self.args.train_batch_size)
        else:
            train_sampler = (
                RandomSampler(self.train_dataset)
                if self.args.local_rank == -1
                else DistributedSampler(self.train_dataset)
            )

        data_loader = DataLoader(
            self.train_dataset,
            batch_size=self.args.train_batch_size,
            sampler=train_sampler,
            collate_fn=self.data_collator,
            drop_last=self.args.dataloader_drop_last,
        )
        return data_loader
