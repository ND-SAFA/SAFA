from datasets import load_metric
from scipy.special import softmax
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler
from transformers.trainer import Trainer
from transformers.trainer_pt_utils import get_tpu_sampler, is_torch_tpu_available

from typing import Dict, List, NamedTuple, Tuple, Union

import numpy as np
from api.responses.prediction_response import PredictionResponse
from tracer.models.model_generator import ModelGenerator
from tracer.train.trace_args import TraceArgs
from tracer.dataset.trace_dataset import TraceDataset
from tracer.metrics.supported_trace_metric import get_metric_path, get_metric_name


class TraceTrainer(Trainer):
    """
    Responsible for using given model for training and prediction using given dataset.
    """

    def __init__(self, args: TraceArgs, model_generator: ModelGenerator, **kwargs):
        """
        Handles the training and evaluation of learning models
        :param args: the learning model arguments
        """
        self.args = args
        self.model_generator = model_generator
        self.model_generator.set_max_seq_length(self.args.max_seq_length)
        self.trace_dataset_creator = args.trace_dataset_creator
        model = self.model_generator.get_model()
        tokenizer = self.model_generator.get_tokenizer()
        super().__init__(model=model, args=args, tokenizer=tokenizer, callbacks=args.callbacks, **kwargs)

    def perform_training(self, train_dataset: TraceDataset, eval_dataset: TraceDataset, checkpoint: str = None) -> Dict:
        """
        Performs the model training.
        :param train_dataset: The dataset used to adjust model weights.
        :param eval_dataset: The dataset used to determine the best model (TODO).
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.train_dataset = train_dataset.to_trainer_dataset(self.model_generator)
        self.eval_dataset = eval_dataset.to_trainer_dataset(self.model_generator)
        output = self.train(resume_from_checkpoint=checkpoint)
        return TraceTrainer.output_to_dict(output)

    def perform_prediction(self, eval_dataset: TraceDataset) -> Dict:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param eval_dataset: The dataset being predicted and/or evaluated.
        :return: A dictionary containing the results.
        """
        self.eval_dataset = eval_dataset.to_trainer_dataset(self.model_generator)
        output = self.predict(self.eval_dataset)
        output.predictions = TraceTrainer.get_similarity_scores(output.predictions)
        if self.args.metrics:
            results = self._eval(output.predictions, output.label_ids, self.args.metrics)
            output.metrics.update(results)
        output_dict = TraceTrainer.output_to_dict(output)
        return PredictionResponse.from_output(output_dict, eval_dataset.get_source_target_pairs())

    @staticmethod
    def output_to_dict(output: NamedTuple) -> Dict:
        """
        Converts train/prediction output to a dictionary
        :param output: output from training or prediction
        :return: the output represented as a dictionary
        """
        return {field: getattr(output, field) for field in output._fields}

    @staticmethod
    def _eval(preds: Union[np.ndarray, Tuple[np.ndarray]], label_ids: np.ndarray, metric_names: List) -> Dict:
        """
        Performs the evaluation of the model (use this instead of Trainer.evaluation to utilize predefined metrics from models)
        :param output: the output from predictions
        :param metric_names: name of metrics desired for evaluation
        :return: a dictionary of metric_name to result
        """
        metric_paths = [get_metric_path(name) for name in metric_names]
        results = {}
        for metric_path in metric_paths:
            metric = load_metric(metric_path, keep_in_memory=True)
            metric_result = metric.compute(predictions=preds, references=label_ids)
            results[get_metric_name(metric)] = metric_result
        return results

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
