import os
from typing import Iterable

import torch
from torch import nn
from torch.nn import Parameter

from tgen.common.constants.hugging_face_constants import DEFAULT_MAX_STEPS_BEFORE_EVAL
from tgen.common.util.override import overrides
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trainers.st.st_mlp import MLP
from tgen.core.trainers.st.tensor_utilities import freeze
from tgen.core.trainers.st_trainer import SentenceTransformerTrainer
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType, ModelTask


class SentenceTransformerTrainerMLP(SentenceTransformerTrainer):
    """
    Trains sentence transformer models. They have a slightly modified API for training the models and loading the data.
    """

    def __init__(self, trainer_args: HuggingFaceArgs, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager,
                 max_steps_before_eval: int = DEFAULT_MAX_STEPS_BEFORE_EVAL, **kwargs):
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
        self.min_eval_steps = max_steps_before_eval
        self.loss_function = nn.MSELoss()
        self.mlp = MLP.build(self.model, [512, 256], nn.ReLU)
        self.max_score = None
        self.model_output_path = os.path.join(self.args.output_dir, "model.pt")
        freeze(self.model)

    @overrides(SentenceTransformerTrainer)
    def calculate_similarity_scores(self, source_embeddings: torch.Tensor, target_embeddings: torch.Tensor):
        """
        Calculates the similarity scores between the source and target embeddings.
        :param source_embeddings: Tensor of source embeddings of size (batch_size, features...)
        :param target_embeddings: Tensor of target embeddings of size (batch_size, features...)
        :return: Tensor of size (batch_size, )
        """
        combined_embeddings = torch.cat((source_embeddings, target_embeddings), dim=1)
        prediction = self.mlp(combined_embeddings)  # Add batch dimension
        return torch.sigmoid(prediction).squeeze()  # Keep as tensor

    @overrides(SentenceTransformerTrainer)
    def get_trainable_parameters(self) -> Iterable[Parameter]:
        """
        :return: Returns the parameters of the MLP.
        """
        return self.mlp.parameters()

    @overrides(SentenceTransformerTrainer)
    def compute_loss(self, scores, labels, *args, **kwargs) -> torch.Tensor:
        """
        Computes the loss between the scores and labels.
        :param scores: The scores predicted by the MLP.
        :param labels: The labels associated with each score.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword-arguments.
        :return: The loss tensor.
        """
        loss = self.loss_function(scores, labels)
        return loss

    @overrides(SentenceTransformerTrainer)
    def save(self):
        """
        Saves MLP at model_output_path.
        :return:
        """
        torch.save(self.mlp, self.model_output_path)
