from typing import Dict, List, Tuple, Union

from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.ranking.steps.sort_step import registered_sorters
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.util.data_structure_util import DataStructureUtil
from tgen.util.ranking_util import RankingUtil


class RankingJob(AbstractJob):
    """
    Uses large claude to rank all source artifacts.
    """

    def __init__(self, dataset_creator: AbstractDatasetCreator = None, artifact_df: ArtifactDataFrame = None,
                 sorter: str = "vsm", select_top_predictions: bool = True, ranking_args: Dict = None,
                 layer_ids: Tuple[str, str] = None):
        """
        Uses dataset defined by role to sort and rank with big claude.
        :param dataset_creator: Creates the dataset to rank.
        :param artifact_df: DataFrame containing sources and targets.
        :param sorter: The sorting function to feed big claude with.
        """
        assert dataset_creator is None or artifact_df is None, "Cannot define both dataset creator and artifact df."
        super().__init__()
        self.dataset_creator = dataset_creator
        self.artifact_df = artifact_df
        self.sorter = sorter
        self.select_top_predictions = select_top_predictions
        self.ranking_args = ranking_args if ranking_args else {}
        self.layer_ids = layer_ids

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Runs sorting and ranking.
        :param kwargs: Additional keyword arguments.
        :return:
        """
        dataset = None
        if self.dataset_creator:
            dataset_role = DatasetRole.EVAL
            trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=self.dataset_creator)
            dataset: TraceDataset = trainer_dataset_manager[dataset_role]
            artifact_df = dataset.artifact_df
        else:
            artifact_df = self.artifact_df
        artifact_map = DataStructureUtil.create_artifact_map(artifact_df)

        # TODO: Deal with multi-layer
        if self.layer_ids:
            parent_type, child_type = self.layer_ids
        else:
            parent_type, child_type = artifact_df.get_parent_child_types()

        parent_ids = list(artifact_df.get_type(parent_type).index)
        children_ids = list(artifact_df.get_type(child_type).index)
        parent2children = {p_id: children_ids for p_id in parent_ids}

        predicted_entries = self.creating_ranking_predictions(parent_ids, parent2children, artifact_map)
        if self.select_top_predictions:
            predicted_entries = RankingUtil.select_predictions(predicted_entries, **self.ranking_args)

        if dataset is not None:
            RankingUtil.calculate_ranking_metrics(dataset, predicted_entries)

        return TracePredictionOutput(prediction_entries=predicted_entries)

    def creating_ranking_predictions(self, parent_ids: List[str], parent2children: Dict[str, List[str]],
                                     artifact_map: Dict[str, str]) -> List[TracePredictionEntry]:
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
