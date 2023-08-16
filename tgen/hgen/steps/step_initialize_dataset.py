from typing import Any

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs, HGenState
from tgen.hgen.hgen_util import save_dataset_checkpoint
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class InitializeDatasetStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Gets the original source datasets used for the generation
        :param args: The arguments and current state of HGEN.
        :param state: The state of HGEN.
        :return: The original dataset and a dataset with only the source layer
        """
        export_path = state.export_path
        original_dataset_complete = args.dataset_creator_for_sources.create() if args.dataset_for_sources is None \
            else args.dataset_for_sources
        save_dataset_checkpoint(original_dataset_complete, export_path, filename="initial_dataset_with_sources")
        source_layer_only_dataset = self._create_dataset_with_single_layer(original_dataset_complete.artifact_df,
                                                                           args.source_layer_id)
        state.source_dataset = source_layer_only_dataset
        state.original_dataset = original_dataset_complete

    @staticmethod
    def _create_dataset_with_single_layer(original_artifact_df: ArtifactDataFrame, layer_id: Any) -> PromptDataset:
        """
        Creates a trace dataset for a single layer
        :param original_artifact_df: A dataframe containing artifacts including those for the layer
        :param layer_id: ID of the layer to construct a dataset for
        :return: The trace dataset
        """
        layer_artifact_df = original_artifact_df.get_type(layer_id)
        if len(layer_artifact_df) == 0:
            raise NameError(f"source_layer_id: {layer_id} does not match any artifacts in the dataset")
        return PromptDataset(artifact_df=layer_artifact_df)
