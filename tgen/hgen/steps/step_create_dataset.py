import uuid
from typing import List

from tgen.constants.prediction_constants import HGEN_TOP_PREDICTION_MIN_THRESHOLD
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs, HGenState
from tgen.hgen.hgen_util import create_artifact_df_from_generated_artifacts, save_dataset_checkpoint, SAVE_DATASET_DIRNAME
from tgen.jobs.trainer_jobs.ranking_job import RankingJob
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.enum_util import EnumDict
from tgen.util.logging.logger_manager import logger
from tgen.util.status import Status


class CreateHGenDataset(AbstractPipelineStep[HGenArgs, HGenState]):

    def run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates a dataset containing original artifacts, generated upper level artifacts, and trace links between them.
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """
        artifact_generations = state.refined_content
        original_dataset_complete = state.original_dataset
        export_path = state.export_path

        original_artifact_df = original_dataset_complete.artifact_df
        original_trace_dataset = original_dataset_complete.trace_dataset if isinstance(original_dataset_complete,
                                                                                       PromptDataset) else original_dataset_complete
        original_trace_df, original_layer_df = None, None
        if original_trace_dataset:
            original_trace_df = original_trace_dataset.trace_df
            original_layer_df = original_trace_dataset.layer_df

        target_layer_id = CreateHGenDataset._get_target_layer_id(args, original_dataset_complete)

        new_artifact_df = create_artifact_df_from_generated_artifacts(args, artifact_generations, target_layer_id)
        save_dataset_checkpoint(PromptDataset(artifact_df=new_artifact_df), export_path, filename="generated_artifacts_only")

        new_layer_df = CreateHGenDataset._create_layer_df_with_generated_artifacts(args, target_layer_id)
        combined_artifact_df = ArtifactDataFrame.concat(original_artifact_df, new_artifact_df)
        new_trace_df = CreateHGenDataset._create_trace_df_with_generated_artifacts(args, combined_artifact_df)
        save_dataset_checkpoint(TraceDataset(artifact_df=new_artifact_df, trace_df=new_trace_df, layer_df=new_layer_df),
                                export_path, filename="generated_dataset_checkpoint")

        new_trace_df = TraceDatasetCreator.generate_negative_links(layer_mapping_df=new_layer_df,
                                                                   artifact_df=combined_artifact_df, trace_df=new_trace_df)
        final_trace_df = TraceDataFrame.concat(original_trace_df, new_trace_df) if original_trace_df is not None else new_trace_df
        final_layer_df = LayerDataFrame.concat(original_layer_df, new_layer_df) if original_layer_df is not None else new_layer_df

        dataset = TraceDataset(combined_artifact_df, final_trace_df, final_layer_df)

        save_path = save_dataset_checkpoint(dataset, export_path, filename=SAVE_DATASET_DIRNAME)
        save_dataset_checkpoint(dataset, save_path, filename="safa", exporter_class=SafaExporter)
        state.dataset = dataset

    @staticmethod
    def _get_target_layer_id(hgen_args: HGenArgs, original_dataset_complete: PromptDataset) -> str:
        """
        Gets the id of the new target layer
        :param original_dataset_complete: The dataset containing source artifacts
        :return: The id of the new target layer
        """
        layer_id = hgen_args.target_type
        if hgen_args.target_type in original_dataset_complete.artifact_df[ArtifactKeys.LAYER_ID].values:
            layer_id = f"{layer_id}_{uuid.uuid4()}"
        return layer_id

    @staticmethod
    def _create_layer_df_with_generated_artifacts(hgen_args: HGenArgs, target_layer_id: str) -> LayerDataFrame:
        """
        Creates a layer dataframe connecting the original lower-level artifacts with the newly generated upper-level artifacts
        :param target_layer_id: The id of the new target layer
        :return: The dataframe with the new layer ids added.
        """
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [hgen_args.source_layer_id], LayerKeys.TARGET_TYPE: [target_layer_id]})
        return layer_df

    @staticmethod
    def _create_trace_df_with_generated_artifacts(hgen_args: HGenArgs, artifact_df: ArtifactDataFrame) -> TraceDataFrame:
        """
        Creates a dataframe of traces including the new trace links between the original lower-level artifacts
        and the newly generated upper-level artifacts
        :return: The dataframe containing new and old trace links
        """
        logger.info(f"Predicting links between {hgen_args.target_type} and {hgen_args.source_layer_id}\n")
        tracing_job = RankingJob(artifact_df=artifact_df, ranking_args={"min_threshold": HGEN_TOP_PREDICTION_MIN_THRESHOLD},
                                 layer_ids=(hgen_args.target_type, hgen_args.source_layer_id))
        result = tracing_job.run()
        if result.status != Status.SUCCESS:
            raise Exception(f"Trace link generation failed: {result.body}")
        trace_predictions: List[TracePredictionEntry] = tracing_job.run().body.prediction_entries
        traces = {}
        for entry in trace_predictions:
            link = EnumDict({
                **entry,
                TraceKeys.SOURCE: entry[TraceKeys.SOURCE.value],
                TraceKeys.TARGET: entry[TraceKeys.TARGET.value],
                TraceKeys.LABEL: 1
            })
            DataFrameUtil.append(traces, link)
        return TraceDataFrame(traces)
