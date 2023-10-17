import os
import uuid
from typing import List, Dict

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.ranking_constants import DEFAULT_HGEN_LINK_THRESHOLD
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.pipeline_util import PipelineUtil
from tgen.common.util.status import Status
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import TraceKeys, ArtifactKeys, LayerKeys
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import SAVE_DATASET_DIRNAME, HGenUtil
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateHGenDatasetStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates a dataset containing original artifacts, generated upper level artifacts, and trace links between them.
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """
        proj_path = os.path.join(args.load_dir, SAVE_DATASET_DIRNAME)
        export_path = state.export_dir

        if os.path.exists(proj_path):
            dataset = TraceDatasetCreator(DataFrameProjectReader(proj_path)).create()
        else:
            original_dataset_complete = state.original_dataset

            original_artifact_df = original_dataset_complete.artifact_df
            original_trace_dataset = original_dataset_complete.trace_dataset \
                if isinstance(original_dataset_complete, PromptDataset) else original_dataset_complete
            original_trace_df, original_layer_df = None, None
            if original_trace_dataset:
                original_trace_df = original_trace_dataset.trace_df
                original_layer_df = original_trace_dataset.layer_df

            target_layer_id = CreateHGenDatasetStep._get_target_layer_id(args, original_dataset_complete)

            generated_artifacts, predicted_links = list(state.refined_content.keys()), list(state.refined_content.values())
            new_artifact_df = HGenUtil.create_artifact_df_from_generated_artifacts(args, generated_artifacts, target_layer_id)
            artifact_id_to_link_predictions = {name: predicted_links[i] for i, name in enumerate(new_artifact_df.index)}
            PipelineUtil.save_dataset_checkpoint(PromptDataset(artifact_df=new_artifact_df), export_path,
                                                 filename="generated_artifacts_only")

            new_layer_df = CreateHGenDatasetStep._create_layer_df_with_generated_artifacts(args, target_layer_id)
            combined_artifact_df = ArtifactDataFrame.concat(original_artifact_df, new_artifact_df)
            new_trace_df = CreateHGenDatasetStep._create_trace_df_with_generated_artifacts(args, state, combined_artifact_df,
                                                                                           artifact_id_to_link_predictions)
            PipelineUtil.save_dataset_checkpoint(TraceDataset(artifact_df=new_artifact_df, trace_df=new_trace_df,
                                                              layer_df=new_layer_df),
                                                 export_path, filename="generated_dataset_checkpoint")

            new_trace_df = TraceDatasetCreator.generate_negative_links(layer_mapping_df=new_layer_df,
                                                                       artifact_df=combined_artifact_df, trace_df=new_trace_df)
            final_trace_df = TraceDataFrame.concat(original_trace_df, new_trace_df) if original_trace_df is not None else new_trace_df
            final_layer_df = LayerDataFrame.concat(original_layer_df, new_layer_df) if original_layer_df is not None else new_layer_df

            dataset = PromptDataset(trace_dataset=TraceDataset(combined_artifact_df, final_trace_df, final_layer_df),
                                    project_summary=args.dataset.project_summary)
        state.final_dataset = dataset

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
            hgen_args.target_type = layer_id
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
    def _create_trace_df_with_generated_artifacts(hgen_args: HGenArgs, hgen_state: HGenState,
                                                  artifact_df: ArtifactDataFrame,
                                                  artifact_id_to_link_predictions: Dict[str, List[str]]) -> TraceDataFrame:
        """
        Creates a dataframe of traces including the new trace links between the original lower-level artifacts
        and the newly generated upper-level artifacts
        :param hgen_args: The arguments to the hierarchy generator
        :param hgen_state: The current state of hgen
        :param artifact_df: The dataframe containing the generated artifacts
        :param artifact_id_to_link_predictions: A dictionary mapping artifact id to the links that were predicted for it
        :return: The dataframe containing new and old trace links
        """
        if not hgen_args.generate_trace_links:
            return TraceDataFrame()
        logger.info(f"Predicting links between {hgen_args.target_type} and {hgen_args.source_layer_id}\n")
        tracing_layers = (hgen_args.target_type, hgen_args.source_layer_id)  # parent, child
        tracing_job = RankingJob(dataset=PromptDataset(artifact_df=artifact_df, project_summary=hgen_args.dataset.project_summary),
                                 layer_ids=tracing_layers,
                                 export_dir=CreateHGenDatasetStep._get_ranking_dir(hgen_state.export_dir),
                                 load_dir=CreateHGenDatasetStep._get_ranking_dir(hgen_args.load_dir),
                                 link_threshold=DEFAULT_HGEN_LINK_THRESHOLD,
                                 pre_sorted_parent2children=artifact_id_to_link_predictions)
        result = tracing_job.run()
        if result.status != Status.SUCCESS:
            raise Exception(f"Trace link generation failed: {result.body}")
        trace_predictions: List[EnumDict] = result.body.prediction_entries
        traces = {}
        for entry in trace_predictions:
            link = EnumDict({
                **entry,
                TraceKeys.SOURCE: entry[TraceKeys.SOURCE],
                TraceKeys.TARGET: entry[TraceKeys.TARGET],
                TraceKeys.LABEL: 1
            })
            DataFrameUtil.append(traces, link)
        return TraceDataFrame(traces)

    @staticmethod
    def _get_ranking_dir(directory: str) -> str:
        """
        Get the directory for ranking job
        :param directory: The main directory used by hgen
        :return: The full path
        """
        return os.path.join(directory, "ranking") if directory else EMPTY_STRING
