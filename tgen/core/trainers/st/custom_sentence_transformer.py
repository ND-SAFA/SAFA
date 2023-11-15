import logging
from typing import Callable, Dict, Iterable, List, Tuple, Type

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import SentenceEvaluator
from torch import nn
from torch.nn import Module
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm

from tgen.core.trainers.st.training_data import TrainingData, TrainingDataParams

logger = logging.getLogger(__name__)


class CustomSentenceTransformer(SentenceTransformer):
    def fit(
            self,
            train_objectives: Iterable[Tuple[DataLoader, nn.Module]],
            evaluator: SentenceEvaluator = None,
            epochs: int = 1,
            steps_per_epoch=None,
            scheduler: str = "WarmupLinear",
            warmup_steps: int = 10000,
            optimizer_class: Type[Optimizer] = torch.optim.AdamW,
            optimizer_params: Dict[str, object] = {"lr": 2e-5},
            weight_decay: float = 0.01,
            evaluation_steps: int = 0,
            output_path: str = None,
            save_best_model: bool = True,
            max_grad_norm: float = 1,
            use_amp: bool = False,
            callback: Callable[[float, int, int], None] = None,
            show_progress_bar: bool = True,
            checkpoint_path: str = None,
            checkpoint_save_steps: int = 500,
            checkpoint_save_total_limit: int = 0,
            accumulation_steps: int = 1
    ):
        """
        Train the model with the given training objective
        Each training objective is sampled in turn for one batch.
        We sample only as many batches from each objective as there are in the smallest one
        to make sure of equal training with each dataset.

        :param train_objectives: Tuples of (DataLoader, LossFunction). Pass more than one for multi-task learning
        :param evaluator: An evaluator (sentence_transformers.evaluation) evaluates the model performance during training on held-out dev data. It is used to determine the best model that is saved to disc.
        :param epochs: Number of epochs for training
        :param steps_per_epoch: Number of training steps per epoch. If set to None (default), one epoch is equal the DataLoader size from train_objectives.
        :param scheduler: Learning rate scheduler. Available schedulers: constantlr, warmupconstant, warmuplinear, warmupcosine, warmupcosinewithhardrestarts
        :param warmup_steps: Behavior depends on the scheduler. For WarmupLinear (default), the learning rate is increased from o up to the maximal learning rate. After these many training steps, the learning rate is decreased linearly back to zero.
        :param optimizer_class: Optimizer
        :param optimizer_params: Optimizer parameters
        :param weight_decay: Weight decay for model parameters
        :param evaluation_steps: If > 0, evaluate the model using evaluator after each number of training steps
        :param output_path: Storage path for the model and evaluation files
        :param save_best_model: If true, the best model (according to evaluator) is stored at output_path
        :param max_grad_norm: Used for gradient normalization.
        :param use_amp: Use Automatic Mixed Precision (AMP). Only for Pytorch >= 1.6.0
        :param callback: Callback function that is invoked after each evaluation.
                It must accept the following three parameters in this order:
                `score`, `epoch`, `steps`
        :param show_progress_bar: If True, output a tqdm progress bar
        :param checkpoint_path: Folder to save checkpoints during training
        :param checkpoint_save_steps: Will save a checkpoint after so many steps
        :param checkpoint_save_total_limit: Total number of checkpoints to store
        """

        # Prepare optimizers
        training_params = TrainingDataParams(evaluator=evaluator,
                                             epochs=epochs,
                                             scheduler_name=scheduler,
                                             warmup_steps=warmup_steps,
                                             optimizer_class=optimizer_class,
                                             optimizer_params=optimizer_params,
                                             weight_decay=weight_decay,
                                             output_path=output_path,
                                             max_grad_norm=max_grad_norm,
                                             use_amp=use_amp,
                                             checkpoint_path=checkpoint_path,
                                             checkpoint_save_steps=checkpoint_save_steps,
                                             checkpoint_save_total_limit=checkpoint_save_total_limit,
                                             accumulation_steps=accumulation_steps
                                             )
        for dataloader, _ in train_objectives:  # Use smart batching
            dataloader.collate_fn = self.smart_batching_collate

        training_data = TrainingData(training_objectives=train_objectives, params=training_params)
        loss_models = training_data.models

        # Add info to model card
        model_card_text = training_data.get_model_card_training_info()
        self._model_card_text = None
        self._model_card_vars["{TRAINING_SECTION}"] = model_card_text

        self.best_score = -9999999

        self.to(self._target_device)
        for loss_model in loss_models:
            loss_model.to(self._target_device)

        if steps_per_epoch is None:
            steps_per_epoch = training_data.get_epoch_steps()

        training_iterations = [(epoch + 1, step + 1) for epoch in range(epochs) for step in range(steps_per_epoch)]

        for epoch, training_step in tqdm(training_iterations, "Training model..."):
            if training_step == 1:
                self.pre_epoch(training_data)

            self.pre_step(training_data)

            training_data.perform_training_step(training_step, self._target_device)

            if evaluation_steps > 0 and training_step % evaluation_steps == 0:
                self._eval_during_training(evaluator, output_path, save_best_model, epoch, training_step, callback)
                self._init_loss_models(loss_models)

            self.post_step(training_data)

            if training_step == steps_per_epoch:
                self._eval_during_training(evaluator, output_path, save_best_model, epoch, -1, callback)
                self.post_epoch(training_data)

        self.post_training(training_data)

    def pre_step(self, training_data: TrainingData) -> None:
        """
        Handler called before each training step
        :return:  None
        """

    def post_step(self, training_data: TrainingData) -> None:
        """
        Called after each training step.
        :param training_data: Data representing state of current training.
        :return: None
        """
        if training_data.params.is_checkpoint_time():
            self._save_checkpoint(training_data.params.checkpoint_path,
                                  training_data.params.checkpoint_save_total_limit,
                                  training_data.params.global_step)

    def pre_epoch(self, training_data: TrainingData) -> None:
        """
        Called before each epoch.
        :param training_data: Data representing state of current training.
        :return: None
        """
        self._init_loss_models(training_data.models)
        training_data.initialize_data_iterators()

    def post_epoch(self, training_data: TrainingData) -> None:
        """
        Called after each epoch.
        :param training_data: Data representing state of current training.
        :return: None
        """

    def post_training(self, training_data: TrainingData) -> None:
        """
        Called after all training steps have been completed.
        :param training_data: Data representing state of current training.
        :return: None
        """
        if training_data.params.should_save_final_model():
            self.save(training_data.params.output_path)

        if training_data.params.checkpoint_path is not None:
            self._save_checkpoint(training_data.params.checkpoint_path,
                                  training_data.params.checkpoint_save_total_limit,
                                  training_data.params.global_step)

    @staticmethod
    def _init_loss_models(loss_models: List[Module]) -> None:
        """
        Initializes models for training by setting loss to 0 and setting them for training.
        :param loss_models: The models to initialize.
        :return: None
        """
        for loss_model in loss_models:
            loss_model.zero_grad()
            loss_model.train()
