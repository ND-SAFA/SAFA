from typing import List, Tuple

import numpy as np
from datasets import Dataset
from sentence_transformers import InputExample, SentenceTransformer
from torch.utils.data import DataLoader
from transformers.trainer_utils import EvalPrediction, PredictionOutput, TrainOutput

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.hugging_face_constants import DEFAULT_MAX_STEPS_BEFORE_EVAL, NEG_LINK
from tgen.common.logging.logger_manager import logger
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.common.util.list_util import ListUtil
from tgen.common.util.override import overrides
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.core.trainers.st.custom_sentence_transformer import CustomSentenceTransformer
from tgen.core.trainers.st.sentence_transformer_evaluator import SentenceTransformerEvaluator
from tgen.core.trainers.st.st_loss_functions import SupportedLossFunctions
from tgen.core.trainers.st.st_metrics import STMetrics
from tgen.core.trainers.st.st_training_manager import STTrainingParams
from tgen.data.keys.csv_keys import CSVKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType, ModelTask


class BalancedBatchSampler:
    def __init__(self, dataset, batch_size: int):
        self.indices = list(np.arange(len(dataset)))
        self.num_samples = len(dataset)
        self.labels = np.array([example.label for example in dataset])
        self.n_positive = len([s for s in self.labels if s != 0])
        self.batch_size = batch_size
        self.negative_indices = self.create_negative_indices()
        self.other_indices = self.create_other_indices()
        self.n_batches = int(min(len(self.other_indices), len(self.negative_indices)) // (self.batch_size / 2))

    def create_negative_indices(self):
        return [i for i in self.indices if self.labels[i] == 0]

    def create_other_indices(self):
        return [i for i in self.indices if self.labels[i] != 0]

    def select_negative(self, n_items: int):
        selected, self.negative_indices = self.select_indices(self.negative_indices, n_items, self.create_negative_indices)
        return selected

    def select_other(self, n_items: int):
        selected, self.other_indices = self.select_indices(self.other_indices, n_items, self.create_other_indices)
        return selected

    @staticmethod
    def select_indices(indices, n_items, create_indices_method):
        if n_items > len(indices):
            logger.info("Resetting indices...")
            indices = create_indices_method()  # Recreate indices using the provided method

        selected = list(np.random.choice(indices, n_items, replace=False))
        indices = [index for index in indices if index not in selected]  # Efficient way to remove selected items
        return selected, indices  # Return both selected items and the updated indices list

    def __iter__(self):
        return self

    def __next__(self):
        n_negative = self.batch_size // 2
        n_pos = self.batch_size - n_negative
        batch_indices = self.select_negative(n_negative) + self.select_other(n_pos)
        np.random.shuffle(batch_indices)
        return batch_indices

    def __len__(self):
        return self.n_batches


class SentenceTransformerTrainer(HuggingFaceTrainer):
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
        self.losses = []
        self.total_loss = 0
        self.loss_function = None
        self.params = None
        self.loss_function = self._create_loss_function()

    @overrides(HuggingFaceTrainer)
    def train(self, **kwargs) -> TrainOutput:
        """
        Trains a sentence transformer model.
        :param kwargs: Currently ignored. TODO: add ability to start from checkpoint.
        :return: None
        """
        if SupportedLossFunctions.MNRL.is_name(self.trainer_args.st_loss_function):
            self.train_dataset = self.trainer_dataset_manager[DatasetRole.TRAIN].to_hf_dataset(self.model_manager, use_pos_ids=True)
            logger.info("Using only positive links in training dataset.")

        train_examples = self.to_input_examples(self.train_dataset, use_scores=self.trainer_args.use_scores, model=self.model)
        train_dataloader = DataLoader(train_examples,
                                      batch_sampler=BalancedBatchSampler(train_examples, batch_size=self.args.train_batch_size))

        n_steps = min(len(train_dataloader) + 1, self.min_eval_steps)

        evaluator = SentenceTransformerEvaluator(self, self.evaluation_roles) if self.has_dataset(DatasetRole.VAL) else None

        logger.log_title("Training...", prefix=NEW_LINE)
        model: CustomSentenceTransformer = self.model
        self.params = STTrainingParams(
            epochs=int(self.args.num_train_epochs),
            warmup_steps=self.args.warmup_steps,
            evaluation_steps=n_steps,
            evaluator=evaluator,
            output_path=self.args.output_dir,
            save_best_model=self.trainer_args.save_best_model,
            accumulation_steps=self.args.gradient_accumulation_steps
        )
        model.fit(train_objectives=[(train_dataloader, self.loss_function)], training_params=self.params)
        self.state.best_model_checkpoint = self.args.output_dir
        if self.args.load_best_model_at_end:
            self.model = CustomSentenceTransformer(self.state.best_model_checkpoint)

        metrics = STMetrics(records=evaluator.metrics, losses=self.losses)
        return TrainOutput(metrics=metrics, training_loss=self.total_loss, global_step=self.params.global_step)

    @overrides(HuggingFaceTrainer)
    def predict(self, dataset_role: DatasetRole, **kwargs) -> PredictionOutput:
        """
        Predicts on the dataset given.
        :param dataset_role: Role of dataset to predict on.
        :return: Prediction output containing similarity scores as predictions.
        """
        self._current_eval_role = dataset_role
        dataset = self._get_dataset(dataset_role)
        input_examples = self.to_input_examples(dataset)
        scores, labels = self.calculate_similarities(self.model, input_examples)
        prediction_metrics = self._compute_validation_metrics(EvalPrediction(scores, labels))
        features, labels = self.model.smart_batching_collate(input_examples)
        for feature in features:
            for label, tensor in feature.items():
                tensor.to(self.model._target_device)
        labels.to(self.model._target_device)
        prediction_metrics["loss"] = self.loss_function(features, labels).item()
        return PredictionOutput(scores, labels, prediction_metrics)

    def _create_loss_function(self):
        """
        Creates the loss function from its defined class.
        :return: The loss function.
        """
        loss_function_name = self.trainer_args.st_loss_function
        loss_function_kwargs = {}
        possible_params = {"size_average": False, "margin": 0.1}
        loss_function_class = SupportedLossFunctions.get_value(loss_function_name)
        for param, param_value in possible_params.items():
            if ReflectionUtil.has_constructor_param(loss_function_class, param):
                loss_function_kwargs[param] = param_value

        loss_function = loss_function_class(self.model, **loss_function_kwargs)
        logger.info(f"Created loss function {loss_function_name}.")
        return loss_function

    @staticmethod
    def to_input_examples(dataset: Dataset, use_scores: bool = False, model: SentenceTransformer = None) -> List[InputExample]:
        """
        Converts a huggingface dataset into a list of sentence transformer input examples.
        :param dataset: The huggingface dataset.
        :param use_scores: Whether to use score over label for negative links.
        :param model: If use_scores, the model used to embed artifacts.
        :return: List of input examples.
        """
        input_examples = []
        for i in dataset:
            source_text = i[CSVKeys.SOURCE]
            target_text = i[CSVKeys.TARGET]
            label = float(i[CSVKeys.LABEL])
            score = i.get(CSVKeys.SCORE, None)
            if use_scores and score:
                label = float(score)
            input_examples.append(InputExample(texts=[source_text, target_text], label=label))

        if use_scores and all([i.label is None for i in input_examples]):
            assert model, f"Model is required to be defined if use_scores is True. Received {model}."
            SentenceTransformerTrainer.replace_labels_with_scores(model, input_examples)
        return input_examples

    @staticmethod
    def replace_labels_with_scores(model: SentenceTransformer, input_examples: List[InputExample], label: int = NEG_LINK):
        """
        Replaces the matching labels with model similarity score.
        :param model: The model to create embeddings for artifacts for.
        :param input_examples: The input examples to modify.
        :param label: The label to replace with scores.
        :return: None. Modified in place.
        """
        examples_with_label = [input_example for input_example in input_examples if input_example.label == label]
        content = ListUtil.flatten([input_example.texts for input_example in examples_with_label])

        embeddings_manager = EmbeddingsManager.create_from_content(content, model=model, show_progress_bar=False)

        for input_example in examples_with_label:
            input_example.label = SentenceTransformerTrainer.get_input_example_score(embeddings_manager, input_example)

        logger.info(f"Adding scores to {len(examples_with_label)} input examples.")

    @staticmethod
    def calculate_similarities(model: SentenceTransformer, input_examples: List[InputExample]) -> Tuple[List[float], List[float]]:
        """
        Calculates the cosine similarity between the texts in each input example. TODO: Replace with embedding util.
        :param model: The model used to embed the test dataset.
        :param input_examples: The list of input examples to calculate similarities for.
        :return: Prediction output containing scores as predictions and labels as label ids.
        """
        unique_content = list(set(ListUtil.flatten([e.texts for e in input_examples])))
        embeddings_manager = EmbeddingsManager.create_from_content(unique_content, model=model, show_progress_bar=False)
        scores = []
        labels = []
        for example in input_examples:
            score = SentenceTransformerTrainer.get_input_example_score(embeddings_manager, example)
            scores.append(score)
            labels.append(example.label)
        return scores, labels

    @staticmethod
    def get_input_example_score(embeddings_manager: EmbeddingsManager, input_example: InputExample) -> float:
        """
        Calculates the similarity score between the two texts in the input example.
        :param embeddings_manager: The embeddings manager containing embedding to text.
        :param input_example: The input example containing texts to compare.
        :return: The similarity score between texts.
        """
        s_text, t_text = input_example.texts
        s_embedding = embeddings_manager.get_embedding(s_text)
        t_embedding = embeddings_manager.get_embedding(t_text)
        score = EmbeddingUtil.calculate_similarity(s_embedding, t_embedding)
        return score
