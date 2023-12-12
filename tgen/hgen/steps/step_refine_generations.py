from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.clustering_constants import CLUSTERING_SUBDIRECTORY
from tgen.common.util.clustering_util import ClusteringUtil
from tgen.common.util.file_util import FileUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.hgen_util import HGenUtil
from tgen.hgen.content_generator import ContentGenerator
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class RefineGenerationsStep(AbstractPipelineStep[HGenArgs, HGenState]):
    GENERATION_FILENAME = "artifact_gen_refinement"

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Re-runs hgen to find the optimal artifacts across runs
        :param args: The arguments to Hierarchy Generator
        :param state: The current state for the generator
        :return: None
        """
        if not args.run_refinement:
            state.refined_generations2sources = state.generations2sources
            return

        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, CLUSTERING_SUBDIRECTORY, self.__class__.__name__)
        artifact_df, _ = HGenUtil.create_artifact_df_from_generated_artifacts(args, state.generations2sources, args.target_type,
                                                                              generate_names=False)
        cluster_args = ClusteringArgs(dataset=PromptDataset(artifact_df=artifact_df),
                                      create_dataset=True,
                                      export_dir=clustering_export_path,
                                      add_orphans_to_best_home=True)
        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        cluster2artifact = ClusteringUtil.convert_cluster_map_to_artifact_format(clustering_pipeline.state.final_cluster_map,
                                                                                 artifact_df)

        content_generator = ContentGenerator(args, state)
        prompt_builder = content_generator.create_prompt_builder(SupportedPrompts.HGEN_REFINEMENT, SupportedPrompts.HGEN_REFINE_TASKS,
                                                                 args.target_type, cluster2artifact)
        generations = content_generator.generate_content(clustering_pipeline.state.cluster_dataset,
                                                         prompt_builder,
                                                         generations_filename=self.GENERATION_FILENAME)
        generations2sources, cluster2generation = content_generator.map_generations_to_predicted_sources(generations)
        state.refined_generations2sources = generations2sources
        state.cluster2generation = cluster2generation
