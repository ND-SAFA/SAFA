import os
import time
from trace import Trace
from typing import Any, Callable, List

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

from tgen.common.logging.logger_manager import logger
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

        EvalRagJob.compare(dataset, embedding_predictions, vsm_predictions, "embeddings", "vsm")
        return [vsm_metrics, embedding_metrics]

    @staticmethod
    def compare(dataset, a_preds, b_preds, a_name, b_name):
        a_pred_map = {}
        for entry in a_preds:
            a_pred_map[entry[TraceKeys.LINK_ID]] = entry

        b_pred_map = {}
        for entry in b_preds:
            b_pred_map[entry[TraceKeys.LINK_ID]] = entry

        pred_ids = a_pred_map.keys()

        common = []  # both a and b got right
        a_entries = []  # only a got right
        b_entries = []  # only b got right
        nobody = []
        all_entries = []

        artifact_map = dataset.artifact_df.to_map()
        trace_map = {}
        for pred_id in pred_ids:
            a_pred = a_pred_map[pred_id]
            b_pred = b_pred_map[pred_id]
            trace = dataset.trace_df.loc[pred_id]
            pred_label = trace[TraceKeys.LABEL.value]
            a_pred_label = 1 if a_pred[TraceKeys.SCORE] >= 0.5 else 0
            b_pred_label = 1 if b_pred[TraceKeys.SCORE] >= 0.5 else 0

            a_right = a_pred_label == pred_label
            b_right = b_pred_label == pred_label

            source_id = trace[TraceKeys.SOURCE.value]
            target_id = trace[TraceKeys.TARGET.value]

            entry = {
                "label": pred_label,
                a_name: a_pred[TraceKeys.SCORE],
                b_name: b_pred[TraceKeys.SCORE],
                "source": source_id,
                "target": target_id,
                "intersection": EvalRagJob.calc_intersection(artifact_map[source_id], artifact_map[target_id])
            }

            if a_right and b_right:
                common.append(entry)
            elif a_right and not b_right:
                a_entries.append(entry)
            elif b_right and not a_right:
                b_entries.append(entry)
            else:
                nobody.append(entry)

            all_entries.append(entry)
            if target_id not in trace_map:
                trace_map[target_id] = []

            trace_map[target_id].append(entry)

        experiment_path = os.path.expanduser("~/desktop/experiment")

        scores = []
        for t_id in dataset.trace_df.index:
            a_pred = a_pred_map[t_id]
            b_pred = b_pred_map[t_id]
            score = max(b_pred[TraceKeys.SCORE], a_pred[TraceKeys.SCORE])
            scores.append(score)

        metrics_manager = MetricsManager(dataset.trace_df, trace_predictions=scores)
        metrics = metrics_manager.eval(SupportedTraceMetric.get_keys())
        trace_map = {t: sorted(v, key=lambda t: t[b_name], reverse=True) for t, v in trace_map.items()}

        ap_entries = {}
        for a_id, entries in trace_map.items():
            labels = [e["label"] for e in entries]
            a_scores = [e[a_name] for e in entries]
            b_scores = [e[b_name] for e in entries]
            pos_entries = [e['intersection'] for e in entries if e["label"] == 1]
            ap_entries[a_id] = {
                a_name: average_precision_score(labels, a_scores),
                b_name: average_precision_score(labels, b_scores),
                "intersection": np.nan if len(pos_entries) == 0 else sum(pos_entries) / len(pos_entries)
            }

        vsm_best = [k for k, v in ap_entries.items() if v["embeddings"] < v["vsm"]]
        embeddings_best = [k for k, v in ap_entries.items() if v["embeddings"] > v["vsm"]]

        vsm_best_lengths = [len(artifact_map[k]) for k in vsm_best]
        embeddings_best_lengths = [len(artifact_map[k]) for k in embeddings_best]

        print("Combined metrics:", metrics)
        print("Done.")

    @staticmethod
    def calc_intersection(a: str, b: str):
        a_words = a.split(" ")
        words_contained = [a_word for a_word in a_words if a_word in b]
        return len(words_contained) / len(a_words)

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
