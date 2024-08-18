from typing import Any, Dict, List, Optional, Set, Tuple

from gen_common.clustering.base.cluster import Cluster
from gen_common.clustering.base.cluster_type import ClusterMapType
from gen_common.clustering.base.clustering_util import ClusteringUtil
from gen_common.constants.clustering_constants import CLUSTERING_SUBDIRECTORY
from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys, TraceKeys
from gen_common.data.objects.trace import Trace
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.traceability.ranking.sorters.transformer_sorter import TransformerSorter
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common.util.dict_util import DictUtil
from gen_common.util.enum_util import EnumDict
from gen_common.util.file_util import FileUtil
from gen_common.util.ranking_util import RankingUtil

from gen.hgen.common.content_generator import ContentGenerator
from gen.hgen.common.duplicate_detector import DuplicateDetector, DuplicateType
from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hgen_prompts import DUP_SUMMARY_TASKS, GENERATION_PROMPT, REFINEMENT_QUESTIONNAIRE, REFINE_OVERVIEW_PROMPT
from gen.hgen.hgen_state import HGenState


class ContentRefiner:
    DUPLICATE_SUMMARIES_FILENAME = "duplicate_summaries_response"
    REFINED_GENERATIONS_FILENAME = "refined_generations_response"

    def __init__(self, args: HGenArgs, state: HGenState, duplicate_type: DuplicateType):
        """
        Runs the refinement of the previous generations by collapsing duplicates.
        :param args: The arguments to HGen.
        :param state: The current state of HGen.
        :param duplicate_type: The type of duplicate to refine.
        """
        self.args = args
        self.state = state
        self.duplicate_type = duplicate_type

    def refine(self, generated_artifacts_df: ArtifactDataFrame,
               duplicate_cluster_map: ClusterMapType = None,
               new_source_clusters: Dict[str, List[EnumDict]] = None) -> Optional[Tuple[Dict, Dict, Dict]]:
        """
        Refines the previous generations.
        :param generated_artifacts_df: Contains the generated artifacts being refined.
        :param duplicate_cluster_map: Map of clusters containing duplicates.
        :param new_source_clusters: Maps duplicate cluster to the cluster of sources that produced them.
        :return: Updated variables for state.
        """
        if not duplicate_cluster_map:
            clustering_export_path = FileUtil.safely_join_paths(self.args.export_dir, CLUSTERING_SUBDIRECTORY,
                                                                f"refine_clusters_{self.duplicate_type.name.lower()}")
            duplicate_detector = DuplicateDetector(embeddings_manager=self.state.embedding_manager)
            logger.info("Clustering generations to identify overlapping artifacts. ")
            duplicate_cluster_map = duplicate_detector.cluster_duplicates(artifact_df=generated_artifacts_df,
                                                                          duplicate_type=self.duplicate_type,
                                                                          original_clusters_to_contents=self.state.get_cluster2generation(),
                                                                          export_path=clustering_export_path)
        if len(duplicate_cluster_map) == 0:
            return

        if not new_source_clusters:
            logger.info("Linking duplicates to their source artifacts. ")
            new_source_clusters, dups2remove = self._create_new_source_clusters(duplicate_cluster_map, generated_artifacts_df)
        else:
            dups2remove = set()
            for cluster in duplicate_cluster_map.values():
                dups2remove.update(cluster.artifact_id_set)
        duplicate_cluster_artifacts = self._convert_clusters_to_df(duplicate_cluster_map)
        format_variables = self._create_prompt_variables(duplicate_cluster_map, new_source_clusters, generated_artifacts_df,
                                                         duplicate_cluster_artifacts)

        refined_generation2sources, refined_cluster2generations = self._regenerate_for_duplicates(duplicate_cluster_artifacts,
                                                                                                  new_source_clusters,
                                                                                                  format_variables)
        self._merge_original_with_refined_generations(refined_cluster2generations, refined_generation2sources,
                                                      new_source_clusters, dups2remove)
        refined_cluster2artifacts = {c_id: [a[ArtifactKeys.ID] for a in c_arts] for c_id, c_arts in new_source_clusters.items()}
        return refined_generation2sources, refined_cluster2generations, refined_cluster2artifacts

    @staticmethod
    def _convert_clusters_to_df(duplicate_cluster_map: ClusterMapType) -> ArtifactDataFrame:
        """
        Converts a map of duplicates into a dataframe.
        :param duplicate_cluster_map: Maps of duplicate clusters.
        :return: A dataframe containing references to the clusters.
        """
        duplicate_cluster_artifacts = ArtifactDataFrame({ArtifactKeys.ID: duplicate_cluster_map.keys(),
                                                         ArtifactKeys.CONTENT: [EMPTY_STRING for _ in duplicate_cluster_map],
                                                         ArtifactKeys.LAYER_ID: ["duplicate_cluster" for _ in duplicate_cluster_map]})
        return duplicate_cluster_artifacts

    def _create_new_source_clusters(self, duplicate_cluster_map: ClusterMapType,
                                    generated_artifacts_df: ArtifactDataFrame) -> Tuple[Dict[str, List[EnumDict]], Set]:
        """
        Creates new clusters of source artifacts centered around a duplicate cluster.
        :param duplicate_cluster_map: Dictionary mapping cluster id to cluster containing duplicates.
        :param generated_artifacts_df: Contains the generated artifacts from previous step.
        :return: Dictionary mapping new cluster to the sources in the cluster and a set of all duplicated generations to remove.
        """
        new_source_clusters, dups2remove = {}, set()
        parent2children = self._find_top_parents_for_children(self.state, generated_artifacts_df) \
            if self.duplicate_type != DuplicateType.INTRA_CLUSTER else {}
        cluster2generation = self.state.get_cluster2generation()
        generation2cluster = DictUtil.flip(cluster2generation)
        original_cluster_to_artifacts = self.state.get_cluster2artifacts(ids_only=True)
        content2id = DictUtil.flip(generated_artifacts_df.to_map())
        for cluster_id, cluster in duplicate_cluster_map.items():
            new_source_clusters[cluster_id] = set()
            for a_id in cluster.artifact_ids:
                content = cluster.get_content(a_id)
                orig_cluster_id = generation2cluster[content]
                candidate_children = set(original_cluster_to_artifacts[orig_cluster_id])
                parent_candidates = [content2id.get(gen) for gen in cluster2generation[orig_cluster_id]]
                if self.duplicate_type == DuplicateType.INTRA_CLUSTER:
                    parent2children[a_id] = candidate_children
                    dups2remove.update(cluster2generation[orig_cluster_id])

                else:
                    self._add_best_children_for_parent(a_id, parent_candidates, list(candidate_children),
                                                       parent2children,
                                                       embedding_manager=self.state.embedding_manager,
                                                       link_threshold=self.args.link_selection_threshold)
                new_source_clusters[cluster_id].update({child_id for child_id in parent2children[a_id]
                                                        if child_id in candidate_children})
                dups2remove.add(content)
        new_source_clusters = {cluster_id: [self.state.source_dataset.artifact_df.get_artifact(a_id) for a_id in artifact_ids]
                               for cluster_id, artifact_ids in new_source_clusters.items()}
        return new_source_clusters, dups2remove

    @staticmethod
    def _add_best_children_for_parent(p_id: str, candidate_parents: List[str], candidate_children: List[str],
                                      parent2children: Dict[str, set], embedding_manager: EmbeddingsManager,
                                      link_threshold: float) -> None:
        """
        Adds the best children (highest sim score) to the parent2children mapping.
        :param p_id: The id of the parent.
        :param candidate_parents: All generations from the same cluster as the parent.
        :param candidate_children: All possible children for the parent.
        :param parent2children: Dictionary mapping parent artifact to a list of related children.
        :param embedding_manager: Contains the parent, children embeddings.
        :param link_threshold: The threshold above which a child is selected as related to parent.
        :return: None (selections added to parent2children dict)
        """
        parent2ranking = TransformerSorter.sort(parent_ids=candidate_parents,
                                                child_ids=candidate_children,
                                                relationship_manager=embedding_manager, return_scores=True)
        all_trace_preds: List[Trace] = [RankingUtil.create_entry(p_id, child, score) for p_id, (children, scores) in
                                        parent2ranking.items() for child, score in zip(children, scores)]
        RankingUtil.normalized_scores_based_on_parent(all_trace_preds)
        link_threshold = RankingUtil.calculate_threshold_from_std(all_trace_preds)
        parent_selected = RankingUtil.select_predictions_by_thresholds([p for p in all_trace_preds
                                                                        if p[TraceKeys.parent_label()] == p_id],
                                                                       primary_threshold=link_threshold)
        DictUtil.set_or_append_item(parent2children, p_id, {p[TraceKeys.child_label()] for p in parent_selected}, set)

    @staticmethod
    def _find_top_parents_for_children(state: HGenState, parent_artifact_df: ArtifactDataFrame) -> Dict[str, List[str]]:
        """
        Finds the top parent for each child.
        :param state: The current state of HGen.
        :param parent_artifact_df: Contains all parent artifacts.
        :return: Dictionary mapping parent artifact to a list of children that "chose" that parent.
        """
        dup_artifact_to_related_sources = {}
        cluster2children = state.get_cluster2artifacts(ids_only=True)
        cluster2parents = state.get_cluster2generation()
        content2id = DictUtil.flip(parent_artifact_df.to_map())
        state.embedding_manager.update_or_add_contents(parent_artifact_df.to_map())
        for cluster_id, child_artifact_ids in cluster2children.items():
            parent_ids = [content2id[parent] for parent in cluster2parents[cluster_id]]
            # switching parent and child so that we can grab best parent for child this time
            child2parents = TransformerSorter.sort(parent_ids=child_artifact_ids,
                                                   child_ids=parent_ids,
                                                   relationship_manager=state.embedding_manager, return_scores=False)
            for child, parents in child2parents.items():
                DictUtil.set_or_append_item(dup_artifact_to_related_sources, parents[0], child, set)
        return dup_artifact_to_related_sources

    def _create_prompt_variables(self, duplicate_cluster_map: ClusterMapType, new_source_clusters: Dict[str, List[EnumDict]],
                                 generated_artifacts_df: ArtifactDataFrame,
                                 duplicate_cluster_artifact_df: ArtifactDataFrame) -> Dict[str, List]:
        """
        Creates the necessary variables to format the regeneration prompts with.
        :param duplicate_cluster_map: Dictionary mapping cluster id to a cluster containing duplicates.
        :param new_source_clusters: Maps cluster_id to the list of source artifacts in that cluster.
        :param generated_artifacts_df: Contains the generated artifacts.
        :param duplicate_cluster_artifact_df: Contains the clusters of the duplicates.
        :return: Dictionary mapping format variable name to its value.
        """
        format_variables = {"n_targets": self._calculate_n_targets(duplicate_cluster_map, new_source_clusters)}
        if self.duplicate_type != DuplicateType.INTRA_CLUSTER:
            format_variables["functionality"] = self._summarize_duplicates(duplicate_cluster_map,
                                                                           generated_artifacts_df,
                                                                           duplicate_cluster_artifact_df,
                                                                           format_variables=format_variables)

        return format_variables

    def _calculate_n_targets(self, duplicate_cluster_map: ClusterMapType, new_source_clusters: Dict[str, List[EnumDict]]) -> List[int]:
        """
        Calculates the number of generations per duplicate cluster.
        :param duplicate_cluster_map: Dictionary mapping cluster id to a cluster containing duplicates.
        :param new_source_clusters: Maps cluster_id to the list of source artifacts in that cluster.
        :return: Dictionary mapping format variable name to its value.
        """
        if self.duplicate_type == DuplicateType.INTRA_CLUSTER:
            cluster2generations = [self.state.get_cluster2generation()[DuplicateDetector.identify_original_cluster(c_id)]
                                   for c_id in duplicate_cluster_map]
            n_generated = [len(c) for c in cluster2generations]
            n_targets = []
            for i, c_id in enumerate(duplicate_cluster_map.keys()):
                reduced_duplicate_n = self._calculate_n_targets_for_duplicate_cluster(duplicate_cluster_map[c_id])
                new_n = n_generated[i] - len(duplicate_cluster_map[c_id].artifact_id_set) + reduced_duplicate_n
                n_target = max(new_n, 2 if n_generated[i] > 3 or len(new_source_clusters[c_id]) > 3 else 1)
                n_targets.append(n_target)
        else:
            n_targets = [self._calculate_n_targets_for_duplicate_cluster(duplicates) for duplicates in duplicate_cluster_map.values()]
        return n_targets

    @staticmethod
    def _calculate_n_targets_for_duplicate_cluster(duplicates: Cluster) -> int:
        """
        Calculates the number of targets per duplicate cluster.
        :param duplicates: The cluster of duplicates.
        :return: The number of targets.
        """
        originating_clusters = duplicates.get_originating_clusters()
        if not originating_clusters:
            originating_clusters = [duplicates]
        n_targets = 0
        for cluster in originating_clusters:
            if cluster.id == DuplicateType.INTRA_CLUSTER.name:
                n_targets += 1
            else:
                n_targets += len(cluster)
        return n_targets

    def _summarize_duplicates(self, duplicate_cluster_map: ClusterMapType, generated_artifacts_df: ArtifactDataFrame,
                              duplicate_cluster_artifact_df: ArtifactDataFrame, format_variables: Dict[str, List]) -> List[str]:
        """
        Summarizes the features of each duplicate cluster.
        :param duplicate_cluster_map: Dictionary mapping cluster id to a cluster containing duplicates.
        :param generated_artifacts_df: Contains the generated artifacts.
        :param duplicate_cluster_artifact_df: Contains the clusters of the duplicates.
        :param format_variables: Dictionary mapping variable name to list of values to use when creating prompt.
        :return: List of the summarized duplicate clusters.
        """
        logger.info("Summarizing duplicate core goals. ")
        cluster2duplicates = ClusteringUtil.convert_cluster_map_to_artifact_format(duplicate_cluster_map,
                                                                                   generated_artifacts_df)
        content_generator = ContentGenerator(self.args, self.state, PromptDataset(artifact_df=duplicate_cluster_artifact_df))
        prompt_builder = content_generator.create_prompt_builder(REFINE_OVERVIEW_PROMPT,
                                                                 DUP_SUMMARY_TASKS,
                                                                 self.args.target_type, cluster2duplicates,
                                                                 include_summary=False, format_variables=format_variables,
                                                                 artifact_prompt_build_method=MultiArtifactPrompt.BuildMethod.NUMBERED)
        summary_of_dups = content_generator.generate_content(prompt_builder, generations_filename=self.DUPLICATE_SUMMARIES_FILENAME,
                                                             return_first=True)
        return summary_of_dups

    def _regenerate_for_duplicates(self, duplicate_cluster_artifacts: ArtifactDataFrame,
                                   new_source_clusters: Dict[str, List[EnumDict]],
                                   format_variables: Dict[str, List]) -> Tuple[Dict, Dict]:
        """
        Regenerates the target type for each duplicate cluster.
        :param duplicate_cluster_artifacts: Dataframe of all duplicate cluster artifacts.
        :param new_source_clusters: Maps cluster_id to the list of source artifacts in that cluster.
        :param format_variables: The variables to format each prompt with.
        :return:  A mapping of the generated artifact to a list of the predicted links to it and mapping of og cluster to generation.
        """
        logger.info("Regenerating content for overlapping artifacts. ")
        content_generator = ContentGenerator(self.args, self.state, PromptDataset(artifact_df=duplicate_cluster_artifacts))
        prompt_builder = content_generator.create_prompt_builder(GENERATION_PROMPT,
                                                                 REFINEMENT_QUESTIONNAIRE,
                                                                 self.args.source_type, new_source_clusters,
                                                                 format_variables=format_variables, include_summary=False)
        generations = content_generator.generate_content(prompt_builder,
                                                         generations_filename=f"{self.REFINED_GENERATIONS_FILENAME}"
                                                                              f"_{self.duplicate_type.name}")
        return content_generator.map_generations_to_predicted_sources(generations, cluster_ids=list(new_source_clusters.keys()))

    def _merge_original_with_refined_generations(self, refined_cluster2generations: Dict[Any, List[str]],
                                                 refined_generation2sources: Dict[str, Set[str]],
                                                 new_source_clusters: Dict[str, List[EnumDict]], dups2remove: Set) -> None:
        """
        Merges the new generations with the originals from last step.
        :param refined_cluster2generations:  Maps the cluster to the generations that came from it.
        :param refined_generation2sources: Maps the generations to the sources that were used to generate it.
        :param new_source_clusters: Maps cluster_id to the sources in the cluster.
        :param dups2remove: Set of duplicate generations to remove.
        :return: None.
        """
        refined_generation2sources.update({generation: sources for generation, sources in self.state.get_generations2sources().items()
                                           if generation not in dups2remove})
        original_cluster2artifacts = self.state.get_cluster2artifacts()
        for cluster, original_generation in self.state.get_cluster2generation().items():
            refined_generations = [g for g in original_generation if g not in dups2remove]
            if refined_generations:
                refined_cluster2generations[cluster] = refined_generations
                new_source_clusters[cluster] = original_cluster2artifacts[cluster]
