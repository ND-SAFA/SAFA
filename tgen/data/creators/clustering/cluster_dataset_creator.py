import uuid
from collections import Set
from typing import Dict, Union, Tuple

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.creators.clustering.iclustering import Clusters
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


class ClusterDatasetCreator(AbstractDatasetCreator):
    """
    Responsible for clustering dataset artifacts
    """

    CLUSTER_CONTENT_FORMAT = "{}"

    def __init__(self, prompt_dataset: PromptDataset,
                 cluster_methods: Union[Set[SupportedClusteringMethod], SupportedClusteringMethod] = SupportedClusteringMethod.MANUAL,
                 manual_clusters: dict = None, **clustering_params):
        """
        Initializes with a dataset with artifacts to be clustered
        :param trace_dataset: The dataset to perform clustering on
        :param artifact_df: The dataframe containing all artifacts to cluster from
        :param cluster_methods: The methods to use to create clusters
        :param manual_clusters: Manually created clusters to use to create dataset
        :param clustering_params: Any additional parameters necessary to create clusters
        """
        super().__init__()
        assert prompt_dataset.artifact_df is not None, "Creator requires artifacts to be provided"
        self.trace_dataset = prompt_dataset.trace_dataset if prompt_dataset.trace_dataset is not None \
            else TraceDataset(prompt_dataset.artifact_df, TraceDataFrame(), LayerDataFrame())
        self.artifact_df = prompt_dataset.artifact_df
        self.cluster_methods = cluster_methods if isinstance(cluster_methods, Set) else {cluster_methods}
        assert SupportedClusteringMethod.MANUAL not in self.cluster_methods or manual_clusters, \
            "Must supply clusters for manual clustering"
        if manual_clusters:
            self.cluster_methods.add(SupportedClusteringMethod.MANUAL)
        self.manual_clusters = {uuid.uuid4(): cluster for cluster in manual_clusters.values()} if manual_clusters else {}
        self.clustering_params = clustering_params
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
                    clusters = cluster_method.value(trace_dataset=self.trace_dataset, **self.clustering_params)
                self.__method_to_clusters[cluster_method] = clusters
        return self.__method_to_clusters

    def get_name(self) -> str:
        """
        Returns the name of the dataset
        :return: The name of the dataset
        """
        return f"cluster_dataset_of_{', '.join([cm.name.capitalize() for cm in self.cluster_methods])}"

    def create(self) -> PromptDataset:
        """
        Creates an artifact dataframe where each cluster represents a single artifact
        :return: The new dataset where each cluster is a single artifact linked to the artifacts in the cluster
        """
        cluster_id_to_content, source_layers, traces = ClusterDatasetCreator._extract_dataset_input_from_clusters(self.get_clusters(),
                                                                                                                  self.trace_dataset
                                                                                                                  .artifact_df)
        new_artifact_df = ArtifactDataFrame({ArtifactKeys.ID: list(cluster_id_to_content.keys()),
                                             ArtifactKeys.CONTENT: list(cluster_id_to_content.values()),
                                             ArtifactKeys.LAYER_ID: [self.layer_id for _ in cluster_id_to_content]})
        artifact_df = ArtifactDataFrame.concat(new_artifact_df, self.trace_dataset.artifact_df)
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: list(source_layers),
                                   LayerKeys.TARGET_TYPE: [self.layer_id for _ in source_layers]})
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=artifact_df, trace_df=TraceDataFrame(traces),
                                                               layer_mapping_df=layer_df)
        trace_df = TraceDataFrame.concat(trace_df, self.trace_dataset.trace_df)
        layer_df = LayerDataFrame.concat(layer_df, self.trace_dataset.layer_df)
        return PromptDataset(artifact_df=new_artifact_df, trace_dataset=TraceDataset(artifact_df, trace_df, layer_df))

    @staticmethod
    def _extract_dataset_input_from_clusters(method_to_clusters: Dict[SupportedClusteringMethod, Clusters],
                                             artifact_df: ArtifactDataFrame) -> Tuple[Dict[str, str], Set[str], Dict[str, Dict]]:
        """
        Gets the mapping of cluster to content, all new positive trace links, and source layer ids to create the project dataframes
        :param method_to_clusters: A dictionary mapping method name to the clusters it produced
        :param artifact_df: The dataframe containing artifacts in the clusters
        :return:  mapping of cluster to content, all new positive trace links, and source layer ids to create the project dataframes
        """
        cluster_id_to_content = {}
        traces = {}
        source_layers = set()
        for clusters in method_to_clusters.values():
            for cluster_id, artifacts in clusters.items():
                artifact_content = []
                for i, artifact_id in enumerate(artifacts):
                    artifact = artifact_df.get_artifact(artifact_id)
                    artifact_content.append(ClusterDatasetCreator.CLUSTER_CONTENT_FORMAT.format(artifact[ArtifactKeys.CONTENT]))
                    traces = DataFrameUtil.append(traces, EnumDict({TraceKeys.SOURCE: artifact_id, TraceKeys.TARGET: cluster_id,
                                                                    TraceKeys.LABEL: 1}))  # add link between artifact and cluster
                    source_layers.add(artifact[ArtifactKeys.LAYER_ID])
                cluster_id_to_content[cluster_id] = NEW_LINE.join(artifact_content)  # combines the content of all artifacts in cluster
        return cluster_id_to_content, source_layers, traces
