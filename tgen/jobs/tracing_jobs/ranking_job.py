import os

from typing import Dict, List, Tuple, Union

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.ranking_constants import DEFAULT_SELECT_TOP_PREDICTIONS
from tgen.common.logging.logger_manager import logger
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.exporters.prompt_dataset_exporter import PromptDatasetExporter
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.pipeline.abstract_pipeline import AbstractPipeline
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.supported_ranking_pipelines import SupportedRankingPipelines

DATA_TOO_LITTLE_INPUTS = "Missing required dataset_creator or artifact_df + layer_ids."
DATA_TOO_MANY_INPUTS = "Expected only one of dataset_creator or artifact_df + layer_ids to be defined."


class RankingJob(AbstractJob):
    """
    Uses large claude to rank all source artifacts.
    """

    def __init__(self, job_args: JobArgs,
                 ranking_pipeline: SupportedRankingPipelines = SupportedRankingPipelines.LLM, layer_ids: Tuple[str, str] = None,
                 select_top_predictions: bool = DEFAULT_SELECT_TOP_PREDICTIONS, **kwargs):
        """
        Uses dataset defined by role to sort and rank with big claude.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param select_top_predictions: Whether to select the top predictions
        :param layer_ids: The layers to rank between.
        :param ranking_pipeline: The pipeline used to rank children to each parent.
        """
        super().__init__(job_args, require_data=True)
        self.select_top_predictions = select_top_predictions
        self.ranking_pipeline = ranking_pipeline
        self.layer_ids = layer_ids
        self.ranking_kwargs = kwargs
        assert self.job_args.dataset.trace_dataset is not None or self.layer_ids, "Must specify parent-child layers or provide trace dataset"

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Sorts children artifacts then ranks them with big claude.
        :param kwargs: Additional keyword arguments.
        :return:
        """
        tracing_types = self.job_args.dataset.trace_dataset.get_parent_child_types() if not self.layer_ids else [self.layer_ids]
        # Predict
        global_predictions = []
        for tracing_type in tracing_types:
            predicted_entries = self.trace_layer(self.job_args.dataset, tracing_type)
            global_predictions.extend(predicted_entries)

        self.optional_eval(self.job_args.dataset.trace_dataset, global_predictions)

        return TracePredictionOutput(prediction_entries=global_predictions)

    def trace_layer(self, layer_dataset: PromptDataset, types_to_trace: Tuple[str, str]):
        """
        Traces the between the child-parent artifact types.
        :param layer_dataset: The dataset containing artifacts to trace.
        :param types_to_trace: The child-parent layers being traced.
        :return:
        """
        full_dataset = self.job_args.dataset
        selected_artifacts = layer_dataset.artifact_df.get_artifacts_by_type(types_to_trace)
        parent_type, child_type = types_to_trace
        parent_ids = list(layer_dataset.artifact_df.get_artifacts_by_type(parent_type).index)
        children_ids = list(layer_dataset.artifact_df.get_artifacts_by_type(child_type).index)

        if not self.select_top_predictions:
            DictUtil.update_kwarg_values(self.ranking_kwargs, selection_method=None)
        export_dir = DictUtil.get_kwarg_values(self.ranking_kwargs, pop=True, export_dir=EMPTY_STRING)
        if export_dir and not export_dir.endswith(RankingJob._get_run_dir(child_type, parent_type)):
            export_dir = FileUtil.safely_join_paths(export_dir, RankingJob._get_run_dir(child_type, parent_type))
        layer_dataset = PromptDataset(artifact_df=selected_artifacts, project_summary=full_dataset.project_summary)
        pipeline_args = RankingArgs(dataset=layer_dataset,
                                    parent_ids=parent_ids,
                                    children_ids=children_ids,
                                    export_dir=export_dir,
                                    types_to_trace=types_to_trace,
                                    **self.ranking_kwargs)
        logger.info(f"Starting to trace: {pipeline_args.run_name}")

        pipeline: AbstractPipeline[RankingArgs, RankingState] = self.ranking_pipeline.value(pipeline_args)
        pipeline.run()
        selected_entries = pipeline.state.get_current_entries()
        has_positive_links = full_dataset.trace_dataset and len(full_dataset.trace_df.get_links_with_label(1)) > 1
        if has_positive_links:
            for entry in pipeline.state.get_current_entries():
                trace_id = self.get_trace_id_from_entry(entry)
                trace_entry = full_dataset.trace_df.loc[trace_id]
                label = trace_entry[TraceKeys.LABEL.value]
                entry[TraceKeys.LABEL] = label
                full_dataset.trace_df.update_value(TraceKeys.SCORE, trace_id, entry[TraceKeys.SCORE])
                if TraceKeys.EXPLANATION in entry:
                    full_dataset.trace_df.update_value(TraceKeys.EXPLANATION, trace_id, entry[TraceKeys.EXPLANATION])

        if export_dir:
            PromptDatasetExporter(export_path=os.path.join(export_dir, "final_dataset"),
                                  dataset=full_dataset, trace_dataset_exporter_type=SafaExporter).export()
        return selected_entries

    @staticmethod
    def get_trace_id_from_entry(entry: EnumDict) -> int:
        """
        Gets the trace id from teh entry
        :param entry: The prediction entry
        :return: The trace id for the entry
        """
        return TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE], entry[TraceKeys.TARGET])

    @staticmethod
    def optional_eval(dataset: TraceDataset, predictions: List) -> None:
        """
        Evaluates the results of the predictions if the dataset contains positive labeled links.
        :param dataset: The dataset representing the ground truth.
        :param predictions: The predictions for the links in the dataset.
        :return: None
        """
        if dataset is None or dataset.trace_df is None or len(dataset.trace_df.get_links_with_label(1)) == 0:
            return
        RankingUtil.evaluate_trace_predictions(dataset.trace_df, predictions)

    @staticmethod
    def _get_run_dir(child_type: str, parent_type: str) -> str:
        """
        Get the name of this run's directory
        :param child_type: The name of the child type
        :param parent_type: The name of the parent type
        :return: The name of the run's directory
        """
        return f"{child_type}_{parent_type}"
