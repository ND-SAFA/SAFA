import uuid
from copy import deepcopy
from typing import List, Dict, Any

from tgen.data.clustering.SupportedClusteringMethod import SupportedClusteringMethod
from tgen.data.clustering.artifact_clusterer import ArtifactClusterer
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.enum_util import EnumDict


class HierarchyGenerator(BaseObject):

    def __init__(self, tgen_trainer: AbstractTrainer, hgen_trainer: AbstractTrainer):
        """
        Initializes the generator with the trainer used for creating trace links
        :param tgen_trainer: The trainer used for creating trace links
        :param hgen_trainer: The trainer used for generating higher level artifacts
        """
        self.tgen_trainer = tgen_trainer
        self.hgen_trainer = hgen_trainer
        self.target_layer_id = str(uuid.uuid4())

    def run(self, layer_id: Any) -> TraceDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :param layer_id: ID of the layer to generate higher-level artifacts for
        :return:  A new trace dataset containing generated higher-level artifacts
        """
        # Step 1: Create Trace Links on Summarized Dataset
        dataset_role = DatasetRole.SUMMARIZE if DatasetRole.SUMMARIZE in self.tgen_trainer.trainer_dataset_manager \
            else DatasetRole.EVAL
        orig_tgen_dataset = self.tgen_trainer.trainer_dataset_manager[dataset_role]
        linked_layer_dataset = self._create_linked_dataset_for_intra_level_artifacts(orig_tgen_dataset.artifact_df, layer_id)

        # Step 2: Create clusters of related artifacts
        clusterer = ArtifactClusterer(linked_layer_dataset)
        clusters = clusterer.get_clusters(SupportedClusteringMethod.LOUVAIN)
        clustered_dataset = clusterer.create_dataset_from_clusters(SupportedClusteringMethod.LOUVAIN)

        # Step 3: Create higher-level artifacts from Clusters
        artifact_generations = self.hgen_trainer.perform_prediction(dataset=clustered_dataset).predictions

        # Step 4: Create new dataset with created artifacts
        orig_tgen_dataset = orig_tgen_dataset.trace_dataset if isinstance(orig_tgen_dataset, PromptDataset) else orig_tgen_dataset
        return self._create_dataset_with_new_artifacts(artifact_generations, clusters, clustered_dataset,
                                                       orig_trace_dataset=orig_tgen_dataset if orig_tgen_dataset is not None
                                                       else linked_layer_dataset)

    def _create_dataset_with_new_artifacts(self, artifact_generations: List[str], clusters: Dict[Any, str],
                                           cluster_dataset: TraceDataset, orig_trace_dataset: TraceDataset) -> TraceDataset:
        """
        Creates a dataset with the new artifacts generated to fill in an upper level of the hierarchy
        :param artifact_generations: A list of generated artifact content
        :param clusters: The clusters of artifacts for which the higher-level artifacts were generated
        :param cluster_dataset: The dataset created from the clusters
        :param orig_trace_dataset: The original trace dataset
        :return: The new dataset with the generated artifacts
        """
        new_artifacts_df = ArtifactDataFrame({ArtifactKeys.ID: list(cluster_dataset.artifact_df.index),
                                              ArtifactKeys.CONTENT: artifact_generations,
                                              ArtifactKeys.LAYER_ID: [self.target_layer_id for _ in artifact_generations]})
        artifacts_df = ArtifactDataFrame.concat(new_artifacts_df, orig_trace_dataset.artifact_df)
        trace_df = TraceDataFrame({TraceKeys.SOURCE: list(clusters.keys()),
                                   TraceKeys.TARGET: list(clusters.values()),
                                   TraceKeys.LABEL: [1 for _ in clusters]})
        source_layer = orig_trace_dataset.artifact_df[ArtifactKeys.LAYER_ID][0]
        layer_df = deepcopy(orig_trace_dataset.layer_mapping_df)
        TraceDatasetCreator.generate_negative_links(layer_mapping_df=layer_df, artifact_df=artifacts_df, trace_df=trace_df)
        layer_df.add_layer(source_layer, self.target_layer_id)
        return TraceDataset(artifact_df=artifacts_df, trace_df=trace_df, layer_mapping_df=layer_df)

    def _create_linked_dataset_for_intra_level_artifacts(self, artifacts_df: ArtifactDataFrame, layer_id: Any = None) -> TraceDataset:
        """
        Creates a trace dataset from predictions for trace links within the same layer
        :param layer_id: ID of the layer to make predictions for
        :return: The dataset containing the trace link predictions
        """
        single_layer_dataset = self._create_trace_dataset_for_single_layer(artifacts_df, layer_id)
        prediction_entries = self.tgen_trainer.perform_prediction(dataset=single_layer_dataset).prediction_entries
        trace_df = TraceDataFrame([EnumDict({k if k != "score" else TraceKeys.LABEL: v for k, v in entry.items()})
                                   for entry in prediction_entries])  # replace score with label to use scores as soft labels
        return TraceDataset(artifact_df=single_layer_dataset.artifact_df, trace_df=trace_df,
                            layer_mapping_df=single_layer_dataset.layer_mapping_df)

    @staticmethod
    def _create_trace_dataset_for_single_layer(artifact_df: ArtifactDataFrame, layer_id: Any) -> TraceDataset:
        """
        Creates a trace dataset for a single layer
        :param artifact_df: A dataframe containing all project artifacts
        :param layer_id: ID of the layer to construct a dataset for
        :return: The trace dataset
        """
        artifact_df = ArtifactDataFrame(DataFrameUtil.filter_df_by_row(artifact_df,
                                                                       lambda row: row[ArtifactKeys.LAYER_ID.value] == layer_id))
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [layer_id],
                                   LayerKeys.TARGET_TYPE: [layer_id]})
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=artifact_df, trace_df=TraceDataFrame(),
                                                               layer_mapping_df=layer_df)
        return TraceDataset(artifact_df=artifact_df, trace_df=trace_df, layer_mapping_df=layer_df)
