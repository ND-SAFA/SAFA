import os
from typing import Any, Dict, Optional, Union

import torch
from datasets import Dataset
from transformers.integrations import WandbCallback
from transformers.trainer import Trainer
from transformers.trainer_utils import PredictionOutput

from tgen.common.constants.experiment_constants import BEST_MODEL_NAME
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.override import overrides
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from tgen.core.save_strategy.comparison_criteria import ComparisonCriterion
from tgen.core.save_strategy.metric_save_strategy import MetricSaveStrategy
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.core.trainers.abstract_trainer import AbstractTrainer
from tgen.core.wandb.trace_callback import TraceCallback
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.data_key import DataKey
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.metrics.metrics_manager import MetricsManager
from tgen.models.model_manager import ModelManager

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
TRIAL = Union["optuna.Trial", Dict[str, Any]]


class HuggingFaceTrainer(AbstractTrainer, Trainer):
    """
    Trains model on data for generic task.
    """

    def __init__(self, trainer_args: HuggingFaceArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, save_strategy: AbstractSaveStrategy = None,
                 **kwargs):
        """
        Handles the training and evaluation of learning models
        :param trainer_args: The learning model arguments
        :param model_manager: The manager for the model used for training and/or predicting
        :param trainer_dataset_manager: The manager for the datasets used for training and/or predicting
        :param save_strategy: The strategy used to save the best model
        :param kwargs: Any additional arguments given to the HF Trainer
        """
        if trainer_args.eager_load_data:
            trainer_dataset_manager.get_hf_datasets(model_manager)  # prepares datasets and caches them
        trainer_args.__post_init__()
        super().__init__(trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args)
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model_manager = model_manager
        self.model_manager.set_max_seq_length(self.trainer_args.max_seq_length)
        self.trainer_args.remove_unused_columns = False
        callbacks = [TraceCallback()]
        model_init = lambda: self.model_manager.get_model()
        tokenizer = self.model_manager.get_tokenizer()
        if save_strategy is None:
            self.save_strategy = MetricSaveStrategy(ComparisonCriterion(["map", "f2"]))
        Trainer.__init__(self, model_init=model_init, args=trainer_args, tokenizer=tokenizer, callbacks=callbacks, **kwargs)
        self.remove_callback(WandbCallback)

    def perform_training(self) -> TraceTrainOutput:
        """
        Performs the model training.
        :return: a dictionary containing the results
        """
        self.compute_metrics = self._compute_validation_metrics  # Will compute trace metrics alongside default eval metrics
        self.train_dataset = self._get_dataset(DatasetRole.TRAIN)
        self.eval_dataset = self._get_dataset(DatasetRole.VAL)
        self.model = self.model_manager.get_model()
        hf_train_output = self.train(resume_from_checkpoint=self.trainer_args.checkpoint_path)
        train_output = TraceTrainOutput(train_output=hf_train_output)
        self._evaluate_training(train_output)
        self._set_best_model_path()
        return train_output

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL, dataset: iDataset = None) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :param dataset: The dataset to use instead of from the dataset manager
        :return: THe prediction output
        """
        dataset = self.trainer_dataset_manager[dataset_role] if not dataset else dataset
        if self.eval_dataset is None:
            self.eval_dataset = dataset.to_hf_dataset(self.model_manager)
        output = self.predict(self.eval_dataset)
        metrics_manager = MetricsManager(trace_df=dataset.trace_df,
                                         link_ids=dataset.get_ordered_link_ids(),
                                         trace_predictions=output.predictions)
        eval_metrics = metrics_manager.eval(self.trainer_args.metrics)
        logger.log_with_title(f"{dataset_role.name} Metrics", repr(eval_metrics))
        output.metrics.update(eval_metrics)

        return TracePredictionOutput(predictions=metrics_manager.get_scores(),
                                     label_ids=metrics_manager.trace_matrix.labels,
                                     metrics=output.metrics,
                                     prediction_entries=metrics_manager.get_trace_predictions())

    def push_to_hub(self, **kwargs) -> Dict[str, str]:
        """
        Pushes the model to the HF hub
        :param kwargs: Additional arguments for push to hub
        :return The url of the commit
        """
        assert self.args.hub_model_id is not None, f"Expected hub_model_id to be defined but found none."
        return {'commit_url': super().push_to_hub(**kwargs)}

    def cleanup(self) -> None:
        """
        Free memory associated with trainer.
        :return: None
        """
        if self.model:
            del self.model

    def _set_best_model_path(self) -> None:
        """
        Sets the path of the best to be in the expected location
        :return: None
        """
        best_model_path = self.state.best_model_checkpoint
        if best_model_path:
            best_model_dir = os.path.join(self.trainer_args.output_dir, BEST_MODEL_NAME)
            if os.path.exists(best_model_dir):
                os.rmdir(best_model_dir)
            os.rename(best_model_path, best_model_dir)

    def _evaluate_training(self, train_output: TraceTrainOutput) -> None:
        """
        Performs an evaluation on the training output using the EVAL dataset if provided
        :param train_output: Output from training
        :return: None
        """
        self.eval_dataset = self._get_dataset(DatasetRole.EVAL)
        self.compute_metrics = None
        if self.eval_dataset is not None:
            train_output.prediction_output = self.perform_prediction(DatasetRole.EVAL)

    @overrides(Trainer)
    def _get_train_sampler(self) -> Optional[torch.utils.data.Sampler]:
        """
        Gets the data sampler used for training
        :return: the train sampler
        """
        if self.trainer_args.use_balanced_batches and self.train_dataset is not None and DataKey.LABEL_KEY in self.train_dataset[0]:
            logger.warning("Balanced batching is not currently supported!")
        return super()._get_train_sampler()

    def _compute_validation_metrics(self, output: PredictionOutput, dataset_role: DatasetRole = DatasetRole.VAL) -> Dict:
        """
        Callback that allows Trainer to compute trace metrics on validation set.
        :param output:The prediction output on a trace dataset.
        :return: Trace metrics associated with prediction.
        """
        dataset = self.trainer_dataset_manager[dataset_role]
        metrics_manager = MetricsManager(trace_df=dataset.trace_df,
                                         link_ids=dataset.get_ordered_link_ids(),
                                         trace_predictions=output.predictions)
        trace_metrics = metrics_manager.eval(self.trainer_args.metrics)
        return trace_metrics

    def _get_dataset(self, dataset_role: DatasetRole) -> Optional[Dataset]:
        """
        Returns dataset set in role if it exists, otherwise none is returned.
        :param dataset_role: The role of the dataset to return.
        :return: Dataset at dataset role if it exists.
        """
        datasets = self.trainer_dataset_manager.get_hf_datasets(self.model_manager)
        return datasets[dataset_role] if dataset_role in datasets else None
