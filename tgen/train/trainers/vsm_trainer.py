import time
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn import exceptions
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import pairwise_distances
from transformers.trainer_utils import PredictionOutput

from tgen.constants.other_constants import VSM_THRESHOLD_DEFAULT
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.ranking.pipeline.utils import extract_prompt_artifacts
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trace_output.stage_eval import Metrics
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.train.trace_output.trace_train_output import TraceTrainOutput
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.override import overrides

SimilarityMatrix = Union[csr_matrix, np.array]


class VSMTrainer(AbstractTrainer):
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
        if metrics is None:
            metrics = SupportedTraceMetric.get_keys()
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model = vectorizer()
        self.metrics = metrics
        super().__init__(trainer_dataset_manager=trainer_dataset_manager, trainer_args=None)

    @overrides(AbstractTrainer)
    def perform_training(self, dataset_role: DatasetRole = DatasetRole.TRAIN) -> TraceTrainOutput:
        """
        Performs training on the model using the Train dataset
         :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :return: The train output (not currently used)
        """
        train_dataset: TraceDataset = self.trainer_dataset_manager[dataset_role]
        start_time = time.perf_counter()
        self.train(train_dataset)
        finish_time = time.perf_counter()
        return TraceTrainOutput(training_time=finish_time - start_time)

    @overrides(AbstractTrainer)
    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL,
                           dataset: iDataset = None,
                           threshold: float = VSM_THRESHOLD_DEFAULT) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :param dataset: The dataset to use instead of from the dataset manager
        :param threshold: The threshold to use to determine whether a link is traced
        :return: The output from the predictions
        """
        eval_dataset: TraceDataset = self.trainer_dataset_manager[dataset_role] if not dataset else dataset
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
        parent_artifacts, child_artifacts, parent_child_pairs = self.get_raw_sources_and_targets(eval_dataset)
        parent_tf_matrix, child_tf_matrix = self.create_term_frequency_matrices(parent_artifacts, child_artifacts)
        similarity_matrix = self.calculate_similarity_matrix_from_term_frequencies(parent_tf_matrix, child_tf_matrix)
        predictions, label_ids, source_target_pairs, link_ids = [], [], [], []
        for i, (parent_id, child_id) in enumerate(parent_child_pairs):
            link_id = TraceDataFrame.generate_link_id(source_id=child_id, target_id=parent_id)
            if link_id not in eval_dataset.trace_df:  # source, target pair between layers that should not be linked
                continue
            row, col = divmod(i, len(child_artifacts))
            predictions.append(similarity_matrix[row][col])
            label_ids.append(int(predictions[-1] > threshold))
            link_ids.append(link_id)
            source_target_pairs.append((child_id, parent_id))  # source, target
        prediction_output = PredictionOutput(predictions=predictions, label_ids=label_ids, metrics=None)
        trace_prediction_output = TracePredictionOutput(prediction_output=prediction_output, source_target_pairs=source_target_pairs)

        if eval_dataset.trace_df.get_label_count(1) > 0:
            metrics = self.eval(eval_dataset.trace_df, predictions, link_ids, self.metrics) \
                if self.metrics else None
            prediction_output.metrics = metrics
            trace_prediction_output.metrics = metrics
        return trace_prediction_output

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
        parent_ids, child_ids = extract_prompt_artifacts(dataset.artifact_df)
        parent_artifacts = [dataset.artifact_df.get_artifact(s_id) for s_id in parent_ids]
        child_artifacts = [dataset.artifact_df.get_artifact(t_id) for t_id in child_ids]
        parent_child_pairs = []
        for parent_id in parent_ids:
            for child_id in child_ids:
                parent_child_pairs.append((parent_id, child_id))

        parent_bodies = pd.Series([artifact[ArtifactKeys.CONTENT] for artifact in parent_artifacts])
        child_bodies = pd.Series([artifact[ArtifactKeys.CONTENT] for artifact in child_artifacts])
        return parent_bodies, child_bodies, parent_child_pairs

    @staticmethod
    def eval(trace_df: TraceDataFrame, predictions: List[float], link_ids: List[int], metrics: List[str]) -> Metrics:
        """
        Evaluates the prediction results using the metrics
        :param trace_df: The dataframe containing the trace links
        :param predictions: The similarity scores predicted by the model
        :param link_ids: Specifies the links ids corresponding to the predictions
        :param metrics: The list of metric names to use for evaluation
        :return: A mapping between metric name and the result
        """
        metrics_manager = MetricsManager(trace_df=trace_df, predicted_similarities=predictions, link_ids=link_ids)
        return metrics_manager.eval(metrics)

    def cleanup(self) -> None:
        """
        Required by parent class, unused
        :return: None
        """
        pass
