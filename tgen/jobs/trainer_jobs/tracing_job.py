from typing import Dict, List, Union

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.data_structure_util import DataStructureUtil
from tgen.util.ranking_util import RankingUtil


class TracingJob(LLMJob):
    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, dataset_role: DatasetRole = DatasetRole.EVAL):
        super().__init__(trainer_dataset_manager, task=TrainerTask.PREDICT)
        self.dataset_role = dataset_role

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        THRESHOLD = 0.5
        dataset: TraceDataset = self.trainer_dataset_manager[self.dataset_role]
        artifact_map = DataStructureUtil.create_artifact_map(dataset.artifact_df)

        prediction_output: TracePredictionOutput = super()._run(**kwargs)
        entries = prediction_output.prediction_entries
        entries = [entry for entry in entries if entry["score"] >= THRESHOLD]

        target2entries: Dict[str, List[TracePredictionEntry]] = self.create_id_to_entries(entries, "target")
        parent_ids = list(target2entries.keys())
        parent2children: Dict[str, List[str]] = {target: [t["source"] for t in entries] for target, entries in target2entries.items()}

        batch_ranked_targets = RankingUtil.rank_children(parent_ids, parent2children, artifact_map)

        predicted_entries = []

        for i, ranked_sources in enumerate(batch_ranked_targets):
            target = parent_ids[i]
            target_entries = target2entries[target]
            target_predicted_entries = RankingUtil.parse_ranking_response(target, ranked_sources, target_entries)
            predicted_entries.extend(target_predicted_entries)
        RankingUtil.calculate_ranking_metrics(dataset, predicted_entries)

        return TracePredictionOutput(prediction_entries=predicted_entries)

    @staticmethod
    def create_id_to_entries(entries, artifact_key: str):
        id2entries: Dict[str, List[Dict]] = {}
        for entry in entries:
            artifact_id = entry[artifact_key]
            if artifact_id not in id2entries:
                id2entries[artifact_id] = []
            id2entries[artifact_id].append(entry)

        id2entries = {t_id: sorted(entries, key=lambda t: t["score"], reverse=True) for t_id, entries in id2entries.items()}
        return id2entries
