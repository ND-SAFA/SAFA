from typing import List

import torch
from common_resources.llm.args.hugging_face_args import HuggingFaceArgs
from common_resources.tools.util.override import overrides
from common_resources.tools.util.tf_util import TFUtil
from sentence_transformers import InputExample
from torch import cosine_similarity

from tgen.core.trainers.st_loss_functions import SupportedSTLossFunctions
from tgen.core.trainers.st_trainer import STTrainer
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType, ModelTask


class STEmbeddingTrainer(STTrainer):
    """
    Trains sentence transformer models. They have a slightly modified API for training the models and loading the data.
    """

    def __init__(self, trainer_args: HuggingFaceArgs, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager,
                 **kwargs):
        """
        Trainer for sentence transformer models. Provides API that allows training and prediction operations.
        :param trainer_args: The trainer arguments.
        :param model_manager: The model manager container sentence transformer.
        :param trainer_dataset_manager: Contains the datasets used for training, validation, and evaluation.
        :param max_steps_before_eval: The maximum number of training steps that are allowed before evaluating.
        :param loss_function: The loss function to use while training model.
        :param save_best_model: Whether to save the best model. Defaults to true
        :param kwargs: Additional keyword arguments passed to parent trainer.
        """
        model_manager.model_task = ModelTask.SBERT
        model_manager.arch_type = ModelArchitectureType.SIAMESE
        super().__init__(trainer_args, model_manager, trainer_dataset_manager, **kwargs)
        self.loss_function = None
        self.loss_function = self._create_loss_function()
        self.starting_learning_rate = 5e-5
        self.ending_learning_rate = 5e-9

    @overrides(STTrainer)
    def calculate_similarity_scores(self, source_embeddings: torch.Tensor, target_embeddings: torch.Tensor) -> torch.Tensor:
        """
        Computes the similarity scores between source and target embeddings.
        :param source_embeddings: The source embeddings.
        :param target_embeddings: The target embeddings.
        :return: Tensor containing similarity scores.
        """
        similarity_scores = cosine_similarity(source_embeddings, target_embeddings)
        return similarity_scores

    @overrides(STTrainer)
    def compute_loss(self, scores: torch.Tensor, labels: torch.Tensor, input_examples: List[InputExample] = None) -> torch.Tensor:
        """
        Computes the loss between the input examples.
        :param scores: The models predictions for input examples.
        :param labels: The labels associated with input examples.
        :param input_examples: The input examples.
        :return: The loss for given predictions.
        """
        loss = self.loss_function(scores, labels)
        return loss

    @overrides(STTrainer)
    def move_training_modules(self, device: torch.device) -> None:
        """
        :param device: The device to move the training modules to.
        :return: Returns list of modules to move to device before training.
        """
        self.loss_function = self.loss_function.to(device)

    @overrides(STTrainer)
    def save(self) -> None:
        """
        Saves the current embedding model.
        :return: None
        """
        self.model.save(self.args.output_dir)

    def _create_loss_function(self):
        """
        Creates the loss function from its defined class.
        :return: The loss function.
        """
        # using MLP losses because it's assumed that embeddings will always be compared via cosine similarity.
        return TFUtil.create_loss_function(SupportedSTLossFunctions, self.trainer_args.st_loss_function, "mse")
