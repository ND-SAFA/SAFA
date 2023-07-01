from typing import Dict, List, Union

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.ranking.pipeline.sort_step import registered_sorters
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.data_structure_util import DataStructureUtil
from tgen.util.ranking_util import RankingUtil


class RankingJob(LLMJob):
    """
    Uses large claude to rank all source artifacts.
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, dataset_role: DatasetRole = DatasetRole.EVAL,
                 sorter: str = "vsm"):
        """
        Uses dataset defined by role to sort and rank with big claude.
        :param trainer_dataset_manager: The manager of the dataset.
        :param dataset_role: The role to evaluate on.
        :param sorter: The sorting function to feed big claude with.
        """
        super().__init__(trainer_dataset_manager, task=TrainerTask.PREDICT)
        self.dataset_role = dataset_role
        self.sorter = sorter

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Runs sorting and ranking.
        :param kwargs: Additional keyword arguments.
        :return:
        """
        dataset: TraceDataset = self.trainer_dataset_manager[self.dataset_role]
        artifact_map = DataStructureUtil.create_artifact_map(dataset.artifact_df)

        # TODO: Deal with multi-layer
        parent_type, child_type = dataset.artifact_df.get_parent_child_types()

        parent_ids = list(dataset.artifact_df.get_type(parent_type).index)
        children_ids = list(dataset.artifact_df.get_type(child_type).index)
        parent2children = {p_id: children_ids for p_id in parent_ids}

        predicted_entries = self.get_ranking_entries(parent_ids, parent2children, artifact_map)

        RankingUtil.calculate_ranking_metrics(dataset, predicted_entries)

        return TracePredictionOutput(prediction_entries=predicted_entries)

    def get_ranking_entries(self, parent_ids: List[str], parent2children: Dict[str, List[str]], artifact_map: Dict[str, str]) -> List[
        TracePredictionEntry]:
        """
        Performs ranking and parses the responses into children ids.
        :param parent_ids: The parent artifact ids.
        :param parent2children: Map of children related to each parent.
        :param artifact_map: The map of artifact ids to body.
        :return: Prediction entries.
        """
        predicted_entries = []
        sorting_function = registered_sorters[self.sorter]
        parent2rankings = RankingUtil.rank_children(parent_ids, parent2children, artifact_map, sorter=sorting_function)

        for parent_id, ranked_children in parent2rankings.items():
            target_predicted_entries = RankingUtil.create_ranking_predictions(parent_id, ranked_children)
            predicted_entries.extend(target_predicted_entries)
        return predicted_entries
