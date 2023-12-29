import math
from typing import Dict, Set, Tuple, List, Any

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.clustering_constants import CLUSTERING_SUBDIRECTORY
from tgen.common.constants.deliminator_constants import DASH
from tgen.common.util.clustering_util import ClusteringUtil
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
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
from tgen.tracing.ranking.sorters.embedding_sorter import EmbeddingSorter


class RefineGenerationsStep(AbstractPipelineStep[HGenArgs, HGenState]):
    DUPLICATE_SUMMARIES_FILENAME = "duplicate_summaries_response"
    REFINED_GENERATIONS_FILENAME = "refined_generations_response"

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Re-runs hgen on cluster of duplicate artifacts to condense them.
        :param args: The arguments to Hierarchy Generator.
        :param state: The current state for the generator.
        :return: None.
        """
        if not args.run_refinement or not args.perform_clustering:
            return

        cluster2duplicates, duplicate_cluster_artifacts = self._create_clusters_of_duplicates(args, state)
        new_source_clusters, dups2remove = self._create_new_source_clusters(args, state, cluster2duplicates)

        format_variables = self._create_prompt_variables(args, state, cluster2duplicates, duplicate_cluster_artifacts)
        refined_generation2sources, refined_cluster2generations = self._regenerate_for_duplicates(args, state, new_source_clusters,
                                                                                                  duplicate_cluster_artifacts,
                                                                                                  format_variables)

        self._merge_original_with_refined_generations(refined_cluster2generations, refined_generation2sources,
                                                      new_source_clusters, duplicate_cluster_artifacts, dups2remove, state)

        state.refined_cluster2artifacts = {c_id: [a[ArtifactKeys.ID] for a in c_arts] for c_id, c_arts in new_source_clusters.items()}
        state.refined_generations2sources = refined_generation2sources
        state.refined_cluster2generation = refined_cluster2generations

    def _regenerate_for_duplicates(self, args: HGenArgs, state: HGenState, new_source_clusters: Dict[str, List[EnumDict]],
                                   duplicate_cluster_artifacts: ArtifactDataFrame,
                                   format_variables: Dict[str, List]) -> Tuple[Dict, Dict]:
        """
        Regenerates the target type for each duplicate cluster.
        :param args: The arguments to Hierarchy Generator
        :param state: The current state for the generator
        :param duplicate_cluster_artifacts: Dataframe of all duplicate cluster artifacts.
        :param new_source_clusters: Dictionary mapping cluster id to a list of all source artifacts in that cluster.
        :param format_variables: The variables to format each prompt with.
        :return:  A mapping of the generated artifact to a list of the predicted links to it and mapping of og cluster to generation.
        """
        content_generator = ContentGenerator(args, state, PromptDataset(artifact_df=duplicate_cluster_artifacts))
        prompt_builder = content_generator.create_prompt_builder(SupportedPrompts.HGEN_GENERATION,
                                                                 SupportedPrompts.HGEN_REFINEMENT_QUESTIONNAIRE,
                                                                 args.source_type, new_source_clusters,
                                                                 format_variables=format_variables)
        generations = content_generator.generate_content(prompt_builder, generations_filename=self.REFINED_GENERATIONS_FILENAME)
        return content_generator.map_generations_to_predicted_sources(generations, cluster_ids=list(new_source_clusters.keys()))

    def _create_prompt_variables(self, args: HGenArgs, state: HGenState, cluster2duplicates: Dict[str, List[EnumDict]],
                                 duplicate_cluster_artifacts: ArtifactDataFrame) -> Dict[str, List]:
        """
        Creates the necessary variables to format the regeneration prompts with.
        :param args: The arguments to Hierarchy Generator
        :param state: The current state for the generator
        :param cluster2duplicates: Dictionary mapping cluster id to a list of the duplicate artifacts in the cluster.
        :param duplicate_cluster_artifacts: Dataframe of all duplicate cluster artifacts.
        :return: Dictionary mapping format variable name to its value.
        """
        summary_of_dups = self._summarize_duplicates(args, state, cluster2duplicates, duplicate_cluster_artifacts)
        n_targets = [max(1, math.floor((len(d.split(DASH)) - 1) / 2)) for d in summary_of_dups]  # 50% of the # of bullets in summary
        format_variables = {"dup_summaries": summary_of_dups,
                            "n_targets": n_targets}
        return format_variables

    def _summarize_duplicates(self, args: HGenArgs, state: HGenState, cluster2duplicates: Dict[str, List[EnumDict]],
                              duplicate_cluster_artifacts: ArtifactDataFrame) -> List[str]:
        """
        Summarizes the features of each duplicate cluster.
        :param args: The arguments to Hierarchy Generator
        :param state: The current state for the generator
        :param cluster2duplicates: Dictionary mapping cluster id to a list of the duplicate artifacts in the cluster.
        :param duplicate_cluster_artifacts: Dataframe of all duplicate cluster artifacts.
        :return: List of the summarized duplicate clusters.
        """
        content_generator = ContentGenerator(args, state, PromptDataset(artifact_df=duplicate_cluster_artifacts))
        prompt_builder = content_generator.create_prompt_builder(SupportedPrompts.HGEN_REFINEMENT,
                                                                 SupportedPrompts.HGEN_DUP_SUMMARY_TASKS,
                                                                 args.target_type, cluster2duplicates, include_summary=False)
        summary_of_dups = content_generator.generate_content(prompt_builder, generations_filename=self.DUPLICATE_SUMMARIES_FILENAME,
                                                             return_first=True)
        return summary_of_dups

    def _create_clusters_of_duplicates(self, args: HGenArgs, state: HGenState) -> Tuple[Dict[str, List[EnumDict]], ArtifactDataFrame]:
        """
        Creates clusters of closely related (duplicated) target artifacts generated from previous step.
        :param args: The arguments to Hierarchy Generator.
        :param state: The current state for the generator.
        :return: Dictionary mapping cluster id to a list of dups in the cluster and a dataframe containing cluster artifacts.
        """
        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, CLUSTERING_SUBDIRECTORY, self.__class__.__name__)
        target_df, _ = HGenUtil.create_artifact_df_from_generated_artifacts(args, state.generations2sources, args.target_type,
                                                                            generate_names=False)
        cluster_args = ClusteringArgs(dataset=PromptDataset(artifact_df=target_df), export_dir=clustering_export_path,
                                      create_dataset=True, allow_duplicates_between_clusters=False,
                                      add_orphans_to_homes=False, allow_singleton_clusters=False)

        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        clustering_state = clustering_pipeline.state
        state.embedding_manager.merge(clustering_state.embedding_manager)

        target_df = clustering_state.cluster_dataset.artifact_df.get_artifacts_by_type(args.target_type)  # ensure matches saved state
        cluster2duplicates = ClusteringUtil.convert_cluster_map_to_artifact_format(clustering_state.final_cluster_map,
                                                                                   target_df)
        cluster_artifacts = clustering_state.cluster_dataset.artifact_df.get_artifacts_by_type(ClusteringArgs.cluster_artifact_type)
        cluster2duplicates = {f"r-{c_id}": duplicates for c_id, duplicates in cluster2duplicates.items()}
        cluster_artifacts.index = list(cluster2duplicates.keys())
        return cluster2duplicates, cluster_artifacts

    @staticmethod
    def _create_new_source_clusters(args: HGenArgs, state: HGenState,
                                    cluster2artifact: Dict[str, List[EnumDict]]) -> Tuple[Dict[str, List[EnumDict]], Set]:
        """
        Creates new clusters of source artifacts centered around a duplicate cluster.
        :param args: The arguments to Hierarchy Generator.
        :param state: The current state for the generator.
        :param cluster2artifact: Dictionary mapping cluster id to a list of the artifacts in the cluster.
        :return: Dictionary mapping new cluster to the sources in the cluster and a set of all duplicated generations to remove.
        """
        new_source_clusters, dups2remove = {}, set()
        generation2cluster = DictUtil.flip(state.cluster2generation)
        for cluster_id, dup_artifacts in cluster2artifact.items():
            new_source_clusters[cluster_id] = []
            for artifact in dup_artifacts:
                a_id, content = artifact[ArtifactKeys.ID], artifact[ArtifactKeys.CONTENT]
                linked_sources, scores = EmbeddingSorter.sort(parent_ids=[a_id],
                                                              child_ids=state.cluster2artifacts[generation2cluster[content]],
                                                              embedding_manager=state.embedding_manager, return_scores=True)[a_id]
                selected_source_ids = [a for a, s in zip(linked_sources, scores) if s >= args.link_selection_threshold]
                selected_source_ids = linked_sources[:min(3, len(scores))] if not selected_source_ids else selected_source_ids
                selected_source_artifacts = [state.source_dataset.artifact_df.get_artifact(c_id) for c_id in selected_source_ids]
                new_source_clusters[cluster_id].extend(selected_source_artifacts)
                dups2remove.add(content)
        return new_source_clusters, dups2remove

    @staticmethod
    def _merge_original_with_refined_generations(refined_cluster2generations: Dict[Any, List[str]],
                                                 refined_generation2sources: Dict[str, Set[str]],
                                                 new_source_clusters: Dict[str, List[EnumDict]],
                                                 duplicate_cluster_artifacts: ArtifactDataFrame, dups2remove: Set,
                                                 state: HGenState) -> None:
        """
        Merges the new generations with the originals from last step.
        :param refined_cluster2generations:  Maps the cluster to the generations that came from it.
        :param refined_generation2sources: Maps the generations to the sources that were used to generate it.
        :param new_source_clusters: Maps cluster_id to the sources in the cluster.
        :param duplicate_cluster_artifacts: Dataframe containing all duplicate cluster artifacts.
        :param dups2remove: Set of duplicate generations to remove.
        :param state: The current state of HGen.
        :return: None.
        """
        refined_generation2sources.update({generation: sources for generation, sources in state.generations2sources.items()
                                           if generation not in dups2remove})
        original_cluster2artifacts = state.get_cluster2artifacts()
        for cluster, original_generation in state.cluster2generation.items():
            refined_generations = [g for g in original_generation if g not in dups2remove]
            if refined_generations:
                refined_cluster2generations[cluster] = refined_generations
                new_source_clusters[cluster] = original_cluster2artifacts[cluster]
        new_source_clusters.update(state.get_cluster2artifacts())
