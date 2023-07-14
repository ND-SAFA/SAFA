import os.path
import re
from typing import Dict, List, Optional, Tuple, Union

from tgen.constants.tgen_constants import DEFAULT_MAX_N_CHILDREN, DEFAULT_RANKING_MODEL, DEFAULT_SORTING_ALGORITHM, \
    GENERATE_SUMMARY_DEFAULT
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_pipeline import ArtifactRankingPipeline
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.util.data_structure_util import DataStructureUtil
from tgen.util.ranking_util import RankingUtil


class RankingJob(AbstractJob):
    """
    Uses large claude to rank all source artifacts.
    """

    def __init__(self, dataset_creator: AbstractDatasetCreator = None, artifact_df: ArtifactDataFrame = None,
                 sorter: str = DEFAULT_SORTING_ALGORITHM, select_top_predictions: bool = True, ranking_args: Dict = None,
                 layer_ids: Tuple[str, str] = None, generate_summary: bool = GENERATE_SUMMARY_DEFAULT, project_summary: str = None,
                 max_children_per_query: int = DEFAULT_MAX_N_CHILDREN, model: str = DEFAULT_RANKING_MODEL):
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
        self.generate_summary = generate_summary
        self.project_summary = project_summary
        self.model = model
        self.max_children_per_query = max_children_per_query
        if self.artifact_df is not None:
            assert self.layer_ids is not None, "Please define the layers to trace."

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Sorts children artifacts then ranks them with big claude.
        :param kwargs: Additional keyword arguments.
        :return:
        """
        export_dir = os.path.expanduser(f"~/desktop/checkpoints/{self.project_name}")
        tracing_types, artifact_df, dataset = self.construct_tracing_request()
        artifact_map = DataStructureUtil.create_artifact_map(artifact_df)
        artifact_map = self.process_newlines(artifact_map)

        # Predict
        global_predictions = []
        for tracing_type in tracing_types:
            predicted_entries = self.trace_layer(artifact_df, artifact_map, export_dir, tracing_type)
            global_predictions.extend(predicted_entries)

        self.optional_eval(dataset, global_predictions)

        return TracePredictionOutput(prediction_entries=global_predictions)

    def trace_layer(self, artifact_df: ArtifactDataFrame, artifact_map: Dict[str, str], export_dir, types_to_trace: Tuple[str, str]):
        parent_type, child_type = types_to_trace
        parent_ids = list(artifact_df.get_type(parent_type).index)
        children_ids = list(artifact_df.get_type(child_type).index)
        pipeline_args = RankingArgs(export_dir=export_dir,
                                    artifact_map=artifact_map,
                                    parent_ids=parent_ids,
                                    children_ids=children_ids,
                                    sorter=self.sorter,
                                    generate_summary=self.generate_summary,
                                    project_summary=self.project_summary,
                                    max_children_per_query=self.max_children_per_query,
                                    model=self.model)
        os.makedirs(pipeline_args.export_dir, exist_ok=True)
        pipeline = ArtifactRankingPipeline(pipeline_args)
        parent2rankings = pipeline.run()
        parent2rankings = {p_id: pipeline_args.children_ids for p_id in pipeline_args.parent_ids}
        predicted_entries = RankingUtil.ranking_to_predictions(parent2rankings)
        if self.select_top_predictions:
            predicted_entries = RankingUtil.select_predictions(predicted_entries, **self.ranking_args)
        return predicted_entries

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

    @staticmethod
    def optional_eval(dataset, predictions):
        if dataset is None:
            return
        RankingUtil.calculate_ranking_metrics(dataset, predictions)

    @staticmethod
    def process_newlines(dictionary):
        processed_dict = {}
        for key, value in dictionary.items():
            processed_value = re.sub(r'\n{2,}', '\n', value)
            processed_dict[key] = processed_value
        return processed_dict
