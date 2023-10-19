from typing import List

from tgen.clustering.clustering_args import ClusteringArgs
from tgen.clustering.clustering_state import ClusteringState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateEmbeddings(AbstractPipelineStep):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Extracts the artifacts and embeds them.
        :param args: Contains the artifacts to embed.
        :param state: Stores the final embedding map.
        :return: None
        """
        artifact_types = args.artifact_types
        artifact_df = args.dataset.trace_dataset.artifact_df

        artifact_map = self.create_artifact_map(artifact_df, artifact_types)
        model = EmbeddingsManager.get_model(args.embedding_model)
        embedding_map = EmbeddingsManager.create_embedding_map(artifact_map, model)

        state.embedding_map = embedding_map

    @staticmethod
    def create_artifact_map(artifact_df: ArtifactDataFrame, artifact_types: List[str]):
        """
        Creates artifact map containing artifacts in types.
        :param artifact_df: The artifact data frame.
        :param artifact_types: The artifact types to include in map.
        :return: Artifact map of all matching artifacts.
        """
        artifact_map = {}
        for artifact_type in artifact_types:
            artifact_type_map = artifact_df.get_type(artifact_type).to_map()
            artifact_map.update(artifact_type_map)
        return artifact_map
