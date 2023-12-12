from typing import Dict, Set

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.clustering_constants import CLUSTERING_SUBDIRECTORY
from tgen.common.util.clustering_util import ClusteringUtil
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.file_util import FileUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
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
                                      add_orphans_to_best_home=False,
                                      allow_singleton_clusters=False,
                                      allow_duplicates_between_clusters=False)
        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        cluster2artifact = ClusteringUtil.convert_cluster_map_to_artifact_format(clustering_pipeline.state.final_cluster_map,
                                                                                 artifact_df)
        cluster_artifacts = clustering_pipeline.state.cluster_dataset.artifact_df\
            .filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] != args.target_type)
        content_generator = ContentGenerator(args, state, PromptDataset(artifact_df=cluster_artifacts))
        response_instructions = "Each {" \
                                f"{ContentGenerator.TARGET_TAG_ID}" \
                                "} should also include the ids of the original artifacts " \
                                "in a comma-deliminated list enclosed in {ids}. "
        prompt_builder = content_generator.create_prompt_builder(SupportedPrompts.HGEN_REFINEMENT, SupportedPrompts.HGEN_REFINE_TASKS,
                                                                 args.target_type, cluster2artifact,
                                                                 additional_task_response_instructions=response_instructions)
        generations = content_generator.generate_content(prompt_builder, generations_filename=self.GENERATION_FILENAME)
        generations2original_ids, _ = content_generator.map_generations_to_predicted_sources(generations)
        cluster2generation = self._add_missing_generations_and_create_cluster_mapping(artifact_df, generations2original_ids, state)
        state.refined_generations2sources = generations2original_ids
        state.cluster2generation = cluster2generation

    @staticmethod
    def _add_missing_generations_and_create_cluster_mapping(artifact_df: ArtifactDataFrame,
                                                            generations2original_ids: Dict[str, Set],
                                                            state: HGenState) -> Dict[str, Set[str]]:
        """
        Adds any missing generations to generations2original_ids and creates a mapping of origin cluster to the generation.
        :param artifact_df: Contains the original generations.
        :param generations2original_ids: Maps new generations to the original artifact ids they came from.
        :param state: The current state of HGen.
        :return: A mapping of origin cluster to the generation.
        """
        cluster2generation = {}
        original_generation2cluster = {generation: cluster_id for cluster_id, generations in state.cluster2generation.items()
                                       for generation in generations}
        seen_ids = set()
        for generation, original_a_ids in generations2original_ids.items():
            seen_ids.update(original_a_ids)
            for a_id in original_a_ids:
                original_generation = artifact_df.get_artifact(a_id)[ArtifactKeys.CONTENT]
                original_cluster = original_generation2cluster[original_generation]
                DictUtil.set_or_append_item(cluster2generation, original_cluster, generation)
            generations2original_ids[generation] = set()
        for a_id, artifact in artifact_df.itertuples():
            if a_id not in seen_ids:
                generation = artifact[ArtifactKeys.CONTENT]
                cluster = original_generation2cluster[generation]
                generations2original_ids[generation] = set()
                DictUtil.set_or_append_item(cluster2generation, cluster, generation)
                seen_ids.add(a_id)
        return cluster2generation
