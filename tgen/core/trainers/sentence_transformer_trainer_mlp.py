import os
from typing import List

import torch
from sentence_transformers import InputExample, SentenceTransformer
from torch import nn, optim
from tqdm import tqdm
from transformers.trainer_utils import TrainOutput

from tgen.common.constants.hugging_face_constants import DEFAULT_MAX_STEPS_BEFORE_EVAL
from tgen.common.logging.logger_manager import logger
from tgen.common.util.list_util import ListUtil
from tgen.common.util.override import overrides
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trainers.sentence_transformer_trainer import SentenceTransformerTrainer
from tgen.core.trainers.st.balanced_batch_sampler import BalancedBatchSampler
from tgen.core.trainers.st.sentence_transformer_evaluator import SentenceTransformerEvaluator
from tgen.core.trainers.st.st_mlp import MLP
from tgen.core.trainers.st.tensor_utilities import freeze
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.embeddings.embeddings_manager import EmbeddingsManager
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
        self.loss_function = nn.MSELoss
        self.mlp = MLP.build(self.model, [512, 256], nn.ReLU)
        self.max_score = None
        self.model_output_path = os.path.join(self.args.output_dir, "model.pt")
        freeze(self.model)

    @overrides(SentenceTransformerTrainer)
    def train(self, **kwargs) -> TrainOutput:
        """
        Trains a sentence transformer model.
        :param kwargs: Currently ignored. TODO: add ability to start from checkpoint.
        :return: None
        """
        train_examples = self.to_input_examples(self.train_dataset, use_scores=self.trainer_args.use_scores, model=self.model)
        train_batch_sampler = BalancedBatchSampler(train_examples, batch_size=self.args.train_batch_size)

        evaluator = SentenceTransformerEvaluator(self, self.evaluation_roles) if self.has_dataset(DatasetRole.VAL) else None
        criterion = nn.MSELoss()  # extract loss and optimizer as params
        optimizer = optim.Adam(self.mlp.parameters(), lr=0.001)
        epochs = int(self.args.num_train_epochs)
        logger.info(f"Epochs: {epochs}")

        for epoch in range(epochs):
            epoch_loss = 0
            for i in tqdm(range(len(train_batch_sampler)), desc="Training model...."):
                batch_indices = next(train_batch_sampler)
                batch = [train_examples[i] for i in batch_indices]
                sentence_pairs: List[List[str]] = [b.texts for b in batch]
                labels = torch.tensor([float(b.label) for b in batch])

                optimizer.zero_grad()  # Clear gradients

                # Process each sentence pair
                predictions = self._predict_similarity(self.mlp, sentence_pairs, embedding_model=self.model)

                # Calculate loss
                loss = criterion(predictions, labels)

                loss.backward()  # Backpropagate and update weights
                optimizer.step()
                epoch_loss += loss.item()
                self.state.global_step += 1

            logger.info(f"Training Loss: {epoch_loss}")
            self.evaluation_step(evaluator)

        return TrainOutput(metrics={}, training_loss=self.total_loss, global_step=self.state.global_step)

    def evaluation_step(self, evaluator: SentenceTransformerEvaluator, **kwargs):
        epoch_score = evaluator(**kwargs)
        if self.max_score is None or epoch_score > self.max_score:
            self.max_score = epoch_score
            self.save()

    def save(self):
        torch.save(self.mlp, self.model_output_path)

    @overrides(SentenceTransformerTrainer)
    def calculate_similarities(self, model: SentenceTransformer, input_examples: List[InputExample]):
        predictions = []
        labels = []

        # create embedding mamanger
        texts = [t for example in input_examples for t in example.texts]
        texts = set(texts)
        embeddings_manager = EmbeddingsManager.create_from_content(texts, model=self.model,
                                                                   embedding_kwargs={"convert_to_tensor": True})

        batches = ListUtil.batch(input_examples, self.args.eval_batch_size)
        for batch in tqdm(batches, desc="Computing predictions..."):
            batch_sentence_pairs = [i.texts for i in batch]
            batch_labels = [i.label for i in batch]
            batch_prediction = self._predict_similarity(self.mlp, batch_sentence_pairs,
                                                        embedding_model_manager=embeddings_manager).tolist()
            predictions.extend(batch_prediction)
            labels.extend(batch_labels)
        return predictions, labels

    @overrides(SentenceTransformerTrainer)
    def compute_internal_loss(self, scores, labels, input_examples: List[InputExample]):
        scores = torch.tensor(scores)
        labels = torch.tensor(labels)
        criterion = nn.MSELoss()
        loss = criterion(scores, labels).item()
        return loss

    @staticmethod
    def _predict_similarity(mlp: nn.Module, sentence_pairs: List[List[str]], embedding_model: SentenceTransformer = None,
                            embedding_model_manager: EmbeddingsManager = None):
        """
        Predictions similarity scores between sentences pairs from their embeddings.
        :param embedding_model: The model used to create the embeddings.
        :param embedding_model_manager: Manager used to retrieve / create embeddings
        :param mlp: The NN resposible for calculating a similarity scores between the sentence pairs.
        :param sentence_pairs:
        :return:
        """
        source_sentences = [s[0] for s in sentence_pairs]
        target_sentences = [s[1] for s in sentence_pairs]

        if embedding_model:
            source_embeddings = embedding_model.encode(source_sentences, convert_to_tensor=True)
            target_embeddings = embedding_model.encode(target_sentences, convert_to_tensor=True)
        elif embedding_model_manager:
            source_embeddings = embedding_model_manager.get_embeddings(source_sentences)
            target_embeddings = embedding_model_manager.get_embeddings(target_sentences)

            source_embeddings = torch.stack(source_embeddings)
            target_embeddings = torch.stack(target_embeddings)
        else:
            raise Exception("")

        # Concatenate embeddings
        combined_embeddings = torch.cat((source_embeddings, target_embeddings), dim=1)

        # Pass through MLP
        prediction = mlp(combined_embeddings)  # Add batch dimension
        return torch.sigmoid(prediction).squeeze()  # Keep as tensor
