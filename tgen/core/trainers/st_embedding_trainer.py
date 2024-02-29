from typing import Iterable, List

import torch
from sentence_transformers import InputExample
from torch import cosine_similarity
from torch.nn import Parameter

from tgen.common.logging.logger_manager import logger
from tgen.common.util.list_util import ListUtil
from tgen.common.util.override import overrides
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.common.util.tf_util import move_input_to_device
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trainers.st.st_loss_functions import SupportedSTLossFunctions
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
    def get_trainable_parameters(self) -> Iterable[Parameter]:
        """
        :return: Returns the embedding model's parameters.
        """
        return self.model.parameters()

    @overrides(STTrainer)
    def compute_loss(self, scores: torch.Tensor, labels: torch.Tensor, input_examples: List[InputExample] = None) -> torch.Tensor:
        """
        Computes the loss between the input examples.
        :param scores: The models predictions for input examples.
        :param labels: The labels associated with input examples.
        :param input_examples: The input examples.
        :return: The loss for given predictions.
        """
        model_device = self.loss_function.model._target_device
        batches = ListUtil.batch(input_examples, self.trainer_args.per_device_eval_batch_size)
        loss_fnc = self.loss_function.to(model_device)

        loss = torch.tensor(0.0)
        for batch in ListUtil.selective_tqdm(batches, desc="Calculating loss.."):
            features, labels = self.model.smart_batching_collate(batch)
            features, labels = move_input_to_device(model_device, features, labels)
            loss += loss_fnc(features, labels)
        return loss

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
        loss_function_name = self.trainer_args.st_loss_function
        loss_function_kwargs = {}
        possible_params = {"size_average": False, "margin": 0.1}
        loss_function_class = SupportedSTLossFunctions.get_value(loss_function_name)
        for param, param_value in possible_params.items():
            if ReflectionUtil.has_constructor_param(loss_function_class, param):
                loss_function_kwargs[param] = param_value

        loss_function = loss_function_class(self.model, **loss_function_kwargs)
        logger.info(f"Created loss function {loss_function_name}.")
        return loss_function
