from typing import Dict, List, Set, Tuple

from gen_common.data.keys.structure_keys import ArtifactKeys, TraceKeys
from gen_common.data.objects.trace import Trace
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.traceability.ranking.common.ranking_args import RankingArgs
from gen_common.traceability.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from gen_common.util.enum_util import EnumDict
from gen_common.util.file_util import FileUtil


class ContextFinder:

    @staticmethod
    def find_related_artifacts(artifact_id: str, dataset: PromptDataset, layer_ids: Set[str] = None, max_context: int = None,
                               base_export_dir: str = None, **ranking_params) -> Tuple[Dict[str, List[EnumDict]], List[Trace]]:
        """
        Identifies related artifacts to the given artifact.
        :param artifact_id: The id of the artifact to find related artifacts for.
        :param dataset: Contains all artifacts in the dataset.
        :param layer_ids: Will only select context artifacts that are in the given layer ids. None if should use all.
        :param base_export_dir: The directory to save output to.
        :param max_context: The maximum number of artifacts allowed in the context.
        :return: A mapping of artifact id to related artifacts and a list of traces containing the related artifacts.
        """
        artifact_df = dataset.artifact_df
        layer_ids = artifact_df.get_artifact_types() if not layer_ids else layer_ids
        requirement = artifact_df.get_artifact(artifact_id)
        children_ids = [artifact_id]
        all_relationships = []
        for layer in layer_ids:
            layer_artifacts = artifact_df.get_artifacts_by_type(layer)
            parent_ids = [a_id for a_id in layer_artifacts.index if a_id != artifact_id]
            if not parent_ids:
                continue
            export_dir = FileUtil.safely_join_paths(base_export_dir, layer)
            ranking_args = RankingArgs(dataset=dataset,
                                       parent_ids=parent_ids,
                                       children_ids=children_ids,
                                       export_dir=export_dir,
                                       types_to_trace=(layer, requirement[ArtifactKeys.LAYER_ID]),
                                       generate_explanations=False,
                                       use_rag_defaults=True,
                                       **ranking_params)
            logger.info(f"Starting to find related {layer} to artifact {artifact_id}")

            pipeline = EmbeddingRankingPipeline(ranking_args)
            pipeline.run()
            selected_entries = pipeline.state.get_current_entries()
            all_relationships.extend(selected_entries)
        top_relationships = sorted(all_relationships, key=lambda item: item[TraceKeys.SCORE], reverse=True)[:max_context] \
            if max_context else all_relationships
        id2context = {artifact_id: [artifact_df.get_artifact(trace[TraceKeys.parent_label()]) for trace in top_relationships]}
        return id2context, all_relationships
