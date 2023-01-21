import os
from copy import deepcopy
from typing import Any, Dict, List, NamedTuple, Tuple, Union

import numpy as np
import torch
from accelerate import Accelerator, memory_utils
from datasets import load_metric
from scipy.special import softmax
from tqdm import tqdm
from transformers.modeling_outputs import SequenceClassifierOutput
from transformers.trainer import Trainer
from transformers.trainer_utils import PREFIX_CHECKPOINT_DIR

from data.datasets.data_key import DataKey
from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from data.datasets.trace_matrix import TraceMatrixManager
from models.model_manager import ModelManager
from train.metrics.map_at_k_metric import MapAtKMetric
from train.metrics.map_metric import MapMetric
from train.metrics.precision_at_threshold_metric import PrecisionAtKMetric
from train.metrics.recall_at_threshold_metric import RecallAtThresholdMetric
from train.metrics.supported_trace_metric import get_metric_name, get_metric_path
from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy, SaveStrategyStage
from train.trainer_args import TrainerArgs
from util.base_object import BaseObject
from util.file_util import FileUtil

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
torch.use_deterministic_algorithms(True)

TRIAL = Union["optuna.Trial", Dict[str, Any]]


class TraceTrainer(Trainer, BaseObject):
    """
    Responsible for using given model for training and prediction using given data.
    """
    BEST_MODEL_NAME = "best"

    def __init__(self, trainer_args: TrainerArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, **kwargs):
        """
        Handles the training and evaluation of learning models
        :param args: the learning model arguments
        """
        self.trainer_args = trainer_args
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model_manager = model_manager
        self.model_manager.set_max_seq_length(self.trainer_args.max_seq_length)
        model_init = lambda: self.model_manager.get_model()
        tokenizer = self.model_manager.get_tokenizer()
        super().__init__(model_init=model_init, args=trainer_args, tokenizer=tokenizer,
                         callbacks=trainer_args.callbacks,
                         **kwargs)

    def perform_training(self, checkpoint: str = None) -> Dict:
        """
        Performs the model training.
        :param checkpoint: path to checkpoint.
        :return: a dictionary containing the results
        """
        self.model = self.model_manager.get_model()
        self._move_model_to_device(self.model, self.args.device)
        self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_trainer_dataset(self.model_manager,
                                                                                                self.trainer_args.train_batch_size)
        train_function = self.custom_train if self.trainer_args.use_custom_train_loop else self.train
        output = train_function(resume_from_checkpoint=checkpoint)
        output_dict = TraceTrainer.output_to_dict(output)
        return output_dict

    def custom_train(self, resume_from_checkpoint: str = None):
        # TODO : Add timing metrics (e.g. total time per epoch)
        # TODO : If loss is nan or inf simply add the average of previous logged losses
        # TODO: Add flag to load best model at the end

        accelerator = Accelerator(gradient_accumulation_steps=self.trainer_args.gradient_accumulation_steps)
        device = accelerator.device
        self.model = self.model_manager.get_model()
        self.model.to(device)
        inner_training_loop = memory_utils.find_executable_batch_size(self._inner_custom_training_loop)
        return inner_training_loop(resume_from_checkpoint=resume_from_checkpoint, accelerator=accelerator, device=device)

    def _inner_custom_training_loop(
            self, batch_size=None, args=None, resume_from_checkpoint=None, trial=None, ignore_keys_for_eval=None, accelerator=None,
            device=None,
    ):
        self._train_batch_size = batch_size
        self.args.per_device_train_batch_size = batch_size
        optimizer = self.trainer_args.optimizer_constructor(self.model.parameters())
        scheduler = self.trainer_args.scheduler_constructor(optimizer)
        loss_function = self.trainer_args.loss_function
        data = self.get_train_dataloader()

        model, optimizer, scheduler, data = accelerator.prepare(self.model, optimizer, scheduler, data)
        model.train()
        training_output: Dict = {}
        save_strategy = self.trainer_args.custom_save_strategy

        for epoch in range(self.trainer_args.num_train_epochs):
            for batch_index, batch in enumerate(tqdm(data)):
                batch = batch.to(device)
                optimizer.zero_grad()

                labels = batch.pop(DataKey.LABELS_KEY)
                output: SequenceClassifierOutput = model(**batch)
                loss = loss_function(output.logits, labels)

                # loss.backward()
                accelerator.backward(loss)
                optimizer.step()
                self.conditional_evaluate(save_strategy, SaveStrategyStage.STEP, batch_index)

            scheduler.step()
            self.conditional_evaluate(save_strategy, SaveStrategyStage.EPOCH, epoch)

    def conditional_evaluate(self, save_strategy: AbstractSaveStrategy, stage: SaveStrategyStage, stage_iteration: int) -> None:
        """
        Conditionally evaluates model depending on save strategy and saves it if it is the current best.
        :param save_strategy: The strategy determining if it is time to evaluate.
        :param stage: The stage in training.
        :param stage_iteration: The number of times this stage has been reached.
        :return: None
        """
        should_evaluate = save_strategy.should_evaluate(stage, stage_iteration)

        if should_evaluate:
            eval_result = self.perform_prediction(DatasetRole.VAL)
            should_save = save_strategy.should_save(eval_result)
            if should_save:
                self.save_model_and_checkpoint()

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> Dict:
        """
        Performs the prediction and (optionally) evaluation for the model
        :return: A dictionary containing the results.
        """
        dataset = self.trainer_dataset_manager[dataset_role]
        self.eval_dataset = dataset.to_trainer_dataset(self.model_manager)
        output = self.predict(self.eval_dataset)
        scores = self.get_similarity_scores(output.predictions)
        trace_matrix = TraceMatrixManager(dataset.get_ordered_links(), scores)
        results = self._eval(trace_matrix, scores, output.label_ids, output.metrics,
                             self.trainer_args.metrics) if self.trainer_args.metrics else None
        output_dict = TraceTrainer.output_to_dict(output, metrics=results, predictions=scores,
                                                  source_target_pairs=dataset.get_source_target_pairs())
        return output_dict

    def save_model_and_checkpoint(self, output_dir: str = None) -> None:
        """
        Saves the model and checkpoint
        :param output_dir: the path to save the model to
        :return: None
        """
        # self.save_model(output_dir)
        self.save_checkpoint(output_dir)

    def save_checkpoint(self, output_dir: str = None, trial: TRIAL = None, save_metrics: bool = False):
        """
        Saves the checkpoint in the output dir specified in training args
        :param output_dir: where to save the checkpoint to
        :param trial: optional, will be given to the original _save_checkpoint if provided
        :param save_metrics: if True, gives the metrics to the original _save_checkpoint so the best_metric can be saved in state
        :return: None
        """
        metrics = self.trainer_args.metrics if save_metrics else None
        if self.model is None:
            raise Exception("Must perform training before checkpoint can be saved.")
        self._save_checkpoint(model=self.model, trial=trial, metrics=metrics)
        checkpoint_dir = self._get_checkpoint_dir()
        assert checkpoint_dir is not None
        checkpoint_path = os.path.join(self.trainer_args.output_dir, checkpoint_dir)
        FileUtil.move_dir_contents(orig_path=checkpoint_path, new_path=output_dir if output_dir else self.trainer_args.output_dir,
                                   delete_after_move=True)

    def _get_checkpoint_dir(self) -> str:
        """
        Gets the directory where the checkpoint was saved to
        :return:the checkpoint dir if the checkpoint was saved properly
        """
        checkpoint_dir = [dir_name for dir_name in os.listdir(self.trainer_args.output_dir)
                          if os.path.isdir(os.path.join(self.trainer_args.output_dir, dir_name))
                          and dir_name.startswith(PREFIX_CHECKPOINT_DIR)]
        return checkpoint_dir.pop() if len(checkpoint_dir) > 0 else None

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

    @staticmethod
    def output_to_dict(output: NamedTuple, **kwargs) -> Dict:
        """
        Converts train/prediction output to a dictionary
        :param output: output from training or prediction
        :return: the output represented as a dictionary
        """
        base_output = {field: kwargs[field] if (field in kwargs and kwargs[field]) else getattr(output, field) for field
                       in output._fields}
        additional_attrs = {field: kwargs[field] for field in kwargs.keys() if field not in base_output}
        return {**base_output, **additional_attrs}

    @staticmethod
    def _eval(trace_matrix: TraceMatrixManager, predicted_scores: List[float], label_ids: np.ndarray,
              output_metrics: Dict, metric_names: List) -> Dict:
        """
        Performs the evaluation of the model (use this instead of Trainer.evaluation to utilize predefined metrics from models)
        :param trace_matrix: the matrix of trace links and their scores
        :param predicted_scores: a list of the predicted similarity scores
        :param label_ids: the list of ground truth labels
        :param output_metrics: the dictionary of metrics to include in the results
        :param metric_names: name of metrics desired for evaluation
        :return: a dictionary of metric_name to result
        """
        metric_paths = [get_metric_path(name) for name in metric_names]
        results = deepcopy(output_metrics)
        trace_matrix_metrics = [MapMetric.name, MapAtKMetric.name, PrecisionAtKMetric.name,
                                RecallAtThresholdMetric.name]
        for metric_path in metric_paths:
            metric = load_metric(metric_path, keep_in_memory=True)
            args = {"trace_matrix": trace_matrix} if metric.name in trace_matrix_metrics else {}
            metric_result = metric.compute(predictions=predicted_scores, references=label_ids, **args)
            metric_name = get_metric_name(metric)
            if isinstance(metric_result, dict):
                results.update(metric_result)
            else:
                results[metric_name] = metric_result
        return results
