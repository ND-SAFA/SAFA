import os
import uuid
from copy import deepcopy
from datetime import datetime
from typing import List, Any, Union

from tgen.data.clustering.SupportedClusteringMethod import SupportedClusteringMethod
from tgen.data.clustering.i_clustering import Clusters
from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.exporters.csv_exporter import CSVExporter
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.csv_keys import CSVKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.logging.logger_manager import logger


class HierarchyGenerator(BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """

    def __init__(self, args: HGenArgs):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        self.args = args

    def run(self, export_path: str, save_dataset_checkpoints: bool = True) -> str:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """
        export_path = os.path.join(export_path, str(uuid.uuid4()))
        # Step 1: Create trace links on between artifacts of the given layer (may be reused if dataset_creator_for_sources provided)
        if self.args.tgen_trainer:
            self._update_trainer_args(self.args.tgen_trainer, export_path)
            logger.info(f"Generating trace links between artifacts in the {self.args.source_layer_id} (source) layer")
            trace_dataset_with_sources = self.args.tgen_trainer.trainer_dataset_manager[DatasetRole.EVAL]
            self._save_dataset_checkpoint(trace_dataset_with_sources, export_path, save_dataset_checkpoints,
                                          filename="initial_dataset_with_sources")
            assert trace_dataset_with_sources.artifact_df is not None, "Artifacts are required for trace generation."
            source_layer_only_dataset = self._create_linked_dataset_for_intra_level_artifacts(trace_dataset_with_sources.artifact_df)
            if save_dataset_checkpoints:
                source_layer_only_dataset.trace_df.to_csv(os.path.join(export_path, "linked_source_layer_dataset.csv"))
        else:
            trace_dataset_with_sources = self.args.dataset_creator_for_sources.create()
            source_layer_only_dataset = self._create_trace_dataset_with_single_layer(trace_dataset_with_sources.artifact_df,
                                                                                     self.args.source_layer_id,
                                                                                     trace_dataset_with_sources.trace_df)

        # Step 2: Create clusters of related artifacts
        cluster_dataset_creator = ClusterDatasetCreator(source_layer_only_dataset, SupportedClusteringMethod.LOUVAIN)

        # Step 3: Create higher-level artifacts from Clusters
        hgen_dataset_manager = TrainerDatasetManager(eval_dataset_creator=cluster_dataset_creator)
        hgen_trainer = self.args.hgen_trainer_type.value(trainer_dataset_manager=hgen_dataset_manager,
                                                         prompt_creator=self.args.hgen_prompt_creator,
                                                         trainer_args=self.args.hgen_trainer_args,
                                                         base_model=self.args.hgen_base_model)
        self._update_trainer_args(hgen_trainer, export_path)
        logger.info(f"Generating content for {len(hgen_dataset_manager[DatasetRole.EVAL].artifact_df)} higher-level artifacts")
        artifact_generations = hgen_trainer.perform_prediction().predictions

        # Step 4: Create new dataset with created artifacts
        generated_dataset = self._create_trace_dataset_with_generated_artifacts(artifact_generations,
                                                                                hgen_dataset_manager[DatasetRole.EVAL],
                                                                                trace_dataset_with_sources,
                                                                                cluster_dataset_creator.get_clusters(),
                                                                                target_layer_id=cluster_dataset_creator.layer_id)
        return self._save_dataset_checkpoint(generated_dataset, export_path, save_dataset_checkpoints=True,
                                             filename="final_generated_dataset")

    def _create_trace_dataset_with_generated_artifacts(self, artifact_generations: List[str],
                                                       hgen_dataset: TraceDataset,
                                                       original_sources_dataset: Union[PromptDataset, TraceDataset],
                                                       clusters: Clusters, target_layer_id: str) -> TraceDataset:
        """
        Creates a dataset with traces between the original lower-level artifacts and the newly generated upper-level artifacts
        :param artifact_generations: A list of generated artifact content
        :param hgen_dataset: The dataset created from the clusters
        :param original_sources_dataset: The original dataset used for trace generation
        :param target_layer_id: The id of the target layer (generated artifacts)
        :return: The dataset using the new generated artifacts
        """
        original_artifact_df = original_sources_dataset.artifact_df
        original_trace_dataset = original_sources_dataset.trace_dataset if isinstance(original_sources_dataset,
                                                                                      PromptDataset) else original_sources_dataset
        original_trace_df, original_layer_df = None, None
        if original_trace_dataset is not None:
            original_trace_df = original_trace_dataset.trace_df
            original_layer_df = original_trace_dataset.layer_mapping_df

        artifact_df = self._create_artifact_df_with_generated_artifacts(artifact_generations, original_artifact_df, hgen_dataset)
        layer_df = self._create_layer_df_with_generated_artifacts(self.args.source_layer_id, target_layer_id, original_layer_df)
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
        :return: The dataframe with the new layer ids added.
        """
        layer_df = LayerDataFrame() if original_layer_df is None else deepcopy(original_layer_df)
        layer_df.add_layer(source_layer, target_layer)
        return layer_df.filter_by_row(lambda row: row[LayerKeys.SOURCE_TYPE.value] != row[LayerKeys.TARGET_TYPE.value])

    def _create_linked_dataset_for_intra_level_artifacts(self, artifacts_df: ArtifactDataFrame) -> TraceDataset:
        """
        Creates a trace dataset from predictions for trace links within the same layer
        :param artifacts_df: Dataframe containing all source artifacts
        :return: The dataset containing the trace link predictions
        """
        single_layer_dataset = self._create_trace_dataset_with_single_layer(artifacts_df, self.args.source_layer_id)
        prediction_entries = self.args.tgen_trainer.perform_prediction(dataset=single_layer_dataset).prediction_entries
        for entry in prediction_entries:
            entry[TraceKeys.LABEL.value] = entry.pop("score")  # replace score with label to use scores as soft labels
        trace_df = TraceDataFrame(prediction_entries)
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=single_layer_dataset.artifact_df, trace_df=trace_df,
                                                               layer_mapping_df=single_layer_dataset.layer_mapping_df)
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

    @staticmethod
    def _save_dataset_checkpoint(dataset: Union[TraceDataset, PromptDataset], export_path: str, save_dataset_checkpoints: bool,
                                 filename: str = None) -> str:
        """
        Exports the dataset to csv
        :param dataset: The dataset to export
        :param export_path: The base path to export to
        :param filename: Name of the file to use when saving the dataset
        :return: The full export path
        """
        if not save_dataset_checkpoints:
            return ''
        current_time_string = datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')
        filename = current_time_string if not filename else filename
        full_export_path = os.path.join(export_path, filename)
        exporter_class = SafaExporter if isinstance(dataset, TraceDataset) or dataset.trace_dataset is not None else CSVExporter
        if issubclass(exporter_class, CSVExporter):
            full_export_path += CSVKeys.EXT
        exporter = exporter_class(export_path=full_export_path, dataset=dataset)
        exporter.export()
        logger.info(f"Dataset checkpoint saved to {full_export_path} ")
        return full_export_path

    @staticmethod
    def _update_trainer_args(trainer: AbstractTrainer, export_path: str) -> None:
        """
        Sets the output directory of the trainer's args to the export path
        :param trainer: The trainer to update output dir for
        :param export_path: The path to set the output dir to
        :return: None
        """
        if hasattr(trainer.trainer_args, "output_dir") and trainer.trainer_args.output_dir is None:
            trainer.trainer_args.output_dir = export_path
        if hasattr(trainer.trainer_args, "metrics"):
            trainer.trainer_args.metrics = []
