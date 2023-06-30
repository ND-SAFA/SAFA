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


class RankingJob(LLMJob):
    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, dataset_role: DatasetRole = DatasetRole.EVAL):
        super().__init__(trainer_dataset_manager, task=TrainerTask.PREDICT)
        self.dataset_role = dataset_role

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        dataset: TraceDataset = self.trainer_dataset_manager[self.dataset_role]
        artifact_map = DataStructureUtil.create_artifact_map(dataset.artifact_df)

        # TODO: Deal with multi-layer
        parent_type, child_type = RankingUtil.get_parent_child_types(dataset.artifact_df)

        parent_ids = list(dataset.artifact_df.filter_by_type(parent_type).index)
        children_ids = list(dataset.artifact_df.filter_by_type(child_type).index)
        parent2children = {p_id: children_ids for p_id in parent_ids}

        predicted_entries = self.get_ranking_entries(parent_ids, parent2children, artifact_map)

        RankingUtil.calculate_ranking_metrics(dataset, predicted_entries)

        return TracePredictionOutput(prediction_entries=predicted_entries)

    @staticmethod
    def get_ranking_entries(parent_ids: List[str], parent2children: Dict[str, List[str]], artifact_map: Dict[str, str]) -> List[
        TracePredictionEntry]:
        predicted_entries = []
        batched_ranked_children = RankingUtil.rank_children(parent_ids, parent2children, artifact_map)

        for i, ranked_children in enumerate(batched_ranked_children):
            parent_id = parent_ids[i]
            target_predicted_entries = RankingUtil.parse_ranking_response(parent_id, ranked_children)
            predicted_entries.extend(target_predicted_entries)
        return predicted_entries
