from typing import List, Union

from tgen.common.util.pipeline_util import PipelineUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class InitializeDatasetStep(AbstractPipelineStep[HGenArgs, HGenState]):
    HGEN_SECTION_TITLE = "Hgen"

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Gets the original source datasets used for the generation
        :param args: The arguments and current state of HGEN.
        :param state: The state of HGEN.
        :return: The original dataset and a dataset with only the source layer
        """
        original_dataset_complete = args.dataset
        PipelineUtil.save_dataset_checkpoint(original_dataset_complete, state.export_dir, filename="initial_dataset_with_sources")

        source_layer_only_dataset = self._create_dataset_with_single_layer(original_dataset_complete.artifact_df, args.source_layer_id)

        state.source_dataset = source_layer_only_dataset
        state.original_dataset = original_dataset_complete

    @staticmethod
    def _create_dataset_with_single_layer(original_artifact_df: ArtifactDataFrame, layer_ids: Union[str, List[str]]) -> PromptDataset:
        """
        Creates a trace dataset for a single layer
        :param original_artifact_df: A dataframe containing artifacts including those for the layer
        :param layer_ids: ID of the layer to construct a dataset for
        :return: The trace dataset
        """
        if isinstance(layer_ids, str):
            layer_ids = [layer_ids]
        artifact_types = original_artifact_df.get_artifact_types()
        source_artifact_df = ArtifactDataFrame()
        for layer_id in layer_ids:
            if layer_id not in artifact_types:
                raise NameError(f"source_layer_id ({layer_id}) does not match any of {artifact_types}.")
            layer_artifact_df = original_artifact_df.get_type(layer_id)
            source_artifact_df = ArtifactDataFrame.concat(source_artifact_df, layer_artifact_df)
        return PromptDataset(artifact_df=source_artifact_df)
