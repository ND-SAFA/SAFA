import uuid
from copy import deepcopy
from typing import Dict, Set, Tuple

from tgen.clustering.base.cluster import Cluster
from common_resources.tools.constants.symbol_constants import SPACE
from common_resources.tools.util.dataframe_util import DataFrameUtil
from common_resources.tools.util.enum_util import EnumDict
from common_resources.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys, LayerKeys, TraceKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer

Clusters = Dict[str, Cluster]


class ClusterDatasetCreator(AbstractDatasetCreator):
    """
    Responsible for clustering dataset artifacts
    """

    CLUSTER_CONTENT_FORMAT = "{}"

    def __init__(self, prompt_dataset: PromptDataset, manual_clusters: Clusters, layer_id: str = None,
                 summarizer: ArtifactsSummarizer = None, **clustering_params):
        """
        Initializes with a dataset with artifacts to be clustered
        :param prompt_dataset: The dataset to perform clustering on
        :param manual_clusters: Manually created clusters to use to create dataset
        :param layer_id: ID to use for the new layer created from the clusters
        :param summarizer: Summarizes the cluster artifact content
        :param clustering_params: Any additional parameters necessary to create clusters
        """
        super().__init__()
        assert prompt_dataset.artifact_df is not None, "Creator requires artifacts to be provided"
        self.trace_dataset = prompt_dataset.trace_dataset if prompt_dataset.trace_dataset is not None \
            else TraceDataset(prompt_dataset.artifact_df, TraceDataFrame(), LayerDataFrame())
        self.manual_clusters = manual_clusters
        self.clustering_params = clustering_params
        self.layer_id = str(uuid.uuid4()) if layer_id is None else layer_id
        self.summarizer = summarizer

    def get_clusters(self) -> Clusters:
        """
        Returns clusters of artifacts in the dataset for each clustering method
        :return: A dictionary mapping cluster_id to the list of artifact ids in the cluster
        """
        return self.manual_clusters

    def get_name(self) -> str:
        """
        Returns the name of the dataset
        :return: The name of the dataset
        """
        return "Generic Cluster Dataset."

    def create(self) -> PromptDataset:
        """
        Creates an artifact dataframe where each cluster represents a single artifact
        :return: The new dataset where each cluster is a single artifact linked to the artifacts in the cluster
        """
        cluster_id_to_content, source_layers, traces = ClusterDatasetCreator._extract_dataset_input_from_clusters(self.manual_clusters,
                                                                                                                  self.trace_dataset
                                                                                                                  .artifact_df,
                                                                                                                  self.layer_id)
        new_artifact_df = ArtifactDataFrame({ArtifactKeys.ID: list(cluster_id_to_content.keys()),
                                             ArtifactKeys.CONTENT: list(cluster_id_to_content.values()),
                                             ArtifactKeys.LAYER_ID: [self.layer_id for _ in cluster_id_to_content]})
        if self.summarizer:
            new_artifact_df.summarize_content(self.summarizer)
        artifact_df = ArtifactDataFrame.concat(new_artifact_df, self.trace_dataset.artifact_df)
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: list(source_layers),
                                   LayerKeys.TARGET_TYPE: [self.layer_id for _ in source_layers]})
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=artifact_df, trace_df=TraceDataFrame(traces),
                                                               layer_df=layer_df)
        trace_df = TraceDataFrame.concat(trace_df, self.trace_dataset.trace_df)
        layer_df = LayerDataFrame.concat(layer_df, self.trace_dataset.layer_df)
        return PromptDataset(artifact_df=new_artifact_df, trace_dataset=TraceDataset(artifact_df, trace_df, layer_df))

    @staticmethod
    def _extract_dataset_input_from_clusters(clusters: Clusters,
                                             artifact_df: ArtifactDataFrame,
                                             layer_id: str) -> Tuple[Dict[str, str], Set[str], Dict[str, Dict]]:
        """
        Gets the mapping of cluster to content, all new positive trace links, and source layer ids to create the project dataframes
        :param clusters: The clusters to extract.
        :param artifact_df: The dataframe containing artifacts in the clusters
        :param layer_id: Layer ID used to calcaluate run ID.
        :return:  mapping of cluster to content, all new positive trace links, and source layer ids to create the project dataframes
        """
        cluster_id_to_content = {}
        traces = {}
        source_layers = set()
        for cluster_id, artifacts in deepcopy(clusters).items():
            if artifact_df.get_artifact(cluster_id) is not None:  # duplicated artifact id
                clusters.pop(cluster_id)
                cluster_id = f"{cluster_id} {layer_id}"
                clusters[cluster_id] = artifacts
            artifact_content = []
            for i, artifact_id in enumerate(artifacts):
                artifact = artifact_df.get_artifact(artifact_id)
                artifact_content.append(ClusterDatasetCreator.CLUSTER_CONTENT_FORMAT.format(artifact[ArtifactKeys.CONTENT]))
                traces = DataFrameUtil.append(traces, EnumDict({TraceKeys.SOURCE: artifact_id, TraceKeys.TARGET: cluster_id,
                                                                TraceKeys.LABEL: 1}))  # add link between artifact and cluster
                source_layers.add(artifact[ArtifactKeys.LAYER_ID])
            cluster_id_to_content[cluster_id] = SPACE.join(artifact_content)  # combines the content of all artifacts in cluster

        return cluster_id_to_content, source_layers, traces
