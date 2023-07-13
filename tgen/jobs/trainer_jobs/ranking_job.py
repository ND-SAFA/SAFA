import os.path
from typing import Dict, List, Optional, Tuple, Union

from tgen.constants.tgen_constants import DEFAULT_SORTING_ALGORITHM
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_pipeline import ArtifactRankingPipeline
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry, TracePredictionOutput
from tgen.util.data_structure_util import DataStructureUtil
from tgen.util.ranking_util import RankingUtil


class RankingJob(AbstractJob):
    """
    Uses large claude to rank all source artifacts.
    """

    def __init__(self, dataset_creator: AbstractDatasetCreator = None, artifact_df: ArtifactDataFrame = None,
                 sorter: str = DEFAULT_SORTING_ALGORITHM, select_top_predictions: bool = True, ranking_args: Dict = None,
                 layer_ids: Tuple[str, str] = None):
        """
        Uses dataset defined by role to sort and rank with big claude.
        :param dataset_creator: Creates the dataset to rank.
        :param artifact_df: DataFrame containing sources and targets.
        :param sorter: The sorting function to feed big claude with.
        """
        super().__init__()
        assert dataset_creator is None or artifact_df is None, "Cannot define both dataset creator and artifact df."
        self.dataset_creator = dataset_creator
        self.sorter = sorter
        self.select_top_predictions = select_top_predictions
        self.ranking_args = ranking_args if ranking_args else {}
        self.artifact_df = artifact_df
        self.layer_ids = layer_ids
        self.project_name = 'DEFAULT' if self.dataset_creator is None else self.dataset_creator.get_name()
        if self.artifact_df is not None:
            assert self.layer_ids is not None, "Please define the layers to trace."

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Sorts children artifacts then ranks them with big claude.
        :param kwargs: Additional keyword arguments.
        :return:
        """
        tracing_types, artifact_df, dataset = self.construct_tracing_request()
        artifact_map = DataStructureUtil.create_artifact_map(artifact_df)

        global_predictions = []
        for tracing_type in tracing_types:
            parent_type, child_type = tracing_type
            parent_ids = list(artifact_df.get_type(parent_type).index)
            children_ids = list(artifact_df.get_type(child_type).index)
            predicted_entries = self.creating_ranking_predictions(parent_ids, children_ids, artifact_map)
            if self.select_top_predictions:
                predicted_entries = RankingUtil.select_predictions(predicted_entries, **self.ranking_args)
            global_predictions.extend(predicted_entries)

        if dataset is not None:
            RankingUtil.calculate_ranking_metrics(dataset, global_predictions)

        return TracePredictionOutput(prediction_entries=global_predictions)

    def construct_tracing_request(self) -> Tuple[List[Tuple[str, str]], ArtifactDataFrame, Optional[TraceDataset]]:
        """
        Reads dataset and constructs what layers will be traced.
        :return: The tracing requests, the artifact data frame, and optional dataset.
        """
        dataset: Optional[TraceDataset] = None
        if self.dataset_creator:
            dataset: TraceDataset = self.dataset_creator.create()
            artifact_df = dataset.artifact_df
            tracing_types = dataset.get_parent_child_types()
        else:
            assert self.layer_ids is not None
            artifact_df = self.artifact_df
            tracing_types = [self.layer_ids]
        return tracing_types, artifact_df, dataset

    def creating_ranking_predictions(self, parent_ids: List[str], children_ids: List[str], artifact_map: Dict[str, str]) -> List[
        TracePredictionEntry]:
        """
        Performs ranking and parses the responses into children ids.
        :param parent_ids: The parent ids to compare to children.
        :param children_ids: List of children ids to compare to parents.
        :param artifact_map: The map of artifact ids to body.
        :return: Prediction entries.
        """
        predicted_entries = []
        export_dir = os.path.expanduser(f"~/desktop/checkpoints/{self.project_name}")
        os.makedirs(export_dir, exist_ok=True)
        pipeline_args = RankingArgs(export_dir=export_dir,
                                    artifact_map=artifact_map,
                                    parent_ids=parent_ids,
                                    children_ids=children_ids,
                                    sorter=self.sorter)
        pipeline = ArtifactRankingPipeline(pipeline_args)
        parent2rankings = pipeline.run()

        for parent_id, ranked_children in parent2rankings.items():
            target_predicted_entries = RankingUtil.create_ranking_predictions(parent_id, ranked_children)
            predicted_entries.extend(target_predicted_entries)

        return predicted_entries
