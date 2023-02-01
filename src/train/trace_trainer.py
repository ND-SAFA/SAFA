import os
from functools import partial
from typing import Optional, Tuple

import torch
from accelerate import find_executable_batch_size
from datasets import Dataset
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import PreTrainedModel, Trainer
from transformers.modeling_outputs import SequenceClassifierOutput
from transformers.trainer_utils import PredictionOutput

from data.datasets.data_key import DataKey
from data.datasets.dataset_role import DatasetRole
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from data.samplers.balanced_batch_sampler import BalancedBatchSampler
from models.model_manager import ModelManager
from train.base_trainer import BaseTrainer
from train.save_strategy.save_strategy_stage import SaveStrategyStage
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trace_output.trace_train_output import TraceTrainOutput
from train.trackers.link_training_tracker import LinkTrainingTracker
from train.trainer_args import TrainerArgs
from train.trainer_tools.supported_optimizers import SupportedOptimizers
from train.trainer_tools.supported_schedulers import SupportedSchedulers
from train.trainer_tools.trace_accelerator import TraceAccelerator
from util.file_util import FileUtil
from util.logging.logger_manager import logger
from util.override import overrides


class TraceTrainer(BaseTrainer):
    """
    Trace trainer for training for trace link prediction.
    """
    BEST_MODEL_NAME = "best"
    CURRENT_MODEL_NAME = "current"
    OPTIMIZER_FILE_NAME = "optimizer.bin"
    SCHEDULER_FILE_NAME = "scheduler.bin"

    def __init__(self, trainer_args: TrainerArgs, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager,
                 **kwargs):
        super().__init__(trainer_args, model_manager, trainer_dataset_manager, **kwargs)
        TraceAccelerator.update(gradient_accumulation_steps=self.trainer_args.gradient_accumulation_steps)
        self.__should_prepare_accumulator = True
        self._link_tracker = LinkTrainingTracker(self.trainer_dataset_manager[DatasetRole.TRAIN]) \
            if DatasetRole.TRAIN in self.trainer_dataset_manager else None

    def train(self, resume_from_checkpoint: str = None, **kwargs) -> TraceTrainOutput:
        """
        Train model on data with optimal batch size.
        :param resume_from_checkpoint: The checkpoint to resume from.
        :return: Output of training session.
        """
        self.model = self.model_manager.get_model()
        inner_training_loop = find_executable_batch_size(
            self.inner_training_loop) if self.trainer_args.per_device_train_batch_size is None else self.inner_training_loop
        trace_train_output = inner_training_loop(resume_from_checkpoint=resume_from_checkpoint)
        self.__should_prepare_accumulator = True
        if self.trainer_args.load_best_model_at_end:
            if not self.trainer_args.should_save:
                logger.warning("Unable to load best model because configuration defined `should_save` to False.")
            else:
                best_model_path = self.get_output_path(self.BEST_MODEL_NAME)
                self.model = self.model_manager.update_model(best_model_path)
        return trace_train_output

    def inner_training_loop(self, batch_size: int = None,
                            resume_from_checkpoint: Optional[str] = None, **kwargs) -> TraceTrainOutput:
        """
        Trains model for the epochs specified in training arguments.
        :param batch_size: The batch size of the training step.
        :param kwargs: Any additional arguments. Currently, ignored but necessary for finding optimal batch size.
        :return: The output of the training session.
        """
        if batch_size is None:
            batch_size = self.args.per_device_train_batch_size
        self._train_batch_size = batch_size
        self.args.per_device_train_batch_size = batch_size
        loss_function = self.trainer_args.loss_function
        self.model.train()
        model, train_data_loader, optimizer, scheduler = self.create_or_load_state(self.model,
                                                                                   self.get_train_dataloader(),
                                                                                   resume_from_checkpoint)
        model = TraceAccelerator.prepare_model(model)
        logger.info(f"Number of GPUS: {TraceAccelerator.num_processes}. Torch devices: {torch.cuda.device_count()}")
        global_step = 0
        training_loss = 0
        training_metrics = {}
        epoch_loss = 0
        accelerate_tqdm = partial(tqdm, disable=not TraceAccelerator.is_main_process, position=0)
        for epoch_index in range(self.trainer_args.num_train_epochs):
            with TraceAccelerator.accumulate(model):
                for batch_index, batch in enumerate(accelerate_tqdm(train_data_loader)):
                    batch = batch.to(TraceAccelerator.device)

                    labels = batch.pop(DataKey.LABELS_KEY)
                    output: SequenceClassifierOutput = model(**batch)
                    loss = loss_function(output.logits, labels)

                    TraceAccelerator.backward(loss)
                    optimizer.step()
                    optimizer.zero_grad()
                    self.on_step(global_step)
                    training_loss += loss.item()
                    global_step += 1
                    epoch_loss += loss.item()

            logger.info(f"Epoch Loss: {epoch_loss}")
            epoch_loss = 0
            scheduler.step()
            self.on_epoch(epoch_index)
        return TraceTrainOutput(global_step=global_step, training_loss=training_loss, metrics=training_metrics,
                                val_metrics=self.save_strategy.stage_evaluations)

    def predict(self, test_dataset: Dataset) -> PredictionOutput:
        """
        Moves model to accelerate device then predicts current model on dataset.
        :param test_dataset: Dataset: The dataset to evaluate.
        :return: The prediction output.
        """
        test_dataloader = self.get_test_dataloader(test_dataset)
        self.model, eval_data_loader, _, _ = self._prepare_accelerator(self.model, test_dataloader)
        self.model.eval()
        eval_predictions, eval_labels = [], []
        for batch in test_dataloader:
            batch.to(TraceAccelerator.device)
            targets = batch.pop("labels")
            with torch.no_grad():
                output = self.model(**batch)
            eval_predictions.append(output.logits)
            eval_labels.append(targets)

        eval_labels = torch.cat(eval_labels, dim=0)
        eval_predictions = torch.cat(eval_predictions, dim=0)
        eval_labels, eval_predictions = TraceAccelerator.gather((eval_labels, eval_predictions))
        eval_predictions = eval_predictions.cpu().numpy()[:len(test_dataset)]
        eval_labels = eval_labels.cpu().numpy()[:len(test_dataset)]
        return PredictionOutput(predictions=eval_predictions, label_ids=eval_labels, metrics={})

    def create_or_load_state(self, model: PreTrainedModel, data_loader: DataLoader, resume_from_checkpoint: Optional[str] = None) \
            -> Tuple[PreTrainedModel, DataLoader, Optimizer, _LRScheduler]:
        """
        If checkpoint given, accelerate entities are instantiated with their previous state. Otherwise, they are instantiated with new
        states.
        :param model: The model to use to prepare the accelerator
        :param data_loader: The data loader to use to prepare the accelerator
        :param resume_from_checkpoint: Path to previous checkpoint.
        :type resume_from_checkpoint:
        :return: Instantiated model, optimizer, scheduler, and train data loader.
        """
        model, data_loader, optimizer, scheduler = self._prepare_accelerator(model, data_loader)
        if resume_from_checkpoint:
            TraceAccelerator.load_state(resume_from_checkpoint)
        return model, data_loader, optimizer, scheduler

    @overrides(Trainer)
    def save_model(self, output_dir: Optional[str] = None, _internal_call: bool = False) -> None:
        """
        Saves model, configuration, tokenizer, optimizer, and scheduler.
        :param output_dir: The path to save the entities to.
        :param _internal_call: Internal property used within HuggingFace Trainer.
        :return: None
        """
        if TraceAccelerator.is_main_process:
            if not output_dir:
                raise ValueError("Expected output_dir to be defined.")
            if self.trainer_args.skip_save:
                return
            FileUtil.create_dir_safely(output_dir)
            model = TraceAccelerator.unwrap_model(self.model)
            self._save(output_dir, state_dict=model.state_dict())
            TraceAccelerator.save(self.optimizer.state_dict(), os.path.join(output_dir, self.OPTIMIZER_FILE_NAME))
            TraceAccelerator.save(self.lr_scheduler.state_dict(), os.path.join(output_dir, self.SCHEDULER_FILE_NAME))
            self.model_manager.get_config().save_pretrained(output_dir)
            self.model_manager.get_tokenizer().save_pretrained(output_dir)

    def on_step(self, step_iteration: int) -> None:
        """
        Callback function called after every training step.
        :param step_iteration: The global step count of the training loop.
        :return: None
        """
        self.conditional_evaluate(SaveStrategyStage.STEP, step_iteration)

    def on_epoch(self, epoch_iteration: int) -> None:
        """
        Callback function called after every training epoch.
        :param epoch_iteration: The index of epoch performed.
        :return: None
        """
        self.conditional_evaluate(SaveStrategyStage.EPOCH, epoch_iteration)
        self.save_model(self.get_output_path(self.CURRENT_MODEL_NAME))

    def conditional_evaluate(self, stage: SaveStrategyStage, stage_iteration: int) -> None:
        """
        Conditionally evaluates model depending on save strategy and saves it if it is the current best.
        :param stage: The stage in training.
        :param stage_iteration: The number of times this stage has been reached.
        :return: None
        """
        should_evaluate = self.save_strategy.should_evaluate(stage, stage_iteration)

        if should_evaluate and DatasetRole.VAL in self.trainer_dataset_manager:
            eval_result: TracePredictionOutput = self.perform_prediction(DatasetRole.VAL)
            previous_best = self.save_strategy.best_scores
            should_save = self.save_strategy.should_save(eval_result.metrics, stage_iteration)
            if should_save:
                current_score = self.save_strategy.get_metric_scores(eval_result.metrics)
                logger.log_with_title("Saving Best Model", f"New Best: {current_score}\tPrevious: {previous_best}")
                self.save_model(self.get_output_path(self.BEST_MODEL_NAME))
                logger.log_with_title("Evaluation Finished.", "-" * 10)
            else:
                logger.info(f"Previous best is still {previous_best}.")

    def get_output_path(self, dir_name: str = None):
        """
        Returns the output path of trainer, with argument accessing directories within it.
        :param dir_name: The directory within the output path to retrieve.
        :return: The path to the trainer output or directory within it.
        """
        base_output_path = self.trainer_args.output_dir
        if dir_name:
            return os.path.join(base_output_path, dir_name)
        return base_output_path

    def _prepare_accelerator(self, model: PreTrainedModel, data_loader: DataLoader) \
            -> Tuple[PreTrainedModel, DataLoader, Optimizer, _LRScheduler]:
        """
        Prepares the model, optimizer, scheduler and data loader for distributed training.
        :param model: The model being trained.
        :param data_loader: The data loader containing training data.
        :return: Prepared model, optimizer, scheduler, and data loader.
        """
        if self.optimizer is None or self.lr_scheduler is None:
            self._initialize_state(model)
        if not self.__should_prepare_accumulator:
            return model, data_loader, self.optimizer, self.lr_scheduler
        TraceAccelerator.clear()
        self.__should_prepare_accumulator = False
        return TraceAccelerator.prepare(model, data_loader, self.optimizer, self.lr_scheduler)

    def _initialize_state(self, model: PreTrainedModel) -> None:
        """
        Initializes related entities for accelerator preparation.
        :param model: The model used to initialize the optimizer.
        :return: None
        """
        self.optimizer = SupportedOptimizers.create(self.trainer_args.optimizer_name, model)
        self.lr_scheduler = SupportedSchedulers.create(self.trainer_args.scheduler_name, self.optimizer)

    @overrides(Trainer)
    def _get_train_sampler(self) -> Optional[torch.utils.data.Sampler]:
        """
        Gets the data sampler used for training
        :return: the train sampler
        """
        if self.trainer_args.use_balanced_batches and self.train_dataset is not None:
            return BalancedBatchSampler(data_source=self.train_dataset, batch_size=self._train_batch_size)
        return super()._get_train_sampler()
