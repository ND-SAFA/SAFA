from copy import deepcopy
from typing import Dict, List, NamedTuple, Tuple, Union

import numpy as np
from datasets import load_metric
from scipy.special import softmax
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler
from transformers.trainer import Trainer
from transformers.trainer_pt_utils import get_tpu_sampler, is_torch_tpu_available

from config.override import overrides
from data.datasets.dataset_role import DatasetRole
from train.metrics.supported_trace_metric import get_metric_name, get_metric_path
from models.model_generator import ModelGenerator
from train.trace_args import TraceArgs


class TraceTrainer(Trainer):
    """
    Responsible for using given model for training and prediction using given data.
    """

    def __init__(self, args: TraceArgs, model_generator: ModelGenerator, **kwargs):
        """
        Handles the training and evaluation of learning models
        :param args: the learning model arguments
        """
        self.args = args
        self.dataset_container = args.trainer_dataset_container
        self.model_generator = model_generator
        self.model_generator.set_max_seq_length(self.args.max_seq_length)
        model = self.model_generator.get_model()
        tokenizer = self.model_generator.get_tokenizer()
        super().__init__(model=model, args=args, tokenizer=tokenizer, callbacks=args.callbacks, **kwargs)

    def perform_training(self, checkpoint: str = None) -> Dict:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.train_dataset = self.dataset_container[DatasetRole.TRAIN].to_trainer_dataset(self.model_generator)
        if DatasetRole.VAL in self.dataset_container:
            self.eval_dataset = self.dataset_container[DatasetRole.VAL].to_trainer_dataset(self.model_generator)
        output = self.train(resume_from_checkpoint=checkpoint)
        return TraceTrainer.output_to_dict(output)

    def perform_prediction(self) -> Dict:
        """
        Performs the prediction and (optionally) evaluation for the model
        :return: A dictionary containing the results.
        """
        self.eval_dataset = self.dataset_container[DatasetRole.EVAL].to_trainer_dataset(self.model_generator)
        output = self.predict(self.eval_dataset)
        predictions = TraceTrainer.get_similarity_scores(output.predictions)
        results = self._eval(predictions, output.label_ids, output.metrics,
                             self.args.metrics) if self.args.metrics else None
        output_dict = TraceTrainer.output_to_dict(output, metrics=results, predictions=predictions,
                                                  source_target_pairs=self.dataset_container[
                                                      DatasetRole.EVAL].get_source_target_pairs())
        return output_dict

    @staticmethod
    def output_to_dict(output: NamedTuple, **kwargs) -> Dict:
        """
        Converts train/prediction output to a dictionary
        :param output: output from training or prediction
        :return: the output represented as a dictionary
        """
        base_output = {field: kwargs[field] if (field in kwargs and kwargs[field]) else getattr(output, field) for field
                       in
                       output._fields}
        additional_attrs = {field: kwargs[field] for field in kwargs.keys() if field not in base_output}
        return {**base_output, **additional_attrs}

    @staticmethod
    def _eval(preds: Union[np.ndarray, Tuple[np.ndarray]], label_ids: np.ndarray, output_metrics: Dict,
              metric_names: List) -> Dict:
        """
        Performs the evaluation of the model (use this instead of Trainer.evaluation to utilize predefined metrics from models)
        :param output: the output from predictions
        :param metric_names: name of metrics desired for evaluation
        :return: a dictionary of metric_name to result
        """
        metric_paths = [get_metric_path(name) for name in metric_names]
        results = deepcopy(output_metrics)
        for metric_path in metric_paths:
            metric = load_metric(metric_path, keep_in_memory=True)
            metric_result = metric.compute(predictions=preds, references=label_ids)
            metric_name = get_metric_name(metric)
            if isinstance(metric_result, dict) and metric_name in metric_result:
                results.update(metric_result)
            else:
                results[metric_name] = metric_result
        return results

    @staticmethod
    def get_similarity_scores(predictions: Union[np.ndarray, Tuple[np.ndarray]]) -> List[float]:
        """
        Transforms predictions into similarity scores.
        :param predictions: The model predictions.
        :return: List of similarity scores associated with predictions.
        """
        similarity_scores = []
        for pred_i in range(predictions.shape[0]):
            prediction = predictions[pred_i]
            similarity_scores.append(softmax(prediction)[1])
        return similarity_scores

    @overrides(Trainer)
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
