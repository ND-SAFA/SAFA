from copy import deepcopy
from typing import List, Any, Union, Type

from tgen.data.clustering.SupportedClusteringMethod import SupportedClusteringMethod
from tgen.data.clustering.i_clustering import Clusters
from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil


class HierarchyGenerator(BaseObject):

    def __init__(self, hgen_trainer_class: Type[AbstractTrainer], dataset_creator_for_sources: TraceDatasetCreator = None,
                 tgen_trainer: AbstractTrainer = None, **hgen_trainer_params):
        """
        Initializes the generator with the trainer used for creating trace links
        :param tgen_trainer: The trainer used for creating trace links
        :param hgen_trainer: The trainer used for generating higher level artifacts
        """
        assert tgen_trainer or dataset_creator_for_sources, "Must provide either a dataset creator to make a " \
                                                            "dataset with traces between artifacts of the source layer " \
                                                            "or a trace generation trainer to create one."
        self.tgen_trainer = tgen_trainer
        self.hgen_trainer_class = hgen_trainer_class
        self.hgen_trainer_params = hgen_trainer_params
        self.dataset_creator_for_sources = dataset_creator_for_sources

    def run(self, layer_id: Any) -> TraceDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :param layer_id: ID of the layer to generate higher-level artifacts for
        :return:  A new trace dataset containing generated higher-level artifacts
        """
        # Step 1: Create trace links on between artifacts of the given layer (may be reused if dataset_creator_for_sources provided)
        if self.tgen_trainer:
            trace_dataset_with_sources = self.tgen_trainer.trainer_dataset_manager[DatasetRole.EVAL]
            assert trace_dataset_with_sources.artifact_df is not None, "Artifacts are required for trace generation."
            source_layer_only_dataset = self._create_linked_dataset_for_intra_level_artifacts(trace_dataset_with_sources.artifact_df,
                                                                                              layer_id)
        else:
            trace_dataset_with_sources = self.dataset_creator_for_sources.create()
            source_layer_only_dataset = self._create_trace_dataset_with_single_layer(trace_dataset_with_sources.artifact_df,
                                                                                     layer_id,
                                                                                     trace_dataset_with_sources.trace_df)

        # Step 2: Create clusters of related artifacts
        cluster_dataset_creator = ClusterDatasetCreator(source_layer_only_dataset, SupportedClusteringMethod.LOUVAIN)

        # Step 3: Create higher-level artifacts from Clusters
        hgen_dataset_manager = TrainerDatasetManager(eval_dataset_creator=cluster_dataset_creator)
        hgen_trainer = self.hgen_trainer_class(trainer_dataset_manager=hgen_dataset_manager, **self.hgen_trainer_params)
        artifact_generations = hgen_trainer.perform_prediction().predictions

        # Step 4: Create new dataset with created artifacts
        return self._create_trace_dataset_with_generated_artifacts(artifact_generations, hgen_dataset_manager[DatasetRole.EVAL],
                                                                   trace_dataset_with_sources,
                                                                   cluster_dataset_creator.get_clusters(),
                                                                   source_layer=layer_id,
                                                                   target_layer=cluster_dataset_creator.layer_id)

    def _create_trace_dataset_with_generated_artifacts(self, artifact_generations: List[str],
                                                       hgen_dataset: TraceDataset,
                                                       original_artifacts_dataset: Union[PromptDataset, TraceDataset],
                                                       clusters: Clusters,
                                                       source_layer: str, target_layer: str) -> TraceDataset:
        """
        Creates a dataset with traces between the original lower-level artifacts and the newly generated upper-level artifacts
        :param artifact_generations: A list of generated artifact content
        :param hgen_dataset: The dataset created from the clusters
        :param original_artifacts_dataset: The original dataset used for trace generation
        :param source_layer: The id of the source layer (original artifacts)
        :param target_layer: The id of the target layer (generated artifacts)
        :return: The dataset using the new generated artifacts
        """
        original_artifact_df = original_artifacts_dataset.artifact_df
        original_trace_dataset = original_artifacts_dataset.trace_dataset if isinstance(original_artifacts_dataset,
                                                                                        PromptDataset) else original_artifacts_dataset
        original_trace_df, original_layer_df = None, None
        if original_trace_dataset is not None:
            original_trace_df = original_trace_dataset.trace_df
            original_layer_df = original_trace_dataset.layer_mapping_df

        artifact_df = self._create_artifact_df_with_generated_artifacts(artifact_generations, original_artifact_df, hgen_dataset)
        layer_df = self._create_layer_df_with_generated_artifacts(source_layer, target_layer, original_layer_df)
        trace_df = self._create_trace_df_with_generated_artifacts(artifact_df, clusters, original_trace_df)
        return TraceDataset(artifact_df, trace_df, layer_df)

    @staticmethod
    def _create_artifact_df_with_generated_artifacts(artifact_generations: List[str], orig_artifact_df: ArtifactDataFrame,
                                                     hgen_dataset: TraceDataset) -> ArtifactDataFrame:
        """
        Creates a dataframe with new artifacts generated to fill in an upper level of the hierarchy
        :param artifact_generations: A list of generated artifact content
        :param orig_artifact_df: The dataframe containing all original artifacts
        :param hgen_dataset: The dataset created from the clusters
        :return: The dataframe of generated artifacts
        """
        hgen_dataset.artifact_df[ArtifactKeys.CONTENT] = artifact_generations
        return ArtifactDataFrame.concat(orig_artifact_df, hgen_dataset.artifact_df)

    @staticmethod
    def _create_trace_df_with_generated_artifacts(new_artifacts_df: ArtifactDataFrame,
                                                  clusters: Clusters,
                                                  orig_trace_df: TraceDataFrame = None) -> TraceDataFrame:
        """
        Creates a dataframe of traces including the new trace links between the original lower-level artifacts
        and the newly generated upper-level artifacts
        :param new_artifacts_df: A dataframe of generated artifacts
        :param orig_trace_df: A dataframe of the original trace links in the dataset
        :param clusters: Dictionary mapping artifact id to its associated cluster
        :return: The dataframe containing new and old trace links
        """
        sources, targets = list(clusters.keys()), list(clusters.values())
        trace_df = TraceDataFrame({TraceKeys.SOURCE: sources,
                                   TraceKeys.TARGET: targets,
                                   TraceKeys.LABEL: [1 for _ in sources]})
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [new_artifacts_df.get_artifact(sources[0])[ArtifactKeys.LAYER_ID]],
                                   LayerKeys.TARGET_TYPE: [new_artifacts_df.get_artifact(targets[0])[ArtifactKeys.LAYER_ID]]})
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=new_artifacts_df, trace_df=trace_df,
                                                               layer_mapping_df=layer_df)

        return TraceDataFrame.concat(trace_df, orig_trace_df) if orig_trace_df is not None else trace_df

    @staticmethod
    def _create_layer_df_with_generated_artifacts(source_layer: str, target_layer: str,
                                                  original_layer_df: LayerDataFrame = None) -> LayerDataFrame:
        """
        Creates a layer dataframe connecting the original lower-level artifacts with the newly generated upper-level artifacts
        :param source_layer: The id of the source layer (original artifacts)
        :param target_layer: The id of the target layer (generated artifacts)
        :param original_layer_df: The dataframe containing the original layers for the dataset
        :return: The dataframe with the new layer ids added
        """
        layer_df = LayerDataFrame() if original_layer_df is None else deepcopy(original_layer_df)
        layer_df.add_layer(source_layer, target_layer)
        return layer_df

    def _create_linked_dataset_for_intra_level_artifacts(self, artifacts_df: ArtifactDataFrame, layer_id: Any = None) -> TraceDataset:
        """
        Creates a trace dataset from predictions for trace links within the same layer
        :param layer_id: ID of the layer to make predictions for
        :return: The dataset containing the trace link predictions
        """
        single_layer_dataset = self._create_trace_dataset_with_single_layer(artifacts_df, layer_id)
        prediction_entries = self.tgen_trainer.perform_prediction(dataset=single_layer_dataset).prediction_entries
        for entry in prediction_entries:
            entry[TraceKeys.LABEL.value] = entry.pop("score")  # replace score with label to use scores as soft labels
        trace_df = TraceDataFrame(prediction_entries)
        return TraceDataset(artifact_df=single_layer_dataset.artifact_df, trace_df=trace_df,
                            layer_mapping_df=single_layer_dataset.layer_mapping_df)

    @staticmethod
    def _create_trace_dataset_with_single_layer(original_artifact_df: ArtifactDataFrame, layer_id: Any,
                                                original_trace_df: TraceDataFrame = None) -> TraceDataset:
        """
        Creates a trace dataset for a single layer
        :param original_artifact_df: A dataframe containing artifacts including those for the layer
        :param layer_id: ID of the layer to construct a dataset for
        :param original_trace_df: A dataframe containing intra layer traces for the layer
        :return: The trace dataset
        """
        layer_artifact_df = original_artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] == layer_id)
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [layer_id],
                                   LayerKeys.TARGET_TYPE: [layer_id]})
        layer_trace_df = TraceDataFrame() if original_trace_df is None else \
            TraceDataFrame(DataFrameUtil.filter_df_by_row(original_trace_df,
                                                          lambda row: row[TraceKeys.SOURCE.value] in layer_artifact_df
                                                                      and row[TraceKeys.TARGET.value] in layer_artifact_df))
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=layer_artifact_df, trace_df=layer_trace_df,
                                                               layer_mapping_df=layer_df)
        return TraceDataset(artifact_df=layer_artifact_df, trace_df=trace_df, layer_mapping_df=layer_df)
