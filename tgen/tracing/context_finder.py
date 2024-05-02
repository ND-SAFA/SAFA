from typing import List, Tuple, Dict

from tgen.common.logging.logger_manager import logger
from tgen.common.objects.trace import Trace
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline


class ContextFinder:

    @staticmethod
    def find_related_artifacts(artifact_id: str, dataset: PromptDataset, max_context: int = None,
                               base_export_dir: str = None, **ranking_params) -> Tuple[Dict[str, List[EnumDict]], List[Trace]]:
        """
        Identifies related artifacts to the given artifact.
        :param artifact_id: The id of the artifact to find related artifacts for.
        :param dataset: Contains all artifacts in the dataset.
        :param base_export_dir: The directory to save output to.
        :param max_context: The maximum number of artifacts allowed in the context.
        :return: A mapping of artifact id to related artifacts and a list of traces containing the related artifacts.
        """
        artifact_df = dataset.artifact_df
        requirement = artifact_df.get_artifact(artifact_id)
        children_ids = [artifact_id]
        all_relationships = []
        for layer in artifact_df.get_artifact_types():
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
