from abc import ABC, abstractmethod
from typing import Iterable, List

import torch
from sentence_transformers import InputExample
from torch import optim
from torch.nn import Parameter
from tqdm import tqdm
from transformers.trainer_utils import EvalPrediction, PredictionOutput, TrainOutput

from tgen.common.constants.hugging_face_constants import DEFAULT_MAX_STEPS_BEFORE_EVAL
from tgen.common.logging.logger_manager import logger
from tgen.common.util.list_util import ListUtil
from tgen.common.util.override import overrides
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.core.trainers.st.balanced_batch_sampler import BalancedBatchSampler
from tgen.core.trainers.st.sentence_transformer_evaluator import SentenceTransformerEvaluator
from tgen.core.trainers.st.st_utilities import to_input_examples
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType, ModelTask


class SentenceTransformerTrainer(HuggingFaceTrainer, ABC):
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
        self.max_score = None

    @overrides(HuggingFaceTrainer)
    def train(self, **kwargs) -> TrainOutput:
        """
        Trains a sentence transformer model.
        :param kwargs: Currently ignored. TODO: add ability to start from checkpoint.
        :return: None
        """
        train_examples = to_input_examples(self.train_dataset, use_scores=self.trainer_args.use_scores, model=self.model)
        train_batch_sampler = BalancedBatchSampler(train_examples, batch_size=self.args.train_batch_size)

        evaluator = SentenceTransformerEvaluator(self, self.evaluation_roles) if self.has_dataset(DatasetRole.VAL) else None
        optimizer = optim.Adam(self.get_parameters(), lr=0.001)
        epochs = int(self.args.num_train_epochs)
        logger.info(f"Epochs: {epochs}")

        self.on_setup()

        for epoch in range(epochs):
            epoch_loss = 0
            for i in tqdm(range(len(train_batch_sampler)), desc="Training model...."):
                self.before_step()
                batch_indices = next(train_batch_sampler)
                batch_examples = [train_examples[i] for i in batch_indices]
                sentence_pairs: List[List[str]] = [b.texts for b in batch_examples]
                labels = torch.tensor([float(b.label) for b in batch_examples])

                optimizer.zero_grad()  # Clear gradients

                # Process each sentence pair
                predictions = self.calculate_predictions(sentence_pairs)

                # Calculate loss
                loss = self.compute_loss(scores=predictions, labels=labels)

                loss.backward()  # Back-propagate and update weights
                optimizer.step()
                epoch_loss += loss.item()
                self.state.total_flos += loss.item()
                self.state.global_step += 1
                self.after_step()

            logger.info(f"Training Loss: {epoch_loss}")
            self.evaluation_step(evaluator)

        return TrainOutput(metrics={}, training_loss=self.state.total_flos, global_step=self.state.global_step)

    def evaluation_step(self, evaluator: SentenceTransformerEvaluator, **kwargs):
        epoch_score = evaluator(**kwargs)
        if self.max_score is None or epoch_score > self.max_score:
            self.max_score = epoch_score
            self.save()

    @overrides(HuggingFaceTrainer)
    def predict(self, dataset_role: DatasetRole, **kwargs) -> PredictionOutput:
        """
        Predicts on the dataset given.
        :param dataset_role: Role of dataset to predict on.
        :return: Prediction output containing similarity scores as predictions.
        """
        self._current_eval_role = dataset_role
        dataset = self._get_dataset(dataset_role)
        input_examples = to_input_examples(dataset)
        scores, labels = self.calculate_similarities(input_examples)
        prediction_metrics = self._compute_validation_metrics(EvalPrediction(scores, labels))
        prediction_metrics["loss"] = self.compute_loss(scores, labels, input_examples).item()
        return PredictionOutput(scores, labels, prediction_metrics)

    def calculate_similarities(self, input_examples: List[InputExample]):
        predictions = []
        labels = []

        texts = [t for example in input_examples for t in example.texts]
        embeddings_manager = self.create_embedding_manager(texts)

        batches = ListUtil.batch(input_examples, self.args.eval_batch_size)
        for batch in tqdm(batches, desc="Computing predictions..."):
            batch_sentence_pairs = [i.texts for i in batch]
            batch_labels = [i.label for i in batch]
            batch_prediction = self.calculate_predictions(batch_sentence_pairs, embeddings_manager).tolist()
            predictions.extend(batch_prediction)
            labels.extend(batch_labels)

        predictions = torch.tensor(predictions)
        labels = torch.tensor(labels)
        return predictions, labels

    def create_embedding_manager(self, texts: List[str]) -> EmbeddingsManager:
        """
        Creates embedding manager for given texts.
        :param texts: The texts to create embeddings for.
        :return: The embeddings manager.
        """
        texts = set(texts)
        embeddings_manager = EmbeddingsManager.create_from_content(texts, model=self.model,
                                                                   embedding_kwargs={"convert_to_tensor": True})
        return embeddings_manager

    def calculate_predictions(self, sentence_pairs: List[List[str]], embedding_model_manager: EmbeddingsManager = None):
        """
        Predictions similarity scores between sentences pairs from their embeddings.
        :param sentence_pairs: The sentence pairs to calculate predictions for.
        :param embedding_model_manager: Manager used to retrieve / create embeddings
        :return:
        """
        source_sentences = [s[0] for s in sentence_pairs]
        target_sentences = [s[1] for s in sentence_pairs]

        if embedding_model_manager:
            source_embeddings = embedding_model_manager.get_embeddings(source_sentences)
            target_embeddings = embedding_model_manager.get_embeddings(target_sentences)

            source_embeddings = torch.stack(source_embeddings)
            target_embeddings = torch.stack(target_embeddings)
        elif self.model:
            source_embeddings = self.model.encode(source_sentences, convert_to_tensor=True)
            target_embeddings = self.model.encode(target_sentences, convert_to_tensor=True)
        else:
            raise Exception("")

        predictions = self.calculate_similarity_scores(source_embeddings, target_embeddings)
        return predictions

    @abstractmethod
    def calculate_similarity_scores(self, source_embeddings: torch.Tensor, target_embeddings: torch.Tensor):
        """
        Calculates the similarity scores between source and target embeddings.
        :param source_embeddings: The source embeddings.
        :param target_embeddings: The target embeddings.
        :return: Tensor containing similarity scores.
        """
        pass

    @abstractmethod
    def get_parameters(self) -> Iterable[Parameter]:
        """
        :return: Returns parameters to optimize.
        """

    @abstractmethod
    def compute_loss(self, scores: torch.Tensor, labels: torch.Tensor, input_examples: List[InputExample] = None) -> torch.Tensor:
        """
        Computes the loss of given examples.
        :param scores: Optional scores assigned to each input example.
        :param labels: Labels associated with each example.
        :param input_examples: The original examples, used to calculate different features if necessary.
        :return:
        """
        pass

    @abstractmethod
    def save(self):
        """
        Saves the current model
        :param self:
        :return:
        """

    def on_setup(self):
        pass

    def before_step(self):
        pass

    def after_step(self):
        pass
