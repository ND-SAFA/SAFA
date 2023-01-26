import os
from typing import Optional, Tuple

import torch
from accelerate import Accelerator, find_executable_batch_size
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, PreTrainedModel, Trainer
from transformers.modeling_outputs import SequenceClassifierOutput

from config.override import overrides
from data.datasets.data_key import DataKey
from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from data.samplers.balanced_batch_sampler import BalancedBatchSampler
from models.model_manager import ModelManager
from train.base_trainer import BaseTrainer
from train.save_strategy.save_strategy_stage import SaveStrategyStage
from train.trace_output.trace_train_output import TraceTrainOutput
from train.trainer_args import TrainerArgs

os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'


class TraceTrainer(BaseTrainer):
    """
    Trace trainer for training for trace link prediction.
    """
    BEST_MODEL_NAME = "best"
    CURRENT_MODEL_NAME = "current"

    def __init__(self, trainer_args: TrainerArgs, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager,
                 **kwargs):
        super().__init__(trainer_args, model_manager, trainer_dataset_manager, **kwargs)
        self.accelerator: Optional[Accelerator] = None

    def train(self, resume_from_checkpoint: str = None, **kwargs) -> TraceTrainOutput:
        """
        Train model on data with optimal batch size.
        :param resume_from_checkpoint: The checkpoint to resume from.
        :return: Output of training session.
        """
        accelerator = Accelerator(gradient_accumulation_steps=self.trainer_args.gradient_accumulation_steps)
        device = accelerator.device
        self.model = self.model_manager.get_model()
        inner_training_loop = find_executable_batch_size(
            self.inner_training_loop) if self.trainer_args.per_device_train_batch_size is None else self.inner_training_loop
        trace_train_output = inner_training_loop(resume_from_checkpoint=resume_from_checkpoint, accelerator=accelerator, device=device)
        if self.trainer_args.load_best_model_at_end:
            best_model_path = self.get_output_path(self.BEST_MODEL_NAME)
            self.model = AutoModelForSequenceClassification.from_pretrained(best_model_path)
        return trace_train_output

    def inner_training_loop(self, batch_size: int = None, accelerator: Accelerator = None, device: torch.device = None,
                            resume_from_checkpoint: Optional[str] = None, **kwargs) -> TraceTrainOutput:
        """
        Trains model for the epochs specified in training arguments.
        :param batch_size: The batch size of the training step.
        :param accelerator: The accelerator used to perform distributed training of the model.
        :param device: The primary device to storage model.
        :param kwargs: Any additional arguments. Currently, ignored but necessary for finding optimal batch size.
        :return: The output of the training session.
        """
        if batch_size is None:
            batch_size = self.args.per_device_train_batch_size
        self._train_batch_size = batch_size
        self.args.per_device_train_batch_size = batch_size
        loss_function = self.trainer_args.loss_function
        self.model.train()
        model, optimizer, scheduler, train_data_loader = self.create_or_load_state(self.model,
                                                                                   self.get_train_dataloader(),
                                                                                   resume_from_checkpoint)
        global_step = 0
        training_loss = 0
        save_strategy = self.trainer_args.custom_save_strategy
        training_metrics = {}
        epoch_loss = 0
        for epoch_index in range(self.trainer_args.num_train_epochs):
            with accelerator.accumulate(model):
                for batch_index, batch in enumerate(tqdm(train_data_loader)):
                    batch = batch.to(device)

                    labels = batch.pop(DataKey.LABELS_KEY)
                    output: SequenceClassifierOutput = model(**batch)
                    loss = loss_function(output.logits, labels)
                    accelerator.backward(loss)
                    optimizer.step()
                    optimizer.zero_grad()

                    self.on_step(global_step)
                    training_loss += loss.item()
                    global_step += 1
                    epoch_loss += loss.item()

            epoch_loss = 0
            scheduler.step()
            self.on_epoch(epoch_index)
        return TraceTrainOutput(global_step=global_step, training_loss=training_loss, metrics=training_metrics,
                                eval_metrics=save_strategy.stage_evaluations)

    def create_or_load_state(self, model: PreTrainedModel, data_loader: DataLoader, resume_from_checkpoint: Optional[str] = None) \
            -> Tuple[PreTrainedModel, Optimizer, _LRScheduler, DataLoader]:
        """
        If checkpoint given, accelerate entities are instantiated with their previous state. Otherwise, they are instantiated with new
        states.
        :param model: The model to use to prepare accelerator
        :param data_loader: The data loader to use to prepare accelerator
        :param resume_from_checkpoint: Path to previous checkpoint.
        :type resume_from_checkpoint:
        :return: Instantiated model, optimizer, scheduler, and train data loader.
        """
        model, optimizer, scheduler, data_loader = self._prepare_accelerator(model, data_loader)
        if resume_from_checkpoint:
            self.accelerator.load_state(resume_from_checkpoint)
        return model, optimizer, scheduler, data_loader

    @overrides(Trainer)
    def save_model(self, output_dir: Optional[str] = None, _internal_call: bool = False) -> None:
        """
        Saves model, configuration, tokenizer, optimizer, and scheduler.
        :param output_dir: The path to save the entities to.
        :param _internal_call: Internal property used within HuggingFace Trainer.
        :return: None
        """
        if not output_dir:
            raise ValueError("Expected output_dir to be defined.")
        if self.trainer_args.skip_save:
            return
        super().save_model(output_dir=output_dir, _internal_call=_internal_call)
        self.accelerator.save_state(output_dir)

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
        save_strategy = self.trainer_args.custom_save_strategy
        should_evaluate = save_strategy.should_evaluate(stage, stage_iteration)

        if should_evaluate:
            eval_result = self.perform_prediction(DatasetRole.VAL)
            should_save = save_strategy.should_save(eval_result)
            if should_save:
                self.save_model(self.get_output_path(self.BEST_MODEL_NAME))

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

    def cleanup(self) -> None:
        """
        Free memory associated with accelerator.
        :return: None
        """
        super().cleanup()
        if self.accelerator:  # covers custom and non-custom
            self.accelerator.free_memory()

    def _initialize_state(self, model: PreTrainedModel) -> None:
        """
        Initializes accelerator and related entities.
        :param model: The model used to initialize the optimizer.
        :return: None
        """
        self.accelerator = Accelerator()
        self.optimizer = self.trainer_args.optimizer_constructor(model.parameters())
        self.lr_scheduler = self.trainer_args.scheduler_constructor(self.optimizer)

    def _prepare_accelerator(self, model: PreTrainedModel, data_loader: DataLoader) \
            -> Tuple[PreTrainedModel, Optimizer, _LRScheduler, DataLoader]:
        """
        Prepares the model, optimizer, scheduler and data loader for distributed training.
        :param model: The model being trained.
        :param data_loader: The data loader containing training data.
        :return: Prepared model, optimizer, scheduler, and data loader.
        """
        if self.accelerator is None:
            self._initialize_state(model)

        return self.accelerator.prepare(model,
                                        self.optimizer,
                                        self.lr_scheduler,
                                        data_loader)

    @overrides(Trainer)
    def _get_train_sampler(self) -> Optional[torch.utils.data.Sampler]:
        """
        Gets the data sampler used for training
        :return: the train sampler
        """
        if self.trainer_args.use_balanced_batches and self.train_dataset is not None:
            return BalancedBatchSampler(data_source=self.train_dataset, batch_size=self._train_batch_size)
        return super()._get_train_sampler()
