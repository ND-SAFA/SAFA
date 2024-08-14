from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.hgen_util import HGenUtil
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class NameArtifactsStep(AbstractPipelineStep[HGenArgs, HGenState]):
    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates names for the generated artifacts.
        :param args: Arguments to the hgen pipeline.
        :param state: Current state of the pipeline.
        :return: None
        """
        new_artifact_df, id_to_related_children = HGenUtil.create_artifact_df_from_generated_artifacts(args,
                                                                                                       state.get_generations2sources(),
                                                                                                       args.target_type,
                                                                                                       generation_id="base")

        new_artifact_dataset = PromptDataset(artifact_df=new_artifact_df)

        source_artifact_df = state.original_dataset.artifact_df.get_artifacts_by_type(args.source_layer_ids)
        all_artifact_df = ArtifactDataFrame.concat(source_artifact_df, new_artifact_df)
        all_artifacts_dataset = PromptDataset(artifact_df=all_artifact_df, project_summary=args.dataset.project_summary)

        state.new_artifact_dataset = new_artifact_dataset
        state.all_artifacts_dataset = all_artifacts_dataset
        state.id_to_related_children = id_to_related_children
