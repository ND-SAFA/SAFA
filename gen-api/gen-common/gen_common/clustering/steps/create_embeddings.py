from typing import Dict, List

from gen_common.clustering.base.clustering_args import ClusteringArgs
from gen_common.clustering.base.clustering_state import ClusteringState
from gen_common.constants.model_constants import USE_NL_SUMMARY_EMBEDDINGS
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager


class CreateEmbeddings(AbstractPipelineStep):

    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Extracts the artifacts and embeds them.
        :param args: Contains the artifacts to embed.
        :param state: Stores the final embedding map.
        :return: None
        """
        artifact_types = args.artifact_types
        artifact_df = args.dataset.artifact_df

        artifact_map = self.create_artifact_map(artifact_df, artifact_types, args.use_ids_as_content)
        if args.embedding_manager:
            embeddings_manager = args.embedding_manager
            embeddings_manager.update_or_add_contents(artifact_map)
        else:
            embeddings_manager = EmbeddingsManager(content_map=artifact_map, model_name=args.embedding_model)
        embeddings_manager.create_embedding_map(include_ids=True)

        state.embedding_manager = embeddings_manager

    @staticmethod
    def create_artifact_map(artifact_df: ArtifactDataFrame, artifact_types: List[str], use_ids_as_content: bool) -> Dict[str, str]:
        """
        Creates artifact map containing artifacts in types.
        :param artifact_df: The artifact data frame.
        :param artifact_types: The artifact types to include in map.
        :param use_ids_as_content: If True, creates embeddings using just the id.
        :return: Artifact map of all matching artifacts.
        """
        artifact_map = {}
        available_types = artifact_df.get_artifact_types()
        for artifact_type in artifact_types:
            if artifact_type not in available_types:
                raise Exception(f"Expected one of ({available_types}) but got ({artifact_type}).")
            artifact_type_map = artifact_df.get_artifacts_by_type(artifact_type). \
                to_map(use_code_summary_only=not USE_NL_SUMMARY_EMBEDDINGS)
            if use_ids_as_content:
                artifact_type_map = {a_id: a_id for a_id in artifact_type_map.keys()}
            artifact_map.update(artifact_type_map)
        return artifact_map
