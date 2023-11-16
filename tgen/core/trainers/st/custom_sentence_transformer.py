import logging
from typing import Iterable, List, Tuple

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import batch_to_device
from torch import nn
from torch.nn import Module
from torch.utils.data import DataLoader
from tqdm import tqdm

from tgen.common.constants.logging_constants import TQDM_NCOLS
from tgen.core.trainers.st.constants import DEFAULT_BEST_SCORE, STARTING_STEP, TRAINING_SECTION_KEY
from tgen.core.trainers.st.training_data import STTrainingManager, STTrainingParams
from tgen.core.wandb.WBManager import WBManager

logger = logging.getLogger(__name__)


class CustomSentenceTransformer(SentenceTransformer):
    def fit(
            self,
            train_objectives: Iterable[Tuple[DataLoader, nn.Module]],
            training_params: STTrainingParams,
            *args, **kwargs
    ):
        """
        Train the model with the given training objective
        :param training_params: The training parameters to run loop on.
        """

        training_manager = STTrainingManager(training_objectives=train_objectives, params=training_params)
        steps_per_epoch = training_manager.get_epoch_steps()

        self.on_pre_training(training_manager)

        for epoch, training_step in tqdm(training_manager.get_training_iterator(), "Training model...", ncols=TQDM_NCOLS):
            if training_step == STARTING_STEP:
                self.on_pre_epoch(training_manager)

            self.on_pre_step(epoch, training_step, training_manager)
            self.perform_training_step(training_manager, training_step)
            self.on_post_step(epoch, training_step, training_manager)

            if training_step == steps_per_epoch:
                self.on_post_epoch(epoch, training_manager)

        self.on_post_training(training_manager)

    def perform_training_step(self, training_manager: STTrainingManager, training_step: int) -> None:
        """
        Performs a training step.
        :param training_manager: Manager containing models, objectives, and data.
        :param training_step: The current training step.
        :return:
        """
        if training_manager.data_iterators is None:
            training_manager.initialize_data_iterators()

        for train_idx in range(len(training_manager.models)):
            loss_model = training_manager.models[train_idx]
            optimizer = training_manager.optimizers[train_idx]
            scheduler = training_manager.schedulers[train_idx]
            data_iterator = training_manager.data_iterators[train_idx]

            data = next(data_iterator)

            features, labels = data
            labels = labels.to(self._target_device)
            features = list(map(lambda batch: batch_to_device(batch, self._target_device), features))

            loss_value = loss_model(features, labels)
            WBManager.log(metrics={"training_loss": loss_value.item()}, step=training_manager.params.global_step)
            loss_value /= training_manager.params.accumulation_steps
            loss_value.backward()

            if training_step % training_manager.params.accumulation_steps == 0:
                torch.nn.utils.clip_grad_norm_(loss_model.parameters(), training_manager.params.max_grad_norm)
                optimizer.step()
                optimizer.zero_grad()

            scheduler.step()

        training_manager.params.global_step += 1

    def on_pre_step(self, epoch: int, training_step: int, training_data: STTrainingManager) -> None:
        """
        Handler called before each training step.
        :param epoch: The epoch of the training session.
        :param training_step: The current training step in epoch.
        :param training_data: The training data containing state of training loop.
        :return:  None
        """

    def on_post_step(self, epoch: int, training_step: int, training_data: STTrainingManager) -> None:
        """
        Called after each training step.
         :param epoch: The epoch of the training session.
        :param training_step: The current training step in epoch.
        :param training_data: The training data containing state of training loop.
        :return: None
        """
        params = training_data.params
        evaluation_steps = params.evaluation_steps
        if evaluation_steps > 0 and training_step % evaluation_steps == 0:
            self._eval_during_training(params.evaluator,
                                       params.output_path,
                                       params.save_best_model,
                                       epoch,
                                       training_step,
                                       params.callback)
            self._init_loss_models(training_data.models)
        if training_data.params.is_checkpoint_time():
            self._save_checkpoint(training_data.params.checkpoint_path,
                                  training_data.params.checkpoint_save_total_limit,
                                  training_data.params.global_step)

    def on_pre_epoch(self, training_data: STTrainingManager) -> None:
        """
        Called before each epoch.
        :param training_data: Data representing state of current training.
        :return: None
        """
        self._init_loss_models(training_data.models)
        training_data.initialize_data_iterators()

    def on_post_epoch(self, epoch: int, training_data: STTrainingManager) -> None:
        """
        Called after each epoch.
        :param epoch: The epoch of the training loop.
        :param training_data: Data representing state of current training.
        :return: None
        """
        params = training_data.params
        self._eval_during_training(params.evaluator,
                                   params.output_path,
                                   params.save_best_model,
                                   epoch,
                                   -1,
                                   params.callback)

    def on_pre_training(self, training_manager: STTrainingManager) -> None:
        """
        Handler called before training begins.
        :param training_manager: The state of the training loop.
        :return:None
        """
        model_card_text = training_manager.get_model_card_training_info()
        self._model_card_text = None
        self._model_card_vars[TRAINING_SECTION_KEY] = model_card_text
        self.best_score = DEFAULT_BEST_SCORE
        self.to(self._target_device)
        for loss_model in training_manager.models:
            loss_model.to(self._target_device)
        for dataloader in training_manager.data_loaders:  # Use smart batching
            dataloader.collate_fn = self.smart_batching_collate

    def on_post_training(self, training_manager: STTrainingManager) -> None:
        """
        Called after all training steps have been completed.
        :param training_manager: State of the training loop.
        :return: None
        """
        if training_manager.params.should_save_final_model():
            self.save(training_manager.params.output_path)

        if training_manager.params.checkpoint_path is not None:
            self._save_checkpoint(training_manager.params.checkpoint_path,
                                  training_manager.params.checkpoint_save_total_limit,
                                  training_manager.params.global_step)

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
