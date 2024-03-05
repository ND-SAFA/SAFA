import os
from typing import Any, Dict, List, Optional, Union

import torch
from datasets import Dataset
from transformers.integrations import WandbCallback
from transformers.trainer import Trainer
from transformers.trainer_utils import EvalPrediction, PredictionOutput

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.script_constants import DISPLAY_METRICS
from tgen.common.logging.logger_manager import logger
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.file_util import FileUtil
from tgen.common.util.override import overrides
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from tgen.core.save_strategy.comparison_criteria import ComparisonCriterion
from tgen.core.save_strategy.metric_save_strategy import MetricSaveStrategy
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.core.trainers.abstract_trainer import AbstractTrainer
from tgen.core.wb.trace_callback import TraceCallback
from tgen.core.wb.wb_manager import WBManager
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.data_key import DataKey
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.metrics.metrics_manager import MetricsManager
from tgen.models.model_manager import ModelManager

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
TRIAL = Union["optuna.Trial", Dict[str, Any]]

DEFAULT_EVALUATION_ROLES = [DatasetRole.VAL, DatasetRole.EVAL]


class HuggingFaceTrainer(AbstractTrainer, Trainer):
    """
    Trains model on data for generic task.
    """

    def __init__(self, trainer_args: HuggingFaceArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, save_strategy: AbstractSaveStrategy = None,
                 evaluation_roles: List[DatasetRole] = None, **kwargs):
        """
        Handles the training and evaluation of learning models
        :param trainer_args: The learning model arguments
        :param model_manager: The manager for the model used for training and/or predicting
        :param trainer_dataset_manager: The manager for the datasets used for training and/or predicting
        :param save_strategy: The strategy used to save the best model
        :param: evaluation_roles: Defines the roles to evaluate the model on during prediction.
        :param kwargs: Any additional arguments given to the HF Trainer
        :param evaluation_roles: The roles to evaluate before and after training.
        """
        if trainer_args.eager_load_data:
            trainer_dataset_manager.get_hf_datasets(model_manager)  # prepares datasets and caches them
        if evaluation_roles is None:
            evaluation_roles = DEFAULT_EVALUATION_ROLES
        if save_strategy is None:
            save_strategy = MetricSaveStrategy(ComparisonCriterion(["map", "f2"]))
        trainer_args.__post_init__()
        super().__init__(trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args)
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model_manager = model_manager
        self.model_manager.set_max_seq_length(self.trainer_args.max_seq_length)
        self.trainer_args.remove_unused_columns = False
        self.evaluation_roles = evaluation_roles
        self.save_strategy = save_strategy
        self.post_init(trainer_args, **kwargs)
        self._current_eval_role = None

    def post_init(self, trainer_args: HuggingFaceArgs, **kwargs):
        """
        Re-initializes the trainer static variables with the current trainer settings.
        :param trainer_args: The starting trainer args.
        :param kwargs: Additional keyword arguments passed to original trainer.
        :return:
        """
        callbacks = [TraceCallback()]
        model_init = lambda: self.model_manager.get_model()
        tokenizer = self.model_manager.get_tokenizer()
        Trainer.__init__(self, model_init=model_init, args=trainer_args, tokenizer=tokenizer, callbacks=callbacks, **kwargs)
        self.remove_callback(WandbCallback)

    def perform_training(self) -> TraceTrainOutput:
        """
        Performs the model training.
        :return: a dictionary containing the results
        """
        WBManager.update_config(args=self.trainer_args)
        self.compute_metrics = self._compute_validation_metrics  # Will compute trace metrics alongside default eval metrics
        self.train_dataset = self._get_dataset(DatasetRole.TRAIN)
        self.eval_dataset = self._get_dataset(DatasetRole.VAL)
        self.model = self.model_manager.get_model()
        if self.trainer_args.do_training_eval:
            self._evaluate(step=0)
        hf_train_output = self.train(resume_from_checkpoint=self.trainer_args.checkpoint_path)
        train_output = TraceTrainOutput(train_output=hf_train_output)
        if self.trainer_args.do_training_eval:
            train_output.prediction_output = self._evaluate()
        if self.trainer_args.save_best_model:
            self._save_best_model()
        return train_output

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL, dataset: iDataset = None) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :param dataset: The dataset to use instead of from the dataset manager
        :return: THe prediction output
        """
        if not self.has_dataset(dataset_role):
            raise Exception(f"Trainer does not have dataset for {dataset_role}.")
        output = self.predict(dataset_role)
        display_metrics = {k: round(output.metrics[k], 4) for k in DISPLAY_METRICS if k in output.metrics}
        logger.log_with_title(f"{dataset_role.name.title()} Metrics", display_metrics)
        trace_dataset: TraceDataset = self.trainer_dataset_manager[dataset_role]
        prediction_entries = trace_dataset.trace_df.get_links()

        return TracePredictionOutput(predictions=output.predictions,
                                     label_ids=output.label_ids,
                                     metrics=output.metrics,
                                     prediction_entries=prediction_entries)

    def predict(self, dataset_role: DatasetRole, **kwargs) -> PredictionOutput:
        """
        Predicts on the dataset at given role and calculates metrics.
        :param dataset_role:
        :param kwargs:
        :return:
        """
        self._current_eval_role = dataset_role
        dataset = self._get_dataset(dataset_role)
        output = super().predict(dataset, **kwargs)

        if not DictUtil.contains_keys(output.metrics, self.trainer_args.metrics):
            trace_metrics = self._compute_validation_metrics(EvalPrediction(output.predictions, output.label_ids))
            output.metrics.update(trace_metrics)
        return output

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

    def _save_best_model(self) -> None:
        """
        Sets the path of the best to be in the expected location
        :return: None
        """
        best_model_path = self.state.best_model_checkpoint
        if best_model_path is None:
            logger.info("State: best_model_checkpoint is not defined. Not saving best model.")
            return

        model_dir_path = self.trainer_args.best_model_path if self.trainer_args.best_model_path else self.trainer_args.output_dir
        FileUtil.move_dir_contents(best_model_path, model_dir_path, delete_after_move=False)
        logger.info(f"Best model at: {model_dir_path}")

    def _evaluate(self, **kwargs) -> Dict[DatasetRole, TracePredictionOutput]:
        """
        Performs an evaluation on the training output using the EVAL dataset if provided
        :return: Map of dataset role evaluated to its prediction output.
        """
        logger.log_title("Evaluating Model", prefix=NEW_LINE)
        results = {}
        for dataset_role in self.evaluation_roles:
            if self.has_dataset(dataset_role):
                logger.log_step(f"{dataset_role.name.title()} Set")
                prediction_output = self.perform_prediction(dataset_role)
                results[dataset_role] = prediction_output
            else:
                logger.warning(f"No {dataset_role} dataset. Skipping evaluation.")
                continue

        WBManager.log({r: output.metrics for r, output in results.items()}, **kwargs)
        return results

    @overrides(Trainer)
    def _get_train_sampler(self) -> Optional[torch.utils.data.Sampler]:
        """
        Gets the data sampler used for training
        :return: the train sampler
        """
        if self.trainer_args.use_balanced_batches and self.train_dataset is not None and DataKey.LABEL_KEY in self.train_dataset[0]:
            logger.warning("Balanced batching is not currently supported!")
        return super()._get_train_sampler()

    def _compute_validation_metrics(self, output: EvalPrediction) -> Dict:
        """
        Callback that allows Trainer to compute trace metrics on validation set.
        :param output:The prediction output on a trace dataset.
        :return: Trace metrics associated with prediction.
        """
        trace_dataset = self.trainer_dataset_manager[self._current_eval_role]
        n_labels = trace_dataset.trace_df.get_label_count()
        if n_labels == 0:
            logger.info("Could not evaluate predictions because no true labels are present.")
            return {}
        
        metrics_manager = MetricsManager(trace_df=trace_dataset.trace_df,
                                         link_ids=trace_dataset.get_ordered_link_ids(),
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

    def has_dataset(self, dataset_role: DatasetRole) -> bool:
        """
        Checks whether trainer contains dataset for given role.
        :param dataset_role: The role to check for.
        :return: Whether dataset is contained for given role.
        """
        datasets = self.trainer_dataset_manager.get_hf_datasets(self.model_manager)
        return dataset_role in datasets
