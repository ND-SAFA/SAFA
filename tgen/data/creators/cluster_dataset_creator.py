import uuid

from tgen.data.clustering.SupportedClusteringMethod import SupportedClusteringMethod
from tgen.data.clustering.i_clustering import Clusters, iClusteringMethod
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys, ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.enum_util import EnumDict


class ClusterDatasetCreator(AbstractDatasetCreator):
    """
    Responsible for clustering dataset artifacts
    """

    def __init__(self, trace_dataset: TraceDataset, cluster_method: SupportedClusteringMethod):
        """
        Initializes with a dataset with artifacts to be clustered
        :param trace_dataset: The dataset to perform clustering on
        """
        super().__init__()
        self.trace_dataset = trace_dataset
        self.cluster_method = cluster_method
        self.layer_id = str(uuid.uuid4())
        self.__clusters: Clusters = {}

    def get_clusters(self) -> Clusters:
        """
        Returns clusters of artifacts in the dataset
        :return: A dictionary mapping artifact id to its cluster num
        """
        if not self.__clusters:
            clustering_method_cls: iClusteringMethod = self.cluster_method.value
            clusters = clustering_method_cls.cluster(trace_dataset=self.trace_dataset)
            cluster_num_2_id = {cluster_num: str(uuid.uuid4()) for cluster_num in clusters.values()}
            self.__clusters = {artifact_id: cluster_num_2_id[cluster_num]
                               for artifact_id, cluster_num in clusters.items()}
        return self.__clusters

    def create(self) -> TraceDataset:
        """
        Creates a trace dataset with each cluster from the given method as a single artifact
        :return: A trace dataset constructed from the clusters
        """
        clusters = self.get_clusters()
        artifact_df = self._get_artifact_df_from_clusters(clusters, self.trace_dataset.artifact_df, self.layer_id)
        trace_df = self._get_trace_df_from_clusters(clusters, self.trace_dataset.trace_df)
        layer_df = self._get_layer_df_from_clusters(self.layer_id)
        return TraceDataset(artifact_df=artifact_df, trace_df=trace_df, layer_mapping_df=layer_df)

    def get_name(self) -> str:
        """
        Returns the name of the dataset
        :return: The name of the dataset
        """
        return self.cluster_method.value

    @staticmethod
    def _get_layer_df_from_clusters(layer_id: str) -> LayerDataFrame:
        """
        Creates the layer df from the clusters
        :param layer_id: The id of the new layer
        :return: The layer df from the clusters
        """
        return LayerDataFrame({LayerKeys.SOURCE_TYPE: [layer_id],
                               LayerKeys.TARGET_TYPE: [layer_id]})

    @staticmethod
    def _get_trace_df_from_clusters(clusters: Clusters, orig_trace_df: TraceDataFrame) -> TraceDataFrame:
        """
        Creates a trace dataframe mapping links between clusters
        :param clusters: The clusters of artifacts
        :param orig_trace_df: The original trace df prior to clustering
        :return: The new trace dataframe mapping links between clusters
        """
        link_ids = set()
        traces = {}
        for link_id, link in orig_trace_df.itertuples():
            source_cluster = clusters[link[TraceKeys.SOURCE]]
            target_cluster = clusters[link[TraceKeys.TARGET]]
            link_id = TraceDataFrame.generate_link_id(source_cluster, target_cluster)
            if source_cluster == target_cluster or link_id in link_ids:
                continue
            traces = DataFrameUtil.append(traces, EnumDict({TraceKeys.SOURCE: source_cluster, TraceKeys.TARGET: target_cluster,
                                                            TraceKeys.LABEL: link[TraceKeys.LABEL]}))
            link_ids.add(link_id)
        return TraceDataFrame(traces)

    @staticmethod
    def _get_artifact_df_from_clusters(clusters: Clusters, orig_artifact_df: ArtifactDataFrame, layer_id: str) -> ArtifactDataFrame:
        """
        Creates an artifact dataframe where each cluster represents a single artifact
        :param clusters: The clusters of artifacts
        :param orig_artifact_df: The original artifact df of all artifacts in the clusters
        :param layer_id: The id of the new layer
        :return: The new artifact dataframe where each cluster is a single artifact
        """
        cluster_num_to_content = {}
        for artifact_id, cluster_num in clusters.items():
            if cluster_num not in cluster_num_to_content:
                cluster_num_to_content[cluster_num] = []
            artifact_content = orig_artifact_df.get_artifact(artifact_id)[ArtifactKeys.CONTENT]
            cluster_num_to_content[cluster_num].append(artifact_content)
        content = ["\n".join(artifact_content) for cluster_num, artifact_content in cluster_num_to_content.items()]
        return ArtifactDataFrame({ArtifactKeys.ID: list(cluster_num_to_content.keys()), ArtifactKeys.CONTENT: content,
                                  ArtifactKeys.LAYER_ID: [layer_id for _ in content]})
