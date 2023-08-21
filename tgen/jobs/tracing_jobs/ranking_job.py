from typing import Dict, List, Optional, Tuple, Union

from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.ranking_util import RankingUtil
from tgen.constants.ranking_constants import DEFAULT_SELECT_TOP_PREDICTIONS, DEFAULT_THRESHOLD_SCORE
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.ranking.supported_ranking_pipelines import SupportedRankingPipelines
from tgen.state.pipeline.abstract_pipeline import AbstractPipeline

DATA_TOO_LITTLE_INPUTS = "Missing required dataset_creator or artifact_df + layer_ids."
DATA_TOO_MANY_INPUTS = "Expected only one of dataset_creator or artifact_df + layer_ids to be defined."


class RankingJob(AbstractJob):
    """
    Uses large claude to rank all source artifacts.
    """

    def __init__(self, dataset_creator: AbstractDatasetCreator = None, artifact_df: ArtifactDataFrame = None,
                 ranking_pipeline: SupportedRankingPipelines = SupportedRankingPipelines.LLM, layer_ids: Tuple[str, str] = None,
                 select_top_predictions: bool = DEFAULT_SELECT_TOP_PREDICTIONS, project_summary: str = None, **kwargs):
        """
        Uses dataset defined by role to sort and rank with big claude.
        :param dataset_creator: Creates the dataset to rank.
        :param artifact_df: DataFrame containing sources and targets.
        :param sorter: The sorting function to feed big claude with.
        :param select_top_predictions: Whether to select the top predictions
        :param layer_ids
        """
        super().__init__()
        assert dataset_creator is not None or (artifact_df is not None and layer_ids is not None), DATA_TOO_LITTLE_INPUTS
        assert dataset_creator is None or artifact_df is None, DATA_TOO_MANY_INPUTS
        self.dataset_creator = dataset_creator
        self.select_top_predictions = select_top_predictions
        self.ranking_pipeline = ranking_pipeline
        self.artifact_df = artifact_df
        self.layer_ids = layer_ids
        self.ranking_kwargs = kwargs
        self.project_summary = project_summary
        self.dataset: TraceDataset = None
        if self.artifact_df is not None:
            assert self.layer_ids is not None, "Please define the layers to trace."

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Sorts children artifacts then ranks them with big claude.
        :param kwargs: Additional keyword arguments.
        :return:
        """
        tracing_types, artifact_df, dataset = self.construct_tracing_request()
        self.dataset = dataset
        # Predict
        global_predictions = []
        for tracing_type in tracing_types:
            predicted_entries = self.trace_layer(artifact_df, tracing_type)
            global_predictions.extend(predicted_entries)

        self.optional_eval(dataset, global_predictions)

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

    def trace_layer(self, artifact_df: ArtifactDataFrame, types_to_trace: Tuple[str, str]):
        """
        Traces the between the child-parent artifact types.
        :param artifact_df: The artifact dataframe containing artifacts ids.
        :param artifact_map: Map of artifact id to content.
        :param types_to_trace: The child-parent layers being traced.
        :return:
        """
        parent_type, child_type = types_to_trace
        parent_ids = list(artifact_df.get_type(parent_type).index)
        children_ids = list(artifact_df.get_type(child_type).index)
        run_name = f"{child_type}2{parent_type}"
        logger.info(f"Starting to trace: {run_name}")

        pipeline_args = RankingArgs(run_name=run_name,
                                    artifact_df=artifact_df,
                                    parent_ids=parent_ids,
                                    children_ids=children_ids,
                                    project_summary=self.project_summary,
                                    **self.ranking_kwargs)
        pipeline: AbstractPipeline[RankingArgs, RankingState] = self.ranking_pipeline.value(pipeline_args)
        predicted_entries = pipeline.run()
        self.project_summary = pipeline.state.project_summary
        for entry in predicted_entries:
            trace_id = TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE.value], entry[TraceKeys.TARGET.value])
            trace_entry = self.dataset.trace_df.loc[trace_id]
            label = trace_entry[TraceKeys.LABEL.value]
            entry[TraceKeys.LABEL.value] = label

        if self.select_top_predictions:
            predicted_entries = [e for e in predicted_entries if e[TraceKeys.SCORE.value] >= DEFAULT_THRESHOLD_SCORE]
        return predicted_entries

    @staticmethod
    def optional_eval(dataset, predictions):
        if dataset is None:
            return
        RankingUtil.evaluate_trace_predictions(dataset.trace_df, predictions)
