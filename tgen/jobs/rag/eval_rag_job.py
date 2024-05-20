import os
import time
from trace import Trace
from typing import Any, Callable, List

import pandas as pd

from tgen.common.constants.ranking_constants import DEFAULT_CROSS_ENCODER_MODEL
from tgen.common.logging.logger_manager import logger
from tgen.common.util.enum_util import EnumDict
from tgen.core.trainers.vsm_trainer import VSMTrainer
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.metrics.metrics_manager import MetricsManager
from tgen.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.relationship_manager.cross_encoder_manager import CrossEncoderManager
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
from tgen.scripts.constants import DATA_PATH
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from tgen.tracing.ranking.steps.re_rank_step import ReRankStep

METRICS = SupportedTraceMetric.get_keys()


class EvalRagJob(AbstractJob):

    def __init__(self, job_args: JobArgs, dataset_names: List[str], custom_export_path: str = None):
        """
        Creates new job evaluating RAG pipeline on dataset.
        :param job_args:
        """
        super().__init__(job_args)
        self.dataset_names = dataset_names
        self.custom_export_path = custom_export_path

    def _run(self) -> Any:

        entries_global = []
        for dataset_name in self.dataset_names:
            dataset_path = os.path.join(DATA_PATH, dataset_name)
            project_reader = StructuredProjectReader(dataset_path)
            trace_dataset_creator = TraceDatasetCreator(project_reader=project_reader)
            prompt_dataset_creator = PromptDatasetCreator(trace_dataset_creator=trace_dataset_creator)
            dataset = prompt_dataset_creator.create()

            entries = self.evaluate_dataset(dataset)
            for e in entries:
                e["dataset"] = dataset_name
            entries_global.extend(entries)

        metrics_df = pd.DataFrame(entries_global)
        summary_metrics = ["dataset", "method", "map", "precision", "recall", "tp", "fp", "tn", "fn"]
        summary_df = metrics_df[summary_metrics]

        if self.custom_export_path:
            os.makedirs(self.custom_export_path, exist_ok=True)
            metrics_df.to_csv(os.path.join(self.custom_export_path, "metrics.csv"), index=False)
            summary_df.to_csv(os.path.join(self.custom_export_path, "summary.csv"), index=False)
            logger.info(f"Saved files to {self.custom_export_path}")

        print(summary_df)

    @staticmethod
    def evaluate_dataset(dataset):
        artifact_df: ArtifactDataFrame = dataset.artifact_df

        def vsm():
            trainer_dataset_manager = TrainerDatasetManager.create_from_datasets(
                {DatasetRole.EVAL: dataset, DatasetRole.TRAIN: dataset})
            trainer = VSMTrainer(trainer_dataset_manager=trainer_dataset_manager, metrics=METRICS, select_predictions=False)
            trainer.perform_training(DatasetRole.EVAL)
            prediction_output = trainer.perform_prediction(evaluate=False)
            child2traces = RankingUtil.group_trace_predictions(prediction_output.prediction_entries, TraceKeys.child_label())
            RankingUtil.normalized_scores_by_individual_artifacts(child2traces, min_score=0)
            return prediction_output.prediction_entries

        vsm_metrics = EvalRagJob.eval_method(vsm, dataset, method="vsm")

        content_map = artifact_df.to_map()
        embeddings_manager = EmbeddingsManager(content_map=content_map)
        embedding_predictions = []

        def embeddings():
            embeddings_manager.create_embeddings()
            for child_type, parent_type in dataset.layer_df.as_list():
                child_artifact_ids = artifact_df.get_artifacts_by_type(child_type).index
                parent_artifact_ids = artifact_df.get_artifacts_by_type(parent_type).index

                ranking_args = RankingArgs(dataset=dataset,
                                           parent_ids=list(parent_artifact_ids),
                                           children_ids=list(child_artifact_ids),
                                           export_dir=None,
                                           re_rank_children=False,
                                           types_to_trace=(parent_type, child_type),
                                           generate_explanations=False,
                                           use_rag_defaults=False,
                                           interactive_mode=False,
                                           relationship_manager=embeddings_manager)

                pipeline = EmbeddingRankingPipeline(ranking_args)
                pipeline.run()
                selected_entries = pipeline.state.candidate_entries
                embedding_predictions.extend(selected_entries)

            child2traces = RankingUtil.group_trace_predictions(embedding_predictions, TraceKeys.child_label())
            RankingUtil.normalized_scores_by_individual_artifacts(child2traces, min_score=0)
            return embedding_predictions

        embedding_metrics = EvalRagJob.eval_method(embeddings, dataset, method="embeddings")
        args = RankingArgs(dataset=dataset,
                           parent_ids=[], children_ids=[], types_to_trace=dataset.layer_df.as_list(),
                           re_rank_children=True)
        state = RankingState()
        state.selected_entries = [EnumDict(**d) for d in embedding_predictions]
        state.relationship_manager = CrossEncoderManager(content_map, model_name=DEFAULT_CROSS_ENCODER_MODEL)

        def re_ranking():
            step = ReRankStep()
            step.run(args, state)
            return state.selected_entries

        re_ranking_metrics = EvalRagJob.eval_method(re_ranking, dataset, method="re_ranking")
        return [vsm_metrics, embedding_metrics, re_ranking_metrics]

    @staticmethod
    def eval_method(exec_lambda: Callable[[], List[Trace]], dataset: TraceDataset, **kwargs):
        start_time = time.time()
        predictions = exec_lambda()
        end_time = time.time()

        id2trace = {}
        for entry in predictions:
            id2trace[entry[TraceKeys.LINK_ID]] = entry

        scores = []
        for t_id in dataset.trace_df.index:
            score = id2trace[t_id][TraceKeys.SCORE] if t_id in id2trace else 0
            scores.append(score)

        # Evaluate
        metrics_manager = MetricsManager(dataset.trace_df, trace_predictions=scores)
        metrics = metrics_manager.eval(SupportedTraceMetric.get_keys())

        output = {"time": end_time - start_time}
        output.update(kwargs)
        output.update(metrics)
        return output
