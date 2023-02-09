from typing import List, Tuple, Dict, Union

import numpy as np

from constants import VSM_THRESHOLD_DEFAULT
from data.datasets.dataset_role import DatasetRole
from data.datasets.trace_dataset import TraceDataset
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from data.tree.trace_link import TraceLink
from train.itrainer import iTrainer
from train.metrics.metrics_manager import MetricsManager
from train.trace_output.stage_eval import Metrics
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trace_output.trace_train_output import TraceTrainOutput
import pandas as pd
from sklearn import exceptions
from scipy.sparse import csr_matrix, vstack
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import pairwise_distances

from util.override import overrides

SimilarityMatrix = Union[csr_matrix, np.array]


class VSMTrainer(iTrainer):
    """
    Handles training using VSM
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, vectorizer: CountVectorizer = TfidfVectorizer,
                 metrics: List[str] = None):
        """
        Initializes trainer with the datasets used for training + eval
        :param trainer_dataset_manager: The manager for the datasets used for training and/or predicting
        :param vectorizer: vectorizer for assigning weights to words, must be one of sklearn.text.extraction
        :param metrics: A list of metric names to use for evaluation
        """
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model = vectorizer()
        self.metrics = metrics

    @overrides(iTrainer)
    def perform_training(self, checkpoint: str = None) -> TraceTrainOutput:
        """
        Performs training on the model using the Train dataset
        :param checkpoint: From interface - Not used
        :return: The train output (not currently used)
        """
        train_dataset: TraceDataset = self.trainer_dataset_manager[DatasetRole.TRAIN]
        self.train(train_dataset)
        return TraceTrainOutput()

    @overrides(iTrainer)
    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL,
                           threshold: float = VSM_THRESHOLD_DEFAULT) -> TracePredictionOutput:
        """
        Performs predictions on the model using the given dataset role
        :param dataset_role: The dataset role to use for predictions
        :param threshold: The threshold to use to determine whether a link is traced
        :return: The output from the predictions
        """
        eval_dataset: TraceDataset = self.trainer_dataset_manager[dataset_role]
        try:
            output = self.predict(eval_dataset, threshold)
        except exceptions.NotFittedError:
            raise exceptions.NotFittedError("Model must be trained before calling predict")
        return output

    def train(self, train_dataset: TraceDataset) -> None:
        """
        Fits the model on the raw source and target tokens used for training
        :param train_dataset: The dataset to use for training
        :return: None
        """
        raw_sources, raw_targets, _ = self.get_raw_sources_and_targets(train_dataset)
        combined = pd.concat([raw_sources, raw_targets], axis=0)
        self.model.fit(combined)

    def predict(self, eval_dataset: TraceDataset, threshold: float) -> TracePredictionOutput:
        """
        Uses the trained model to predict on the raw source and target tokens
        :param eval_dataset: The dataset to use for predicting
        :param threshold: All similarity scores above this threshold will be considered traced, otherwise they are untraced
        :return: The output from the prediction
        """
        raw_sources, raw_targets, all_source_target_pairs = self.get_raw_sources_and_targets(eval_dataset)
        set_source, set_target = self.create_term_frequency_matrices(raw_sources, raw_targets)
        similarity_matrix = self.calculate_similarity_matrix_from_term_frequencies(set_source, set_target)
        predictions, label_ids, source_target_pairs, links = [], [], [], []
        for i, pair in enumerate(all_source_target_pairs):
            link_id = TraceLink.generate_link_id(*pair)
            if link_id not in eval_dataset.links:  # source, target pair between layers that should not be linked
                continue
            row, col = divmod(i, len(raw_targets))
            predictions.append(similarity_matrix[row][col])
            label_ids.append(int(predictions[-1] > threshold))
            links.append(eval_dataset.links[link_id])
            source_target_pairs.append(pair)
        metrics = self.eval(links, predictions, self.metrics) if self.metrics else None
        return TracePredictionOutput(predictions=predictions, label_ids=label_ids, source_target_pairs=source_target_pairs,
                                     metrics=metrics)

    def create_term_frequency_matrices(self, raw_sources: pd.Series, raw_targets: pd.Series) -> Tuple[csr_matrix, csr_matrix]:
        """
        Creates 2 TermFrequencyMatrices (one for A another for B) where the weight of
        each (row, col) pair is calculated via TF-IDF
        :param raw_sources : The source documents whose matrix is the first element
        :param raw_targets : The target documents whose matrix is the second element
        :return: CountMatrix for raw_sources and raw_targets, and also the trained model
        """
        set_source: csr_matrix = self.model.transform(raw_sources)
        set_target: csr_matrix = self.model.transform(raw_targets)
        return set_source, set_target

    @staticmethod
    def calculate_similarity_matrix_from_term_frequencies(tf_source: csr_matrix, tf_target: csr_matrix) -> SimilarityMatrix:
        """
        Calculates the similarity matrix used for predicting traces from the term frequencies of the sources and targets
        :param tf_source: The term frequencies of the sources
        :param tf_target: The term frequencies of the targets
        :return: The similarity matrix where each cell contains the similarity of the corresponding source (row) and target (col)
        """
        return 1 - pairwise_distances(tf_source, Y=tf_target, metric="cosine", n_jobs=-1)

    @staticmethod
    def get_raw_sources_and_targets(dataset: TraceDataset) -> Tuple[pd.Series, pd.Series, List[Tuple[str, str]]]:
        """
        Gets the raw source and target tokens from a dataset
        :param dataset: The dataset to use for sources and targets
        :return: The raw source and target tokens as a tuple of pd.Series and a list containing the ids of each source target pair
        """
        sources, targets = set(), set()
        for link in dataset.links.values():
            sources.add(link.source)
            targets.add(link.target)
        source_target_pairs = [(source.id, target.id) for source in sources for target in targets]
        raw_sources = pd.Series([source.token for source in sources])
        raw_targets = pd.Series([target.token for target in targets])
        return raw_sources, raw_targets, source_target_pairs

    @staticmethod
    def eval(links: List[TraceLink], predictions: List[float], metrics: List[str]) -> Metrics:
        """
        Evaluates the prediction results using the metrics
        :param links: The links corresponding to the predictions
        :param predictions: The similarity scores predicted by the model
        :param metrics: The list of metric names to use for evaluation
        :return: A mapping between metric name and the result
        """
        metrics_manager = MetricsManager(trace_links=links, predicted_similarities=predictions)
        return metrics_manager.eval(metrics)
