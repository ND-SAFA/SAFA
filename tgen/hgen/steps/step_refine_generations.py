from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.clustering_constants import CLUSTERING_SUBDIRECTORY
from tgen.common.util.file_util import FileUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.hgen_util import HGenUtil
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class RefineGenerationsStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Re-runs hgen to find the optimal artifacts across runs
        :param args: The arguments to Hierarchy Generator
        :param state: The current state for the generator
        :return: None
        """
        # TODO
        return
        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, CLUSTERING_SUBDIRECTORY, self.__class__.__name__)
        artifacts_df, _ = HGenUtil.create_artifact_df_from_generated_artifacts(args, state.generations2sources, args.target_type,
                                                                               generate_names=False)
        cluster_args = ClusteringArgs(dataset=PromptDataset(artifact_df=artifacts_df),
                                      create_dataset=True,
                                      export_dir=clustering_export_path,
                                      add_orphans_to_best_home=True)
        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        clusters = clustering_pipeline.state.final_cluster_map

