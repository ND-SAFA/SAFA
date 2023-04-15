from typing import Dict

from tgen.data.clustering.SupportedClusteringMethod import SupportedClusteringMethod
from tgen.data.clustering.i_clustering import Clusters, iClusteringMethod
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys, ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.enum_util import EnumDict


class ArtifactClusterer(BaseObject):
    """
    Responsible for clustering dataset artifacts
    """

    def __init__(self, trace_dataset: TraceDataset):
        """
        Initializes the clusterer with a dataset with artifacts to be clustered
        :param trace_dataset: The dataset to perform clustering on
        """
        self.trace_dataset = trace_dataset
        self.__method_to_clusters: Dict[SupportedClusteringMethod, Clusters] = {}

    def get_clusters(self, clustering_method: SupportedClusteringMethod) -> Clusters:
        """
        Returns clusters of artifacts in the dataset
        :param clustering_method: The method to use to cluster the dataset
        :return: A dictionary mapping artifact id to its cluster num
        """
        if clustering_method not in self.__method_to_clusters:
            clustering_method_cls: iClusteringMethod = clustering_method.value
            self.__method_to_clusters[clustering_method] = clustering_method_cls.cluster(trace_dataset=self.trace_dataset)
        return self.__method_to_clusters[clustering_method]

    def create_dataset_from_clusters(self, clustering_method: SupportedClusteringMethod) -> TraceDataset:
        """
        Creates a trace dataset with each cluster from the given method as a single artifact
        :param clustering_method: The method to use to cluster the dataset
        :return: A trace dataset constructed from the clusters
        """
        clusters = self.get_clusters(clustering_method)
        artifact_df = self._get_artifact_df_from_clusters(clusters, self.trace_dataset.artifact_df)
        trace_df = self._get_trace_df_from_clusters(clusters, self.trace_dataset.trace_df)
        layer_df = self._get_layer_df_from_clusters()
        return TraceDataset(artifact_df=artifact_df, trace_df=trace_df, layer_mapping_df=layer_df)

    @staticmethod
    def _get_layer_df_from_clusters() -> LayerDataFrame:
        """
        Creates the layer df from the clusters
        :return: The layer df from the clusters
        """
        return LayerDataFrame({LayerKeys.SOURCE_TYPE: ["layer_1"], LayerKeys.TARGET_TYPE: ["layer_1"]})

    @staticmethod
    def _get_trace_df_from_clusters(clusters: Clusters, orig_trace_df: TraceDataFrame, ) -> TraceDataFrame:
        """
        Creates a trace dataframe mapping links between clusters
        :param clusters: The clusters of artifacts
        :param orig_trace_df: The original trace df prior to clustering
        :return: The new trace dataframe mapping links between clusters
        """
        link_ids = set()
        traces = {}
        for link_id, link in orig_trace_df.iterrows():
            source_cluster = clusters[link[TraceKeys.SOURCE.value]]
            target_cluster = clusters[link[TraceKeys.TARGET.value]]
            link_id = TraceDataFrame.generate_link_id(source_cluster, target_cluster)
            if source_cluster == target_cluster or link_id in link_ids:
                continue
            traces = DataFrameUtil.append(traces, EnumDict({TraceKeys.SOURCE: source_cluster, TraceKeys.TARGET: target_cluster,
                                                            TraceKeys.LABEL: link[TraceKeys.LABEL.value]}))
            link_ids.add(link_id)
        return TraceDataFrame(traces)

    @staticmethod
    def _get_artifact_df_from_clusters(clusters: Clusters, orig_artifact_df: ArtifactDataFrame) -> ArtifactDataFrame:
        """
        Creates an artifact dataframe where each cluster represents a single artifact
        :param clusters: The clusters of artifacts
        :param orig_artifact_df: The original artifact df of all artifacts in the clusters
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
                                  ArtifactKeys.LAYER_ID: ["layer_1" for _ in content]})
