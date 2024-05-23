import os
import time
from typing import Any, Callable, List

import pandas as pd

from tgen.common.logging.logger_manager import logger
from tgen.common.objects.trace import Trace
from tgen.common.util.dict_util import DictUtil
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
from tgen.jobs.rag.tracing_evaluator import TracingEvaluator
from tgen.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
from tgen.scripts.constants import DATA_PATH
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline

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
        summary_metrics = ["method", "map", "precision_at_recall"]
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
        vsm_predictions = []

        def vsm():
            trainer_dataset_manager = TrainerDatasetManager.create_from_datasets(
                {DatasetRole.EVAL: dataset, DatasetRole.TRAIN: dataset})
            trainer = VSMTrainer(trainer_dataset_manager=trainer_dataset_manager, metrics=METRICS, select_predictions=False)
            trainer.perform_training(DatasetRole.EVAL)
            prediction_output = trainer.perform_prediction(evaluate=False)
            child2traces = RankingUtil.group_trace_predictions(prediction_output.prediction_entries, TraceKeys.child_label())
            RankingUtil.normalized_scores_by_individual_artifacts(child2traces, min_score=0)
            vsm_predictions.extend(prediction_output.prediction_entries)
            return prediction_output.prediction_entries

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

        metrics = EvalRagJob.eval_method(["vsm", "embeddings"], [vsm, embeddings], dataset)

        return metrics

    @staticmethod
    def calc_intersection(a: str, b: str):
        a_words = a.split(" ")
        words_contained = [a_word for a_word in a_words if a_word in b]
        return len(words_contained) / len(a_words)

    @staticmethod
    def eval_method(methods: List[str], method_execs: List[Callable[[], List[Trace]]], dataset: TraceDataset, **kwargs):

        global_metrics = {}
        global_query_metrics = {}
        global_predictions = []

        methods.append("combined")
        method_execs.append(lambda: EvalRagJob.combine_predictions(global_predictions))

        for method_name, method_exec in zip(methods, method_execs):
            start_time = time.time()
            predictions = method_exec()
            end_time = time.time()
            global_predictions.append(predictions)

            evaluator = TracingEvaluator(dataset.trace_df, predictions)
            metrics, query_metrics = evaluator.calculate_metrics()

            output = {"time": end_time - start_time, **metrics}
            global_metrics[method_name] = output
            global_query_metrics[method_name] = query_metrics

        return global_metrics

    @staticmethod
    def combine_predictions(method_predictions: List[List[Trace]]) -> List[Trace]:
        id2trace = {}
        for prediction_batch in method_predictions:
            for prediction in prediction_batch:
                t_id = prediction[TraceKeys.LINK_ID]
                DictUtil.initialize_value_if_not_in_dict(id2trace, t_id, [])
                id2trace[t_id].append(prediction)

        combined_traces = []
        for t_id, traces in id2trace.items():
            trace = Trace(**traces[0])
            trace[TraceKeys.SCORE] = max(trace[TraceKeys.SCORE] for trace in traces)
            combined_traces.append(trace)

        return combined_traces
