import json
from typing import Any

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.util.str_util import StrUtil
from tgen.core.trainers.vsm_trainer import VSMTrainer
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.jobs.abstract_job import AbstractJob
from tgen.metrics.metrics_manager import MetricsManager
from tgen.metrics.supported_trace_metric import SupportedTraceMetric


class EvalConceptTracingJob(AbstractJob):
    def _run(self) -> Any:
        # dataset
        dataset = self.job_args.dataset_creator.create()
        artifact_df: ArtifactDataFrame = dataset.artifact_df
        layer_df: LayerDataFrame = dataset.trace_dataset.layer_df

        # Fit VSM Model
        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.TRAIN: dataset, DatasetRole.EVAL: dataset})
        trainer = VSMTrainer(trainer_dataset_manager=trainer_dataset_manager)
        trainer.perform_training()

        # Extract entities
        concepts = trainer.model.vocabulary_.keys()
        frequent_concepts = {word: trainer.model.idf_[word_idx] for word, word_idx in trainer.model.vocabulary_.items()}
        frequent_concepts = sorted(frequent_concepts.items(), key=lambda t: t[1], reverse=False)
        concepts = [c[0] for c in frequent_concepts[:10] if c[0] not in StrUtil.STOP_WORDS]
        # concepts = ["create", "edit", "retrieve", "update", "delete"]
        # Create concept map
        artifacts = artifact_df.to_artifacts()
        artifact2concepts = {a[ArtifactKeys.ID]: [] for a in artifacts}
        concept2artifacts = {c: [] for c in concepts}
        for artifact in artifacts:
            content = Artifact.get_summary_or_content(artifact).lower()
            for concept in concepts:
                if concept in content:
                    concept2artifacts[concept].append(artifact)
                    artifact2concepts[artifact[ArtifactKeys.ID]].append(concept)

        # Trace
        id2trace = {}
        for child_type, parent_type in layer_df.as_list():
            parent_artifacts = dataset.artifact_df.get_artifacts_by_type(parent_type).to_artifacts()

            for artifact in parent_artifacts:
                artifact_id = artifact[ArtifactKeys.ID]
                artifact_concepts = artifact2concepts[artifact_id]
                artifact_neighborhood = {a[ArtifactKeys.ID]: a for concept in artifact_concepts for a in concept2artifacts[concept]}
                artifact_candidates = [a for a in artifact_neighborhood.values() if a['layer_id'] == child_type]
                for candidate in artifact_candidates:
                    t_id = TraceDataFrame.generate_link_id(source_id=candidate[ArtifactKeys.ID], target_id=artifact_id)
                    id2trace[t_id] = Trace(id=t_id, source=candidate, target=artifact_id, score=1)

        scores = []
        for t_id in dataset.trace_df.index:
            score = id2trace[t_id][TraceKeys.SCORE] if t_id in id2trace else 0
            scores.append(score)

        # Evaluate
        metrics_manager = MetricsManager(dataset.trace_df, trace_predictions=scores)
        metrics = metrics_manager.eval(SupportedTraceMetric.get_keys())

        print("Metrics:", json.dumps(metrics, indent=4))
