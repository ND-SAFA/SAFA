import os
import uuid
from datetime import datetime
from typing import Any, List, Union, Type

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from tgen.data.exporters.csv_exporter import CSVExporter
from tgen.data.exporters.dataframe_exporter import DataFrameExporter
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.csv_keys import CSVKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.file_util import FileUtil
from tgen.util.llm_response_util import LLMResponseUtil
from tgen.util.logging.logger_manager import logger


class HierarchyGenerator(BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """
    BASE_PROMPT = SupportedPrompts.ARTIFACT_GENERATION
    GENERATION_TAG = "doc"

    def __init__(self, args: HGenArgs, hgen_llm_manager: AbstractLLMManager):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        self.args = args
        self.hgen_llm_manager = hgen_llm_manager

    def run(self) -> TraceDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """
        export_path = os.path.join(self.args.export_path, str(uuid.uuid4())) if self.args.export_path else None

        # Step 1: Create trace links on between artifacts of the given layer (may be reused if dataset_creator_for_sources provided)
        if self.args.tgen_trainer:  # links need generated
            dataset_with_sources = self._get_trace_dataset_with_sources_from_trainer(export_path)
            source_layer_only_dataset = self._create_linked_dataset_for_intra_level_artifacts(
                dataset_with_sources.artifact_df, export_path)
        else:  # links pre-generated or not needed
            dataset_with_sources = self.args.dataset_creator_for_sources.create() if self.args.dataset_for_sources is None \
                else self.args.dataset_for_sources
            self.save_dataset_checkpoint(dataset_with_sources, export_path, filename="initial_dataset_with_sources")
            source_layer_only_dataset = self._create_dataset_with_single_layer(dataset_with_sources.artifact_df,
                                                                               self.args.source_layer_id,
                                                                               dataset_with_sources.trace_dataset.trace_df
                                                                               if dataset_with_sources.trace_dataset else None)
        # Step 2: Create clusters of related artifacts
        target_layer_id = self._get_target_layer_id(dataset_with_sources)
        cluster_dataset_creator = ClusterDatasetCreator(prompt_dataset=source_layer_only_dataset,
                                                        layer_id=target_layer_id,
                                                        cluster_methods=self.args.clustering_method,
                                                        manual_clusters=self.args.manual_clusters, **self.args.clustering_params)

        # Step 3: Create higher-level artifacts from Clusters
        hgen_dataset_manager = TrainerDatasetManager(eval_dataset_creator=cluster_dataset_creator)
        artifact_generations = self._generate_artifact_content(hgen_dataset_manager, export_path=export_path)

        # Step 4: Create new dataset with created artifacts
        return self._create_trace_dataset_with_generated_artifacts(artifact_generations,
                                                                   hgen_dataset_manager[DatasetRole.EVAL],
                                                                   dataset_with_sources, export_path=export_path)

    def _get_trace_dataset_with_sources_from_trainer(self, export_path: str) -> TraceDataset:
        """
        Gets the trace dataset containing the source artifacts from the tgen trainer
        :param export_path: The path to export the dataset to
        :return: The dataset
        """
        self._update_trainer_args(self.args.tgen_trainer, export_path)
        trace_dataset_with_sources = self.args.tgen_trainer.trainer_dataset_manager[DatasetRole.EVAL]
        self.save_dataset_checkpoint(trace_dataset_with_sources, export_path, filename="initial_dataset_with_sources")
        assert trace_dataset_with_sources.artifact_df is not None, "Artifacts are required for trace generation."
        return trace_dataset_with_sources

    def _generate_artifact_content(self, hgen_dataset_manager: TrainerDatasetManager, export_path: str) -> List[str]:
        """
        Generates the content for the new artifacts using the given dataset
        :param hgen_dataset_manager: Contains the dataset used to create
        :param export_path: The path to export dataset checkpoints to
        :return: The content for the generated artifacts
        """
        example = self._get_example_of_target_type()
        prompt_creator = GenerationPromptCreator(prompt_args=self.hgen_llm_manager.prompt_args,
                                                 base_prompt=self.BASE_PROMPT.value.format(artifact_type=self.args.target_type,
                                                                                           example=example))
        hgen_trainer = LLMTrainer(llm_manager=self.hgen_llm_manager,
                                  trainer_dataset_manager=hgen_dataset_manager,
                                  prompt_creator=prompt_creator)
        if export_path:
            self._update_trainer_args(hgen_trainer, export_path)
        logger.info(f"Generating content for {len(hgen_dataset_manager[DatasetRole.EVAL].artifact_df)} higher-level artifacts")
        artifact_generations = hgen_trainer.perform_prediction().predictions
        return artifact_generations

    def _create_trace_dataset_with_generated_artifacts(self, artifact_generations: List[str],
                                                       hgen_dataset: TraceDataset,
                                                       original_sources_dataset: Union[PromptDataset, TraceDataset],
                                                       export_path: str) -> TraceDataset:
        """
        Creates a dataset with traces between the original lower-level artifacts and the newly generated upper-level artifacts
        :param artifact_generations: A list of generated artifact content
        :param hgen_dataset: The dataset created from the clusters
        :param original_sources_dataset: The original dataset used for trace generation
        :param export_path: The path to export the dataset to
        :return: The dataset using the new generated artifacts
        """
        original_artifact_df = original_sources_dataset.artifact_df

        original_trace_dataset = original_sources_dataset.trace_dataset if isinstance(original_sources_dataset,
                                                                                      PromptDataset) else original_sources_dataset
        original_trace_df, original_layer_df = None, None
        if original_trace_dataset:
            original_trace_df = original_trace_dataset.trace_df
            original_layer_df = original_trace_dataset.layer_df

        artifact_df = self._create_artifact_df_with_generated_artifacts(artifact_generations, hgen_dataset.artifact_df,
                                                                        original_artifact_df)
        layer_df = self._create_layer_df_with_generated_artifacts(hgen_dataset.layer_df, original_layer_df)
        trace_df = self._create_trace_df_with_generated_artifacts(hgen_dataset.trace_df, artifact_df, original_trace_df)
        dataset = TraceDataset(artifact_df, trace_df, layer_df)
        save_path = self.save_dataset_checkpoint(dataset, export_path, filename="final_generated_dataset")
        self.save_dataset_checkpoint(dataset, save_path, filename="safa", exporter_class=SafaExporter)
        return dataset

    @staticmethod
    def _create_artifact_df_with_generated_artifacts(artifact_generations: List[str], hgen_artifacts_df: ArtifactDataFrame,
                                                     orig_artifact_df: ArtifactDataFrame) -> ArtifactDataFrame:
        """
        Creates a dataframe with new artifacts generated to fill in an upper level of the hierarchy
        :param artifact_generations: A list of generated artifact content
        :param orig_artifact_df: The dataframe containing all original artifacts
        :param hgen_artifacts_df: The dataframe containing artifacts created from the clusters
        :return: The dataframe of generated artifacts
        """
        artifact_content = [HierarchyGenerator._extract_generated_content(gen) for gen in artifact_generations]
        hgen_artifacts_df[ArtifactKeys.CONTENT] = artifact_content
        return ArtifactDataFrame.concat(orig_artifact_df, hgen_artifacts_df)

    @staticmethod
    def _extract_generated_content(generation: str) -> str:
        """
        Extracts the new artifact content from the LLM generation
        :param generation: The response from the LLM for the artifact content
        :return: The new artifact content
        """
        return LLMResponseUtil.parse(generation, HierarchyGenerator.GENERATION_TAG)

    @staticmethod
    def _create_trace_df_with_generated_artifacts(hgen_trace_df: TraceDataFrame, artifact_df: ArtifactDataFrame,
                                                  orig_trace_df: TraceDataFrame = None) -> TraceDataFrame:
        """
        Creates a dataframe of traces including the new trace links between the original lower-level artifacts
        and the newly generated upper-level artifacts
        :param hgen_trace_df: The dataframe containing traces created from the clusters
        :param orig_trace_df: A dataframe of the original trace links in the dataset
        :return: The dataframe containing new and old trace links
        """
        trace_df = TraceDataFrame.concat(hgen_trace_df, orig_trace_df) if orig_trace_df is not None else hgen_trace_df
        return trace_df.filter_by_row(lambda row: artifact_df.get_artifact(row[TraceKeys.SOURCE.value])[ArtifactKeys.LAYER_ID] !=
                                                  artifact_df.get_artifact(row[TraceKeys.TARGET.value])[ArtifactKeys.LAYER_ID])

    @staticmethod
    def _create_layer_df_with_generated_artifacts(hgen_layer_df: LayerDataFrame,
                                                  original_layer_df: LayerDataFrame = None) -> LayerDataFrame:
        """
        Creates a layer dataframe connecting the original lower-level artifacts with the newly generated upper-level artifacts
        :param hgen_layer_df: The dataframe containing layers b/w artifacts and the clusters
        :param original_layer_df: The dataframe containing the original layers for the dataset
        :return: The dataframe with the new layer ids added.
        """
        layer_df = LayerDataFrame.concat(hgen_layer_df, original_layer_df) if original_layer_df is not None else hgen_layer_df
        return layer_df.filter_by_row(lambda row: row[LayerKeys.SOURCE_TYPE.value] != row[LayerKeys.TARGET_TYPE.value])

    def _create_linked_dataset_for_intra_level_artifacts(self, artifacts_df: ArtifactDataFrame, export_path: str) -> PromptDataset:
        """
        Creates a trace dataset from predictions for trace links within the same layer
        :param artifacts_df: Dataframe containing all source artifacts
        :param export_path: The path to export the dataset to
        :return: The dataset containing the trace link predictions
        """
        logger.info(f"Generating trace links between artifacts in the {self.args.source_layer_id} (source) layer")
        single_layer_dataset = self._create_dataset_with_single_layer(artifacts_df, self.args.source_layer_id)
        prediction_entries = self.args.tgen_trainer.perform_prediction(dataset=single_layer_dataset).prediction_entries
        for entry in prediction_entries:
            entry[TraceKeys.LABEL.value] = entry.pop("score")  # replace score with label to use scores as soft labels
        trace_df = TraceDataFrame(prediction_entries)
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=single_layer_dataset.artifact_df, trace_df=trace_df,
                                                               layer_mapping_df=single_layer_dataset.layer_df)
        dataset = TraceDataset(artifact_df=single_layer_dataset.artifact_df, trace_df=trace_df,
                               layer_df=single_layer_dataset.layer_df)
        self.save_dataset_checkpoint(dataset, export_path, "linked_source_layer_dataset")
        return PromptDataset(trace_dataset=dataset)

    @staticmethod
    def _create_dataset_with_single_layer(original_artifact_df: ArtifactDataFrame, layer_id: Any,
                                          original_trace_df: TraceDataFrame = None) -> PromptDataset:
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
        return PromptDataset(trace_dataset=TraceDataset(artifact_df=layer_artifact_df, trace_df=trace_df, layer_df=layer_df))

    @staticmethod
    def save_dataset_checkpoint(dataset: Union[TraceDataset, PromptDataset], export_path: str = None,
                                filename: str = None, exporter_class: Type[AbstractDatasetExporter] = None) -> str:
        """
        Exports the dataset to csv
        :param dataset: The dataset to export
        :param export_path: The base path to export to
        :param filename: Name of the file to use when saving the dataset
        :param exporter_class: Exporter class to specify if not using defaults
        :return: The full export path
        """
        if not export_path:
            return EMPTY_STRING
        FileUtil.create_dir_safely(export_path)
        current_time_string = datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')
        filename = current_time_string if not filename else filename
        full_export_path = os.path.join(export_path, filename)
        if isinstance(dataset, PromptDataset) and dataset.trace_dataset is not None:
            dataset = dataset.trace_dataset
        if exporter_class is None:
            exporter_class = DataFrameExporter if isinstance(dataset, TraceDataset) else CSVExporter
        if issubclass(exporter_class, CSVExporter):
            full_export_path += CSVKeys.EXT
        exporter = exporter_class(export_path=full_export_path, dataset=dataset)
        exporter.export()
        logger.info(f"Dataset checkpoint saved to {full_export_path} ")
        return full_export_path

    def _get_target_layer_id(self, dataset_with_sources: PromptDataset) -> str:
        """
        Gets the id of the new target layer
        :param dataset_with_sources: The dataset containing source artifacts
        :return: The id of the new target layer
        """
        layer_id = self.args.target_type
        if self.args.target_type in dataset_with_sources.artifact_df[ArtifactKeys.LAYER_ID].values:
            layer_id = f"{layer_id}_{uuid.uuid4()}"
        return layer_id

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

    def _get_example_of_target_type(self) -> str:
        """
        Gets an example of the target artifact to use in the generation prompt for theLLM
        :return: An example of the target artifact
        """
        example_prompt_format = SupportedPrompts.ARTIFACT_EXAMPLE.value.format(artifact_type=self.args.target_type)
        example_prompt = GenerationPromptCreator(prompt_args=self.args.llm_manager_for_example.prompt_args,
                                                 base_prompt=example_prompt_format).create('')[PromptKeys.PROMPT]
        args = self.args.llm_manager_for_example.llm_args.to_params(TrainerTask.PREDICT, LLMCompletionType.GENERATION)
        res = self.args.llm_manager_for_example.make_completion_request(prompt=example_prompt,
                                                                        completion_type=LLMCompletionType.GENERATION,
                                                                        **args)
        example = LLMResponseUtil.parse(res.batch_responses[0], "example")
        return example
