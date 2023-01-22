from typing import Optional, Tuple

import torch
from accelerate import Accelerator, memory_utils
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import PreTrainedModel, Trainer
from transformers.modeling_outputs import SequenceClassifierOutput

from config.override import overrides
from data.datasets.data_key import DataKey
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from models.model_manager import ModelManager
from train.trace_output.trace_train_output import TraceTrainOutput
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs


class CustomTrainer(TraceTrainer):
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
        self.model.to(device)
        inner_training_loop = memory_utils.find_executable_batch_size(self._inner_custom_training_loop)
        return inner_training_loop(resume_from_checkpoint=resume_from_checkpoint, accelerator=accelerator, device=device)

    def _inner_custom_training_loop(self, batch_size: int = None, accelerator: Accelerator = None, device: torch.device = None,
                                    resume_from_checkpoint: Optional[str] = None, **kwargs) -> TraceTrainOutput:
        """
        Trains model for the epochs specified in training arguments.
        :param batch_size: The batch size of the training step.
        :param accelerator: The accelerator used to perform distributed training of the model.
        :param device: The primary device to storage model.
        :param kwargs: Any additional arguments. Currently, ignored but necessary for finding optimal batch size.
        :return: The output of the training session.
        """

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

        for epoch_index in range(self.trainer_args.num_train_epochs):
            for batch_index, batch in enumerate(tqdm(train_data_loader)):
                batch = batch.to(device)
                optimizer.zero_grad()

                labels = batch.pop(DataKey.LABELS_KEY)
                output: SequenceClassifierOutput = model(**batch)
                loss = loss_function(output.logits, labels)

                accelerator.backward(loss)
                optimizer.step()
                self.on_step(global_step)
                training_loss += loss.item()
                global_step += 1

            scheduler.step()
            self.on_epoch(epoch_index)

        return TraceTrainOutput(global_step=global_step, training_loss=training_loss, metrics=training_metrics,
                                eval_metrics=save_strategy.stage_evaluations)

    def create_or_load_state(self, model: PreTrainedModel, data_loader: DataLoader,
                             resume_from_checkpoint: Optional[str] = None) -> Tuple[
        PreTrainedModel, Optimizer, _LRScheduler, DataLoader]:
        """
        If checkpoint given, accelerate entities are instantiated with their previous state. Otherwise, they are instantiated with new
        states.
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
            output_dir = self.trainer_args.output_dir
        super().save_model(output_dir=output_dir, _internal_call=_internal_call)
        self.accelerator.save_state(output_dir)

    def _initialize_state(self, model: PreTrainedModel) -> None:
        """
        Initializes accelerator and related entities.
        :param model: The model used to initialize the optimizer.
        :return: None
        """
        self.accelerator = Accelerator()
        self.optimizer = self.trainer_args.optimizer_constructor(model.parameters())
        self.lr_scheduler = self.trainer_args.scheduler_constructor(self.optimizer)

    def _prepare_accelerator(self, model: PreTrainedModel, data_loader: DataLoader) -> Tuple[
        PreTrainedModel, Optimizer, _LRScheduler, DataLoader]:
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
