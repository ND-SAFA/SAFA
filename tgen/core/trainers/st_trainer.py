from abc import ABC, abstractmethod
from typing import Iterable, List

import torch
from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.llm.args.hugging_face_args import HuggingFaceArgs
from common_resources.tools.constants.hugging_face_constants import DEFAULT_MAX_STEPS_BEFORE_EVAL
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.list_util import ListUtil
from common_resources.tools.util.math_util import MathUtil
from common_resources.tools.util.override import overrides
from common_resources.tools.util.st_util import STUtil
from common_resources.tools.util.tf_util import TFUtil
from sentence_transformers import InputExample
from torch import optim
from torch.nn import Parameter
from torch.optim import Optimizer
from torch.optim.lr_scheduler import ExponentialLR
from tqdm import tqdm
from transformers.trainer_utils import EvalPrediction, PredictionOutput, TrainOutput

from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.core.trainers.st.balanced_batch_sampler import BalancedBatchSampler
from tgen.core.trainers.st.st_evaluator import STEvaluator
from tgen.core.wb.wb_manager import WBManager
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType, ModelTask
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager


class STTrainer(HuggingFaceTrainer, ABC):
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
        self.curr_score = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.setup_complete = False
        self.starting_learning_rate = None
        self.ending_learning_rate = None

    @overrides(HuggingFaceTrainer)
    def train(self, **kwargs) -> TrainOutput:
        """
        Trains a sentence transformer model.
        :param kwargs: Currently ignored. TODO: add ability to start from checkpoint.
        :return: None
        """
        self.complete_device_setup()
        train_examples = STUtil.to_input_examples(self.train_dataset, use_scores=self.trainer_args.use_scores, model=self.model)
        train_batch_sampler = BalancedBatchSampler(train_examples, batch_size=self.args.train_batch_size)
        n_batches = len(train_batch_sampler)
        n_examples = len(self.train_dataset)

        evaluator = STEvaluator(self, self.evaluation_roles, self.trainer_args.metric_for_best_model) if self.has_dataset(
            DatasetRole.VAL) else None

        optimizer = self.setup_optimizer()
        scheduler = self.setup_scheduler(optimizer)

        epochs = int(self.args.num_train_epochs)
        logger.info(f"Total Epochs: {epochs}")
        training_metrics = []
        for epoch in range(epochs):
            logger.info(f"Starting Epoch {epoch + 1}")
            epoch_loss = 0
            self.model.train()
            for i in tqdm(range(n_batches), desc="Training model...."):
                batch_indices = next(train_batch_sampler)
                batch_examples = [train_examples[i] for i in batch_indices]
                sentence_pairs: List[List[str]] = [b.texts for b in batch_examples]
                labels = torch.tensor([float(b.label) for b in batch_examples]).to(self.device)

                optimizer.zero_grad()  # Clear gradients
                predictions = self.calculate_predictions(sentence_pairs).to(self.device)  # Process each sentence pair
                loss = self.compute_loss(scores=predictions, labels=labels, input_examples=batch_examples)
                loss.backward()  # Back-propagate and update weights
                optimizer.step()

                step_loss = loss.item()
                epoch_loss += step_loss
                self.state.total_flos += step_loss
                self.state.global_step += 1
                WBManager.log({DatasetRole.TRAIN: {"loss": step_loss, "epoch": epoch + 1}}, step=self.state.global_step)

            train_batch_sampler.reset()
            scheduler.step()
            epoch_loss /= n_examples
            logger.info(f"Average Step Loss: {epoch_loss}")
            self.evaluate_if_save(evaluator)
            training_metrics.append({"epoch": epoch + 1, "loss": epoch_loss})

        return TrainOutput(metrics=training_metrics, training_loss=self.state.total_flos, global_step=self.state.global_step)

    @overrides(HuggingFaceTrainer)
    def predict(self, dataset_role: DatasetRole, **kwargs) -> PredictionOutput:
        """
        Predicts on the dataset given.
        :param dataset_role: Role of dataset to predict on.
        :return: Prediction output containing similarity scores as predictions.
        """
        self.complete_device_setup()
        self.model.eval()
        self._current_eval_role = dataset_role
        dataset = self._get_dataset(dataset_role)
        input_examples = STUtil.to_input_examples(dataset)
        labels = [e.label for e in input_examples]
        device_scores = self.predict_similarity_scores(input_examples, device=self.device)
        host_scores = device_scores.cpu().tolist()
        scaled_scores = self.scale_scores(input_examples, host_scores)
        prediction_metrics = self._compute_validation_metrics(EvalPrediction(scaled_scores, labels))
        labels_tensor = self.get_labels_tensor(input_examples, self.device)
        with torch.no_grad():
            prediction_metrics["loss"] = self.compute_loss(scores=device_scores, labels=labels_tensor,
                                                           input_examples=input_examples).cpu().item()

        return PredictionOutput(host_scores, labels, prediction_metrics)

    def scale_scores(self, input_examples: List[InputExample], scores: List[float]) -> List[float]:
        """
        Uses min max scaling per parent to adjust the scores.
        :param input_examples: Contains the parent, child information.
        :param scores: List of pre-scaled scores.
        :return: The scaled scores.
        """
        items = zip(input_examples, scores)
        parent2items = DictUtil.group_by(items, lambda i: i[0].texts[1])
        parent2min = {}
        for p, children in parent2items.items():
            children_scores = [c[1] for c in children]
            parent2min[p] = {
                "min": min(children_scores),
                "max": max(children_scores)
            }
        new_scores = []
        for example, score in zip(input_examples, scores):
            parent_id = example.texts[1]
            parent_stats = parent2min[parent_id]
            parent_min = parent_stats["min"]
            parent_max = parent_stats["max"]
            new_score = MathUtil.convert_to_new_range(score, (parent_min, parent_max), (0, 1))
            new_scores.append(new_score)
        return new_scores

    def predict_similarity_scores(self, input_examples: List[InputExample], device: torch.device = None):
        """
        Predicts a similarity score for each input examples.
        :param input_examples: The examples to predict.
        :param device: The device to store tensor on.
        :return: List of similarity scores.
        """
        predictions = []
        texts = [t for example in input_examples for t in example.texts]
        embeddings_manager = EmbeddingsManager.create_from_content(texts, model=self.model, as_tensors=True)

        batches = ListUtil.batch(input_examples, self.args.eval_batch_size)
        for batch in tqdm(batches, desc="Computing predictions..."):
            batch_sentence_pairs = [i.texts for i in batch]
            batch_prediction_tensor = self.calculate_predictions(batch_sentence_pairs, embeddings_manager)
            batch_prediction = batch_prediction_tensor.tolist()
            predictions.extend(batch_prediction)

        predictions = torch.tensor(predictions)
        if device:
            predictions = predictions.to(device)
        return predictions

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
            source_features = self.model.tokenize(source_sentences)
            target_features = self.model.tokenize(target_sentences)

            TFUtil.move_features_to_device(self.device, source_features)
            TFUtil.move_features_to_device(self.device, target_features)

            source_embeddings = self.model(source_features)['sentence_embedding']
            target_embeddings = self.model(target_features)['sentence_embedding']
        else:
            raise Exception("Expected embedding manager or model to be defined.")

        predictions = self.calculate_similarity_scores(source_embeddings, target_embeddings)
        return predictions

    def setup_optimizer(self) -> Optimizer:
        """
        Creates optimizer with training parameters.
        :return:
        """
        assert self.starting_learning_rate is not None
        model_parameters = list(self.model.parameters())
        additional_parameters = list(self.get_additional_training_parameters())
        TFUtil.set_gradients(model_parameters, requires_grad=not self.trainer_args.freeze_base)
        parameters = model_parameters + additional_parameters
        trainable_params = [p for p in parameters if p.requires_grad]
        optimizer = optim.Adam(trainable_params, lr=self.starting_learning_rate)
        logger.info(f"Training {len(trainable_params)} parameters...")
        return optimizer

    def setup_scheduler(self, optimizer: Optimizer):
        """
        Creates scheduler for optimizer.
        :param optimizer: The optimizer.
        :return: The scheduler.
        """
        assert self.starting_learning_rate is not None and self.ending_learning_rate is not None
        total_epochs = int(self.args.num_train_epochs)
        gamma = (self.ending_learning_rate / self.starting_learning_rate) ** (1 / total_epochs)
        scheduler = ExponentialLR(optimizer, gamma=gamma)
        return scheduler

    def evaluate_if_save(self, evaluator: STEvaluator, **kwargs) -> None:
        """
        Evaluates the model and saves if its the best version of the model so far.
        :param evaluator: The evaluator called to get score.
        :param kwargs: Keyword arguments to evaluator.
        :return: None, model is saved.
        """
        epoch_score = evaluator(**kwargs)
        if self.curr_score is None or \
                (epoch_score > self.curr_score and self.trainer_args.greater_is_better) or \
                (epoch_score < self.curr_score and not self.trainer_args.greater_is_better):
            logger.info(f"New Best Model: {self.curr_score} -> {epoch_score}")
            self.curr_score = epoch_score
            self.save()
        else:
            logger.info(f"No change to best model ({self.curr_score})")

    def complete_device_setup(self) -> None:
        """
        Lazily performs final setup on device.
        :return: None
        """
        if not self.setup_complete:
            self.setup_training_device()
            self.setup_complete = True

    def setup_training_device(self) -> None:
        """
        Moves training modules to training device.
        :return: None
        """
        logger.info(f"Moving modules to training device: {self.device}")
        self.model = self.model.to(self.device)
        self.move_training_modules(self.device)

    def get_additional_training_parameters(self) -> Iterable[Parameter]:
        """
        :return: Returns parameters to include in optimizer calculation.
        """
        return []

    @staticmethod
    def get_labels_tensor(input_examples: List[InputExample], device: torch.device) -> torch.Tensor:
        """
        Creates tensor containing labels of examples.
        :param input_examples:  The input examples to extract labels from.
        :param device: The device to move labels to.
        :return: The tensor on device.
        """
        labels = [e.label for e in input_examples]
        labels_tensor = torch.Tensor(labels)
        return TFUtil.move_tensor_to_device(labels_tensor, device)

    @abstractmethod
    def move_training_modules(self, device: torch.device) -> None:
        """
        :param device: The device to move the training modules to.
        :return: Moves any additional modules to device before training.
        """
        pass

    @abstractmethod
    def calculate_similarity_scores(self, source_embeddings: torch.Tensor, target_embeddings: torch.Tensor):
        """
        Calculates the similarity scores between source and target embeddings.
        :param source_embeddings: The source embeddings of size (batch_size, features..).
        :param target_embeddings: The target embeddings (batch_size, features..).
        :return: Tensor containing similarity scores of size (batch_size,)
        """
        pass

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
    def save(self) -> None:
        """
        Saves the current model
        :param self:
        :return:
        """
