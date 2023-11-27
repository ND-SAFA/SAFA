from tgen.common.util.pipeline_util import PipelineUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


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

        artifact_types = set(original_dataset_complete.artifact_df.get_artifact_types())
        missing_types = [s for s in args.source_layer_ids if s not in artifact_types]
        assert len(missing_types) == 0, f"Unknown artifact types: {missing_types}. Should be one of {artifact_types}."

        source_artifact_df = original_dataset_complete.artifact_df.get_type(args.source_layer_ids)
        source_layer_only_dataset = PromptDataset(artifact_df=source_artifact_df)

        state.source_dataset = source_layer_only_dataset
        state.original_dataset = original_dataset_complete
