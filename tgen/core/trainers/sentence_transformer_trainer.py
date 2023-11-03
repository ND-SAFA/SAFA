from typing import Dict, List, Optional

import numpy as np
from datasets import Dataset
from sentence_transformers import InputExample, SentenceTransformer
from sentence_transformers.evaluation import SentenceEvaluator
from sentence_transformers.losses import ContrastiveLoss, CosineSimilarityLoss
from sklearn.metrics.pairwise import cosine_similarity
from torch.utils.data import DataLoader
from transformers.trainer_utils import PredictionOutput, TrainOutput

from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.override import overrides
from tgen.common.util.supported_enum import SupportedEnum
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType, ModelTask

SEPARATOR_BAR = "-" * 50
EmbeddingType = np.array  # TODO: Merge with embedding type.

DEFAULT_EVAL_METRIC = "map"
DEFAULT_MAX_STEPS_BEFORE_EVAL = 50


class SupportedLossFunctions(SupportedEnum):
    """
    Enumerates the different loss functions available for sentence embedding models.
    """
    COSINE = CosineSimilarityLoss
    CONTRASTIVE = ContrastiveLoss


class SentenceTransformerEvaluator(SentenceEvaluator):
    def __init__(self, trainer: HuggingFaceTrainer, dataset_role: DatasetRole = DatasetRole.VAL,
                 evaluator_metric: str = DEFAULT_EVAL_METRIC):
        """
        Evaluates dataset under role with given trainer.
        :param trainer: The trainer used to predict on the dataset.
        :param dataset_role: The role the dataset to predict should be found under.
        """
        self.trainer = trainer
        self.dataset_role = dataset_role
        self.evaluator_metric = evaluator_metric
        self.metrics = []

    def __call__(self, model: SentenceTransformer, **kwargs) -> float:
        """
        Evaluates the model on the evaluation dataset.
        :param model: The model to evaluate.
        :param kwargs: Ignored.
        :return: The score for this evaluation run.
        """
        prediction_output: TracePredictionOutput = self.trainer.perform_prediction(self.dataset_role)
        logger.info(SEPARATOR_BAR)
        metrics = prediction_output.metrics
        self.metrics.append(metrics)
        return metrics[self.evaluator_metric]


class SentenceTransformerTrainer(HuggingFaceTrainer):
    """
    Trains sentence transformer models. They have a slightly modified API for training the models and loading the data.
    """

    def __init__(self, trainer_args: HuggingFaceArgs, model_manager: ModelManager, trainer_dataset_manager: TrainerDatasetManager,
                 max_steps_before_eval: int = DEFAULT_MAX_STEPS_BEFORE_EVAL,
                 loss_function: SupportedLossFunctions = SupportedLossFunctions.COSINE, **kwargs):
        """
        Trainer for sentence transformer models. Provides API that allows training and prediction operations.
        :param trainer_args: The trainer arguments.
        :param model_manager: The model manager container sentence transformer.
        :param trainer_dataset_manager: Contains the datasets used for training, validation, and evaluation.
        :param max_steps_before_eval: The maximum number of training steps that are allowed before evaluating.
        :param kwargs: Additional keyword arguments passed to parent trainer.
        """
        model_manager.model_task = ModelTask.SBERT
        model_manager.arch_type = ModelArchitectureType.SIAMESE
        super().__init__(trainer_args, model_manager, trainer_dataset_manager, **kwargs)
        self.min_eval_steps = max_steps_before_eval
        self.loss_function = loss_function

    @overrides(HuggingFaceTrainer)
    def train(self, **kwargs) -> TrainOutput:
        """
        Trains a sentence transformer model.
        :param kwargs: Currently ignored. TODO: add ability to start from checkpoint.
        :return: None
        """
        logger.log_title("Starting Performance")
        self.perform_prediction(DatasetRole.VAL)

        train_dataloader = DataLoader(self.train_dataset, shuffle=True, batch_size=self.args.train_batch_size)
        train_loss = self.loss_function.value(self.model)
        n_steps = min(len(train_dataloader) + 1, self.min_eval_steps)
        evaluator = SentenceTransformerEvaluator(self)

        logger.log_title("Starting Training")
        self.model.fit(train_objectives=[(train_dataloader, train_loss)],
                       epochs=int(self.args.num_train_epochs),
                       warmup_steps=self.args.warmup_steps,
                       evaluation_steps=n_steps,
                       evaluator=evaluator)
        return TrainOutput(metrics=evaluator.metrics, training_loss=None, global_step=None)

    @overrides(HuggingFaceTrainer)
    def predict(self, test_dataset: List[InputExample], **kwargs) -> PredictionOutput:
        """
        Predicts on the dataset given.
        :param test_dataset: The dataset to predict scores for.
        :return: Prediction output containing similarity scores as predictions.
        """
        embeddings = self.create_embedding_map(self.model, test_dataset)
        return self.calculate_similarities(embeddings, test_dataset)

    @overrides(HuggingFaceTrainer)
    def _get_dataset(self, dataset_role: DatasetRole) -> Optional[Dataset]:
        """
        Returns the dataset in the given role.
        :param dataset_role: The role to retrieve.
        :return: Trainer dataset containing input examples.
        """
        return self.trainer_dataset_manager[dataset_role].to_trainer_dataset(self.model_manager)

    @staticmethod
    def create_embedding_map(model: SentenceTransformer, test_dataset: List[InputExample]):
        """
        Creates embedding map from content to embedding for texts in dataset. TODO: Replace with embedding manager.
        :param model: The model used to embed the test dataset.
        :param test_dataset: The dataset containing source and target texts per example.
        :return: Map of text to embedding.
        """
        unique_texts = list(set([a for e in test_dataset for a in e.texts]))
        batch_embeddings = model.encode(unique_texts)
        embeddings = {k: v for k, v in zip(unique_texts, batch_embeddings)}
        return embeddings

    @staticmethod
    def calculate_similarities(embedding_map: Dict[str, EmbeddingType], input_examples: List[InputExample]) -> PredictionOutput:
        """
        Calculates the cosine similarity between the texts in each input example. TODO: Replace with embedding util.
        :param embedding_map: Maps text to embedding for all input examples.
        :param input_examples: The list of input examples to calculate similarities for.
        :return: Prediction output containing scores as predictions and labels as label ids.
        """
        scores = []
        labels = []
        for example in input_examples:
            source_text, target_text = example.texts
            source_embedding = embedding_map[source_text]
            target_embedding = embedding_map[target_text]
            score = cosine_similarity([source_embedding], [target_embedding])[0][0]
            scores.append(score)
            labels.append(example.label)
        return PredictionOutput(predictions=scores, label_ids=labels, metrics={})
