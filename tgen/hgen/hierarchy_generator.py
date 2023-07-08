import os
import uuid
from typing import Any, Tuple

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.data.clustering.llm_clustering import LLMClustering
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_util import save_dataset_checkpoint
from tgen.hgen.steps.step_construct_questionnaire import construct_questionnaire
from tgen.hgen.steps.step_create_dataset import create_hgen_dataset
from tgen.hgen.steps.step_generate_artifact_content import generate_artifact_content
from tgen.hgen.steps.step_refine_output import refine_artifact_content
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.token_limits import ModelTokenLimits
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil


class HierarchyGenerator(BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """
    RES_TOKENS_MIN = 25000

    def __init__(self, args: HGenArgs):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        self.args = args
        self._set_max_tokens(self.args.hgen_llm_manager)

    def run(self) -> TraceDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """
        export_path = os.path.join(self.args.export_dir, str(uuid.uuid4())) if self.args.export_dir else None
        original_dataset_complete, source_layer_only_dataset = self._get_source_datasets_for_generation(export_path)

        self.args.state.export_path = export_path
        self.args.state.source_dataset = source_layer_only_dataset
        self.args.state.original_dataset = original_dataset_complete

        pipeline = [construct_questionnaire,
                    generate_artifact_content,
                    refine_artifact_content,
                    create_hgen_dataset]
        for step in pipeline:
            step(hgen_args=self.args)

        dataset = self.args.state.dataset
        assert dataset is not None, f"Final dataset is not set."
        return dataset

    def _get_source_datasets_for_generation(self, export_path: str = EMPTY_STRING) -> Tuple[PromptDataset, PromptDataset]:
        """
        Gets the original source datasets used for the generation
        :param export_path: The path to export checkpoints to
        :return: The original dataset and a dataset with only the source layer
        """
        original_dataset_complete = self.args.dataset_creator_for_sources.create() if self.args.dataset_for_sources is None \
            else self.args.dataset_for_sources
        save_dataset_checkpoint(original_dataset_complete, export_path, filename="initial_dataset_with_sources")
        source_layer_only_dataset = self._create_dataset_with_single_layer(original_dataset_complete.artifact_df,
                                                                           self.args.source_layer_id,
                                                                           original_dataset_complete.trace_dataset.trace_df
                                                                           if original_dataset_complete.trace_dataset else None)
        return original_dataset_complete, source_layer_only_dataset

    @staticmethod
    def _create_dataset_with_single_layer(original_artifact_df: ArtifactDataFrame, layer_id: Any,
                                          original_trace_df: TraceDataFrame = None) -> PromptDataset:
        """
        Creates a trace dataset for a single layer
        :param original_artifact_df: A dataframe containing artifacts including those for the layer
        :param layer_id: ID of the layer to construct a dataset for
        :param original_trace_df: A dataframe containing intra layer traces for the layer
        :return: The trace dataset
        """
        layer_artifact_df = original_artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] == layer_id)
        if len(layer_artifact_df) == 0:
            raise NameError(f"source_layer_id: {layer_id} does not match any artifacts in the dataset")
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [layer_id],
                                   LayerKeys.TARGET_TYPE: [layer_id]})
        layer_trace_df = TraceDataFrame() if original_trace_df is None else \
            TraceDataFrame(DataFrameUtil.filter_df_by_row(original_trace_df,
                                                          lambda row: row[TraceKeys.SOURCE.value] in layer_artifact_df
                                                                      and row[TraceKeys.TARGET.value] in layer_artifact_df))
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=layer_artifact_df, trace_df=layer_trace_df,
                                                               layer_mapping_df=layer_df)
        return PromptDataset(trace_dataset=TraceDataset(artifact_df=layer_artifact_df, trace_df=trace_df, layer_df=layer_df))

    @staticmethod
    def _update_trainer_args(trainer: AbstractTrainer, export_path: str) -> None:
        """
        Sets the output directory of the trainer's args to the export path
        :param trainer: The trainer to update output dir for
        :param export_path: The path to set the output dir to
        :return: None
        """
        if hasattr(trainer.trainer_args, "output_dir") and trainer.trainer_args.output_dir is None:
            trainer.trainer_args.output_dir = export_path
        if hasattr(trainer.trainer_args, "metrics"):
            trainer.trainer_args.metrics = []

    @staticmethod
    def _set_max_tokens(llm_manager: AbstractLLMManager) -> int:
        """
        Tries to find the optimal number of tokens to set for the model's response
        :param llm_manager: The LLM Manager being used for the clustering
        :return: The max tokens that the model was set to
        """
        model_token_limit = ModelTokenLimits.get_token_limit_for_model(llm_manager.llm_args.model)
        max_tokens = max(HierarchyGenerator.RES_TOKENS_MIN, int(model_token_limit * LLMClustering.PERC_TOKENS_FOR_RES))
        llm_manager.llm_args.set_max_tokens(max_tokens)
        return max_tokens
