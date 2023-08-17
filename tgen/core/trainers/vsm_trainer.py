import time
from typing import Dict, Iterable, List, Tuple, Union

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn import exceptions
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import pairwise_distances

from tgen.common.util.list_util import ListUtil
from tgen.common.util.override import overrides
from tgen.common.util.ranking_util import RankingUtil
from tgen.constants.other_constants import VSM_THRESHOLD_DEFAULT
from tgen.constants.ranking_constants import DEFAULT_VSM_SELECT_PREDICTION
from tgen.core.trace_output.stage_eval import Metrics
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.core.trainers.abstract_trainer import AbstractTrainer
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from tgen.data.processing.cleaning.data_cleaner import DataCleaner
from tgen.data.processing.cleaning.lemmatize_words_step import LemmatizeWordStep
from tgen.data.processing.cleaning.remove_non_alpha_chars_step import RemoveNonAlphaCharsStep
from tgen.data.processing.cleaning.separate_camel_case_step import SeparateCamelCaseStep
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.metrics.metrics_manager import MetricsManager
from tgen.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.ranking.common.utils import extract_tracing_requests

SimilarityMatrix = Union[csr_matrix, np.array]


class VSMTrainer(AbstractTrainer):
    """
    Handles training using VSM
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, vectorizer: CountVectorizer = TfidfVectorizer,
                 metrics: List[str] = None, steps: List[AbstractDataProcessingStep] = None,
                 select_predictions: bool = DEFAULT_VSM_SELECT_PREDICTION):
        """
        Initializes trainer with the datasets used for training + eval
        :param trainer_dataset_manager: The manager for the datasets used for training and/or predicting
        :param vectorizer: vectorizer for assigning weights to words, must be one of sklearn.text.extraction
        :param metrics: A list of metric names to use for evaluation
        """
        if steps is None:
            steps = [RemoveNonAlphaCharsStep(), SeparateCamelCaseStep(), LemmatizeWordStep()]
        if metrics is None:
            metrics = SupportedTraceMetric.get_keys()
        self.trainer_dataset_manager = trainer_dataset_manager
        self.model = vectorizer(strip_accents="ascii")
        self.metrics = metrics
        self.artifact_map = VSMTrainer.create_clean_artifact_map(self.trainer_dataset_manager, steps)
        self.select_predictions = select_predictions
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
        Fits the model on the set of raw source and target tokens in training dataset.
        :param train_dataset: The dataset to use for training
        :return: None
        """
        tracing_requests = extract_tracing_requests(train_dataset.artifact_df, train_dataset.layer_df.as_list())
        artifacts = []
        for tracing_request in tracing_requests:
            artifacts = artifacts + self.get_artifacts(tracing_request.parent_ids)
            artifacts = artifacts + self.get_artifacts(tracing_request.child_ids)
        combined = pd.Series(artifacts)
        self.model.fit(combined)

    def get_artifacts(self, artifact_ids: List[str]) -> List[str]:
        return [self.artifact_map[a_id] for a_id in artifact_ids]

    def predict(self, eval_dataset: TraceDataset, threshold: float) -> TracePredictionOutput:
        """
        Uses the trained model to predict on the raw source and target tokens
        :param eval_dataset: The dataset to use for predicting
        :param threshold: All similarity scores above this threshold will be considered traced, otherwise they are untraced
        :return: The output from the prediction
        """
        tracing_requests = extract_tracing_requests(eval_dataset.artifact_df, eval_dataset.layer_df.as_list())
        prediction_entries = []

        for tracing_request in tracing_requests:
            parent_artifacts = self.get_artifacts(tracing_request.parent_ids)
            child_artifacts = self.get_artifacts(tracing_request.child_ids)
            child_parent_pairs = tracing_request.get_tracing_pairs()

            parent_tf_matrix, child_tf_matrix = self.create_term_frequency_matrices(parent_artifacts, child_artifacts)
            similarity_matrix = self.calculate_similarity_matrix_from_term_frequencies(parent_tf_matrix, child_tf_matrix)

            for i, (child_id, parent_id) in enumerate(child_parent_pairs):
                link_id = TraceDataFrame.generate_link_id(source_id=child_id, target_id=parent_id)
                row, col = divmod(i, len(child_artifacts))
                similarity_score = similarity_matrix[row][col]

                link_id = eval_dataset.trace_df.generate_link_id(child_id, parent_id)
                label = eval_dataset.trace_df.get_link(link_id)[TraceKeys.LABEL]
                prediction_entry = TracePredictionEntry(source=child_id, target=parent_id, score=similarity_score, label=label)
                prediction_entries.append(prediction_entry)

        if self.select_predictions:
            self.convert_to_percentiles(prediction_entries)
            prediction_entries = RankingUtil.select_predictions(prediction_entries)
        metrics = RankingUtil.calculate_ranking_metrics(eval_dataset, prediction_entries)
        trace_prediction_output = TracePredictionOutput(prediction_entries=prediction_entries,
                                                        metrics=metrics)
        return trace_prediction_output

    def create_term_frequency_matrices(self, raw_sources: Iterable[str], raw_targets: Iterable[str]) -> \
            Tuple[csr_matrix, csr_matrix]:
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
    def create_clean_artifact_map(trainer_dataset_manager: TrainerDatasetManager, cleaning_steps: List[AbstractDataProcessingStep]) -> \
            Dict[str, str]:
        """
        Creates a map of artifact ids to cleaned artifact bodies for all datasets.
        :param trainer_dataset_manager: The trainer dataset manager containing datasets with artifacts to clean.
        :param cleaning_steps: The cleaning steps to perform.
        :return: Map of artifact id to clean body.
        """
        data_cleaner = DataCleaner(steps=cleaning_steps)
        artifacts_seen = set()
        artifact_ids = []
        artifact_bodies = []
        for dataset_role in DatasetRole:
            dataset = trainer_dataset_manager[dataset_role]
            if dataset is None:
                continue
            for artifact_id, artifact_row in dataset.artifact_df.itertuples():
                if artifact_id not in artifacts_seen:
                    artifacts_seen.add(artifact_id)
                    artifact_ids.append(artifact_id)
                    artifact_bodies.append(artifact_row[ArtifactKeys.CONTENT])

        artifact_bodies = data_cleaner.run(list(artifact_bodies))
        return {a_id: a_body for a_id, a_body in zip(artifact_ids, artifact_bodies)}

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

    @staticmethod
    def convert_to_percentiles(predictions: List[TracePredictionEntry]) -> None:
        """
        Converts the scores into percentiles.
        :param predictions: The trace predictions containing scores.
        :return: None
        """
        parent2preds = {}
        for p in predictions:
            parent_id = p["target"]
            if parent_id not in parent2preds:
                parent2preds[parent_id] = []
            parent2preds[parent_id].append(p)

        for parent, preds in parent2preds.items():
            scores = [p["score"] for p in preds]
            percentiles = ListUtil.get_percentiles(scores)
            for p, percentile in zip(preds, percentiles):
                p["score"] = percentile
