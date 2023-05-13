import uuid
from collections import Set
from typing import Dict, Any, List, Union, Tuple

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.creators.clustering.supported_clustering_method import SupportedClusteringMethod
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys, ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.enum_util import EnumDict
from tgen.util.logging.logger_manager import logger

Clusters = Dict[str, List[Any]]


class ClusterDatasetCreator(AbstractDatasetCreator):
    """
    Responsible for clustering dataset artifacts
    """

    CLUSTER_CONTENT_FORMAT = "{}"

    def __init__(self, trace_dataset: TraceDataset = None, trace_dataset_creator: TraceDatasetCreator = None,
                 cluster_methods: Union[Set[SupportedClusteringMethod], SupportedClusteringMethod] = SupportedClusteringMethod.MANUAL,
                 manual_clusters: dict = None):
        """
        Initializes with a dataset with artifacts to be clustered
        :param trace_dataset_creator:
        :param trace_dataset: The dataset to perform clustering on
        """
        super().__init__()
        assert not (trace_dataset is None and trace_dataset_creator is None), "Provide either a trace dataset or a creator to make one"
        self.trace_dataset = trace_dataset if trace_dataset is not None else trace_dataset_creator.create()
        self.cluster_methods = cluster_methods if isinstance(cluster_methods, Set) else {cluster_methods}
        assert SupportedClusteringMethod.MANUAL not in self.cluster_methods or manual_clusters is not None, \
            "Must supply clusters for manual clustering"
        if manual_clusters is not None:
            self.cluster_methods.add(SupportedClusteringMethod.MANUAL)
        self.manual_clusters = manual_clusters
        self.layer_id = str(uuid.uuid4())
        self.__method_to_clusters: Dict[SupportedClusteringMethod, Clusters] = {}

    def get_clusters(self) -> Dict[SupportedClusteringMethod, Clusters]:
        """
        Returns clusters of artifacts in the dataset for each clustering method
        :return: A dictionary mapping cluster_id to the list of artifact ids in the cluster
        """
        if not self.__method_to_clusters:
            for cluster_method in self.cluster_methods:
                logger.info(f"Creating clusters of artifacts using {cluster_method.name.capitalize()}")
                if cluster_method == SupportedClusteringMethod.MANUAL:
                    clusters = self.manual_clusters
                else:
                    clusters = self._cluster(trace_dataset=self.trace_dataset, cluster_method=cluster_method)
                self.__method_to_clusters[cluster_method] = clusters
        return self.__method_to_clusters

    def create(self) -> PromptDataset:
        """
        Creates a trace dataset with each cluster from the given method as a single artifact
        :return: A trace dataset constructed from the clusters
        """
        clusters = self.get_clusters()
        return self._create_dataset_from_clusters(clusters, self.trace_dataset, self.layer_id)

    def get_name(self) -> str:
        """
        Returns the name of the dataset
        :return: The name of the dataset
        """
        return f"cluster_dataset_of_{', '.join([cm.name.capitalize() for cm in self.cluster_methods])}"

    @staticmethod
    def _cluster(trace_dataset: TraceDataset, cluster_method: SupportedClusteringMethod) -> Clusters:
        """
        Creates clusters of artifacts in the dataset
        :return: A dictionary mapping artifact id to its cluster num
        """
        graph = trace_dataset.construct_graph_from_traces()
        communities = cluster_method.value(graph).communities
        return {str(uuid.uuid4()): community for community in communities if len(community) > 1}

    @staticmethod
    def _create_dataset_from_clusters(method_to_clusters: Dict[SupportedClusteringMethod, Clusters],
                                      orig_dataset: TraceDataset, cluster_layer_id: str) -> PromptDataset:
        """
        Creates an artifact dataframe where each cluster represents a single artifact
        :param method_to_clusters: Maps cluster methods to the clusters of artifacts it produced
        :param orig_dataset: The original dataset from which the clusters were formed
        :param cluster_layer_id: The id of the new layer
        :return: The new dataset where each cluster is a single artifact linked to the artifacts in the cluster
        """
        cluster_id_to_content, source_layers, traces = ClusterDatasetCreator._extract_dataset_input_from_clusters(method_to_clusters,
                                                                                                                  orig_dataset)
        new_artifact_df = ArtifactDataFrame({ArtifactKeys.ID: list(cluster_id_to_content.keys()),
                                             ArtifactKeys.CONTENT: list(cluster_id_to_content.values()),
                                             ArtifactKeys.LAYER_ID: [cluster_layer_id for _ in cluster_id_to_content]})
        artifact_df = ArtifactDataFrame.concat(new_artifact_df, orig_dataset.artifact_df)
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: list(source_layers),
                                   LayerKeys.TARGET_TYPE: [cluster_layer_id for _ in source_layers]})
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=artifact_df, trace_df=TraceDataFrame(traces),
                                                               layer_mapping_df=layer_df)
        trace_df = TraceDataFrame.concat(trace_df, orig_dataset.trace_df)
        layer_df = LayerDataFrame.concat(layer_df, orig_dataset.layer_df)
        return PromptDataset(artifact_df=new_artifact_df, trace_dataset=TraceDataset(artifact_df, trace_df, layer_df))

    @staticmethod
    def _extract_dataset_input_from_clusters(method_to_clusters: Dict[str, Clusters], orig_dataset: TraceDataset) \
            -> Tuple[Dict[str, str], Set[str], Dict[str, Dict]]:
        """
        Gets the mapping of cluster to content, all new positive trace links, and source layer ids to create the project dataframes
        :param method_to_clusters: A dictionary mapping method name to the clusters it produced
        :param orig_dataset: The original trace dataset
        :return:  mapping of cluster to content, all new positive trace links, and source layer ids to create the project dataframes
        """
        cluster_id_to_content = {}
        traces = {}
        source_layers = set()
        for clusters in method_to_clusters.values():
            for cluster_id, artifacts in clusters.items():
                artifact_content = []
                for i, artifact_id in enumerate(artifacts):
                    artifact = orig_dataset.artifact_df.get_artifact(artifact_id)
                    artifact_content.append(ClusterDatasetCreator.CLUSTER_CONTENT_FORMAT.format(artifact[ArtifactKeys.CONTENT]))
                    traces = DataFrameUtil.append(traces, EnumDict({TraceKeys.SOURCE: artifact_id, TraceKeys.TARGET: cluster_id,
                                                                    TraceKeys.LABEL: 1}))  # add link between artifact and cluster
                    source_layers.add(artifact[ArtifactKeys.LAYER_ID])
                cluster_id_to_content[cluster_id] = NEW_LINE.join(artifact_content)  # combines the content of all artifacts in cluster
        return cluster_id_to_content, source_layers, traces
