import time
from trace import Trace
from typing import Any, Callable, List

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.metrics.metrics_manager import MetricsManager
from tgen.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from tgen.tracing.ranking.steps.re_rank_step import ReRankStep


class EvalRagJob(AbstractJob):

    def __init__(self, job_args: JobArgs):
        """
        Creates new job evaluating RAG pipeline on dataset.
        :param job_args:
        """
        super().__init__(job_args)

    def _run(self) -> Any:
        dataset = self.job_args.dataset_creator.create()
        artifact_df: ArtifactDataFrame = dataset.artifact_df
        content_map = artifact_df.to_map()
        embeddings_manager = EmbeddingsManager(content_map=content_map)

        metrics = {}

        embeddings_manager.create_embeddings()

        def embeddings():
            embedding_predictions = []
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
                                           use_rag_defaults=True, relationship_manager=embeddings_manager)

                pipeline = EmbeddingRankingPipeline(ranking_args)
                pipeline.run()
                selected_entries = pipeline.state.get_current_entries()
                embedding_predictions.extend(selected_entries)
            return embedding_predictions

        def re_ranking():
            step = ReRankStep()

        embedding_metrics = self.eval_method(embeddings, dataset)

    def eval_method(self, exec_lambda: Callable[[], List[Trace]], dataset: TraceDataset):
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
        metrics["time"] = end_time - start_time

        return metrics
