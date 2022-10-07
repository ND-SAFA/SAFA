from typing import Dict, List, NamedTuple

from datasets import load_metric
from scipy.special import softmax
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.sampler import RandomSampler
from transformers.trainer import Trainer
from transformers.trainer_pt_utils import get_tpu_sampler, is_torch_tpu_available
from transformers.trainer_utils import PredictionOutput

from common.api.responses import PredictionResponse
from trace.config.constants import LINKED_TARGETS_ONLY_DEFAULT
from trace.jobs.trace_args import TraceArgs
from trace.metrics.supported_trace_metric import get_metric_path


class TraceTrainer(Trainer):
    """
    Responsible for using given model for training and prediction using given dataset.
    """

    def __init__(self, args: TraceArgs):
        """
        Handles the training and evaluation of learning models
        :param args: the learning model arguments
        """
        self.args = args
        self.model_generator = args.model_generator
        self.model_generator.set_max_seq_length(self.args.max_seq_length)
        self.trace_dataset_creator = args.trace_dataset_creator
        model = self.model_generator.get_model()
        tokenizer = self.model_generator.get_tokenizer()
        super().__init__(model=model, args=args, tokenizer=tokenizer, callbacks=args.callbacks)

    def perform_training(self, checkpoint: str = None) -> Dict:
        """
        Performs the model training
        :param checkpoint: path to checkpoint
        :return: a dictionary containing the results
        """
        self.train_dataset = self.trace_dataset_creator.get_training_dataset(self.args.resample_rate).data
        self.eval_dataset = self.trace_dataset_creator.get_validation_dataset(self.args.eval_dataset_size,
                                                                              linked_targets_only=LINKED_TARGETS_ONLY_DEFAULT).data
        output = self.train(resume_from_checkpoint=checkpoint)

        self.save_model(self.args.model_generator.model_path)
        return TraceTrainer.output_to_dict(output)

    def perform_prediction(self, dataset) -> Dict:
        """
        Performs the prediction and (optionally) evaluation for the model
        :return: a dictionary containing the results
        """
        dataset = self.trace_dataset_creator.get_prediction_dataset() if dataset is None else dataset
        self.eval_dataset = dataset.data
        output = self.predict(self.eval_dataset)
        print(self.args.metrics)
        if self.args.metrics:
            self._eval(output, self.args.metrics)
        output_dict = TraceTrainer.output_to_dict(output)
        return PredictionResponse.from_output(output_dict, dataset.source_target_pairs)

    @staticmethod
    def output_to_dict(output: NamedTuple) -> Dict:
        """
        Converts train/prediction output to a dictionary
        :param output: output from training or prediction
        :return: the output represented as a dictionary
        """
        return {field: getattr(output, field) for field in output._fields}

    @staticmethod
    def _eval(output: PredictionOutput, metric_names: List):
        """
        Performs the evaluation of the model (use this instead of Trainer.evaluation to utilize predefined metrics from models)
        :param output: the output from predictions
        :param metric_names: name of metrics desired for evaluation
        """
        preds = TraceTrainer.get_similarity_scores(output.predictions)
        metric_paths = [get_metric_path(name) for name in metric_names]
        for metric_path in metric_paths:
            metric = load_metric(metric_path, keep_in_memory=True)
            results = metric.compute(predictions=preds, references=output.label_ids)
            output.metrics.update(results)

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
    def get_similarity_scores(predictions):
        similarity_scores = []
        for pred_i in range(predictions.shape[0]):
            prediction = predictions[pred_i]
            similarity_scores.append(softmax(prediction)[1])
        return similarity_scores
