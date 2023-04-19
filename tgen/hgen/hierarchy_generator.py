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


class HierarchyGenerator(BaseObject):

    def __init__(self, tgen_trainer: AbstractTrainer, hgen_trainer: AbstractTrainer):
        """
        Initializes the generator with the trainer used for creating trace links
        :param tgen_trainer: The trainer used for creating trace links
        :param hgen_trainer: The trainer used for generating higher level artifacts
        """
        self.tgen_trainer = tgen_trainer
        self.hgen_trainer = hgen_trainer

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
        assert orig_tgen_dataset.artifact_df is not None, "Hierarchy generation requires artifacts to be given."
        linked_layer_dataset = self._create_linked_dataset_for_intra_level_artifacts(orig_tgen_dataset.artifact_df, layer_id)

        # Step 2: Create clusters of related artifacts
        clusterer = ArtifactClusterer(linked_layer_dataset)
        clusters = clusterer.get_clusters(SupportedClusteringMethod.LOUVAIN)
        clustered_dataset = clusterer.create_dataset_from_clusters(SupportedClusteringMethod.LOUVAIN)

        # Step 3: Create higher-level artifacts from Clusters
        artifact_generations = self.hgen_trainer.perform_prediction(dataset=clustered_dataset).predictions

        # Step 4: Create new dataset with created artifacts
        return self._create_trace_dataset_with_generated_artifacts(artifact_generations, clustered_dataset,
                                                                   clusters, orig_tgen_dataset)

    def _create_trace_dataset_with_generated_artifacts(self, artifact_generations, clustered_dataset, clusters, orig_tgen_dataset) \
            -> TraceDataset:
        """
        Creates a dataset with traces between the original lower-level artifacts and the newly generated upper-level artifacts
        :param artifact_generations: A list of generated artifact content
        :param clustered_dataset: The dataset created from the clusters
        :param clusters: The clusters of artifacts for which the higher-level artifacts were generated
        :param orig_tgen_dataset: The original dataset used for trace generation
        :return: The dataset using the new generated artifacts
        """
        orig_trace_dataset = orig_tgen_dataset.trace_dataset if isinstance(orig_tgen_dataset, PromptDataset) else orig_tgen_dataset
        original_trace_df, original_layer_df = None, None
        if orig_trace_dataset is not None:
            original_trace_df = orig_trace_dataset.trace_df
            original_layer_df = orig_trace_dataset.layer_mapping_df

        artifact_df = self._create_artifact_df_with_generated_artifacts(artifact_generations, orig_tgen_dataset.artifact_df,
                                                                        clustered_dataset)
        layer_df = self._create_layer_df_with_generated_artifacts(orig_tgen_dataset.artifact_df, clustered_dataset, original_layer_df)
        trace_df = self._create_trace_df_with_generated_artifacts(artifact_df, clusters, original_trace_df)
        return TraceDataset(artifact_df, trace_df, layer_df)

    @staticmethod
    def _create_artifact_df_with_generated_artifacts(artifact_generations: List[str], orig_artifact_df: ArtifactDataFrame,
                                                     clustered_dataset: TraceDataset) -> ArtifactDataFrame:
        """
        Creates a dataframe with new artifacts generated to fill in an upper level of the hierarchy
        :param artifact_generations: A list of generated artifact content
        :param orig_artifact_df: The dataframe containing all original artifacts
        :param clustered_dataset: The dataset created from the clusters
        :return: The dataframe of generated artifacts
        """
        clustered_dataset.artifact_df[ArtifactKeys.CONTENT] = artifact_generations
        return ArtifactDataFrame.concat(orig_artifact_df, clustered_dataset.artifact_df)

    @staticmethod
    def _create_trace_df_with_generated_artifacts(new_artifacts_df: ArtifactDataFrame, clusters: Dict[Any, str],
                                                  orig_trace_df: TraceDataFrame, ) -> TraceDataFrame:
        """
        Creates a dataframe of traces including the new trace links between the original lower-level artifacts
        and the newly generated upper-level artifacts
        :param new_artifacts_df: A dataframe of generated artifacts
        :param clusters: The clusters of artifacts for which the higher-level artifacts were generated
        :param orig_trace_df: A dataframe of the original trace links in the dataset
        :return: The dataframe containing new and old trace links
        """
        sources, targets = list(clusters.keys()), list(clusters.values())
        trace_df = TraceDataFrame({TraceKeys.SOURCE: sources,
                                   TraceKeys.TARGET: targets,
                                   TraceKeys.LABEL: [1 for _ in clusters]})
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [HierarchyGenerator._get_layer_of_artifacts(new_artifacts_df,
                                                                                                      artifact_id=sources[0])],
                                   LayerKeys.TARGET_TYPE: [HierarchyGenerator._get_layer_of_artifacts(new_artifacts_df,
                                                                                                      artifact_id=targets[0])]})
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=new_artifacts_df, trace_df=trace_df,
                                                               layer_mapping_df=layer_df)

        return  TraceDataFrame.concat(trace_df, orig_trace_df) if orig_trace_df is not None else trace_df

    @staticmethod
    def _create_layer_df_with_generated_artifacts(orig_artifact_df: ArtifactDataFrame, cluster_dataset: TraceDataset,
                                                  original_layer_df: LayerDataFrame = None) -> LayerDataFrame:
        """
        Creates a layer dataframe connecting the original lower-level artifacts with the newly generated upper-level artifacts
        :param orig_artifact_df: The dataframe containing all original artifacts
        :param cluster_dataset: The dataset created from the clusters
        :param original_layer_df: The dataframe containing the original layers for the dataset
        :return: The dataframe with the new layer ids added
        """
        source_layer = HierarchyGenerator._get_layer_of_artifacts(orig_artifact_df)
        target_layer = HierarchyGenerator._get_layer_of_artifacts(cluster_dataset.artifact_df)

        layer_df = LayerDataFrame() if original_layer_df is None else original_layer_df
        layer_df.add_layer(source_layer, target_layer)

        return layer_df

    def _create_linked_dataset_for_intra_level_artifacts(self, artifacts_df: ArtifactDataFrame, layer_id: Any = None) -> TraceDataset:
        """
        Creates a trace dataset from predictions for trace links within the same layer
        :param layer_id: ID of the layer to make predictions for
        :return: The dataset containing the trace link predictions
        """
        single_layer_dataset = self._create_trace_dataset_for_single_layer(artifacts_df, layer_id)
        prediction_entries = self.tgen_trainer.perform_prediction(dataset=single_layer_dataset).prediction_entries
        for entry in prediction_entries:
            entry[TraceKeys.LABEL.value] = entry.pop("score")  # replace score with label to use scores as soft labels
        trace_df = TraceDataFrame(prediction_entries)
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

    @staticmethod
    def _get_layer_of_artifacts(artifact_df: ArtifactDataFrame, artifact_id: Any = None) -> Any:
        """
        Gets the id of the layer for the given artifacts
        :param artifact_df: The dataframe containing the artifacts
        :return: THe id of the layer
        """
        artifact_id = list(artifact_df.index)[0] if not artifact_id else artifact_id
        return artifact_df.get_artifact(artifact_id)[ArtifactKeys.LAYER_ID]
