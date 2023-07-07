import os
import re
import string
import uuid
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Tuple, Type, Union, Set

import bs4
from yaml.constructor import SafeConstructor

from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.constants.path_constants import GENERATION_QUESTIONNAIRE_PROMPTS_PATH
from tgen.constants.prediction_constants import HGEN_TOP_PREDICTION_MIN_THRESHOLD
from tgen.data.clustering.llm_clustering import LLMClustering
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from tgen.data.exporters.csv_exporter import CSVExporter
from tgen.data.exporters.dataframe_exporter import DataFrameExporter
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.csv_keys import CSVKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.jobs.trainer_jobs.ranking_job import RankingJob
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.token_limits import ModelTokenLimits
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.dict_util import DictUtil
from tgen.util.enum_util import EnumDict
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger
from tgen.util.state.state.llm_trainer_state import LLMTrainerState


class HierarchyGenerator(BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """
    GENERATION_INSTRUCTIONS = "Complete the following steps using your knowledge of the system:"
    TASK_PREFACE = f"{NEW_LINE} TASKS: {NEW_LINE}"
    RES_TOKENS_MIN = 20000

    def __init__(self, args: HGenArgs):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        self.args = args
        self._set_max_tokens(self.args.hgen_llm_manager)

    def run(self) -> TraceDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """
        export_path = os.path.join(self.args.export_path, str(uuid.uuid4())) if self.args.export_path else None
        original_dataset_complete, source_layer_only_dataset = self._get_source_datasets_for_generation(export_path)
        questionnaire = self._construct_questionnaire_for_generation()
        artifact_generation_content = self._generate_artifact_content(questionnaire, source_layer_only_dataset)
        refined_content = self._refine_generations(artifact_generation_content, source_layer_only_dataset)

        return self._create_trace_dataset_with_generated_artifacts(refined_content,
                                                                   original_dataset_complete,
                                                                   export_path=export_path)

    def _construct_questionnaire_for_generation(self) -> QuestionnairePrompt:
        """
        Constructs a questionnaire prompt that is used to generate the new artifacts
        :return: The questionnaire prompt that is used to generate the new artifacts
        """

        def construct_tag_from_yaml(loader, node):
            value = loader.construct_scalar(node)
            return bs4.Tag(value)

        instructions_prompt: Prompt = SupportedPrompts.HGEN_INSTRUCTIONS.value
        format_prompt: Prompt = Prompt("Finally, provide an example of the typical format for a {target_type}. "
                                       "The format should be for only the body of the {target_type} and should exclude any title.",
                                       response_manager=PromptResponseManager(response_tag="format",
                                                                              required_tag_ids=REQUIRE_ALL_TAGS))

        questionnaire_prompt_path = self._get_path_to_generation_questionnaire_prompt(
            self._convert_spaces_to_dashes(self.args.target_type))
        if os.path.exists(questionnaire_prompt_path):
            SafeConstructor.add_constructor('!!python/object:bs4.element.Tag', construct_tag_from_yaml)
            questionnaire_content = FileUtil.read_yaml(questionnaire_prompt_path)
        else:
            logger.info("Creating questionnaire prompt for generation\n")
            prompt_builder = PromptBuilder(prompts=[instructions_prompt, format_prompt])
            prompt_builder.format_prompts_with_var(target_type=self.args.target_type, source_type=self.args.source_type)
            questionnaire_content = self._get_predictions(prompt_builder, PromptDataset(),
                                                          response_prompt_ids={instructions_prompt.id, format_prompt.id})[0]
            FileUtil.write_yaml(questionnaire_content, questionnaire_prompt_path)
        questions = self._construct_question_prompts_from_output(*instructions_prompt.response_manager.get_all_tag_ids(),
                                                                 format_prompt.response_manager.response_tag,
                                                                 questionnaire_content)
        return QuestionnairePrompt(question_prompts=questions,
                                   instructions=self.GENERATION_INSTRUCTIONS)

    def _construct_question_prompts_from_output(self, step_id: str, name_id: str, instructions_id: str, deliverable_id: str,
                                                format_id: str, result: Dict) -> List[QuestionPrompt]:
        """
        Constructs the question prompts from the model output
        :param step_id: The id of the tag for the step
        :param name_id: The id of the tag for the step name
        :param instructions_id: The id of the tag for the step id
        :param deliverable_id: The id of the tag for the step deliverable
        :param format_id: The id of the tag for the artifact format
        :param result: The model output
        :return: The list of question prompts created from model output
        """
        steps = result[step_id]
        questions = []
        target_artifact_tag = self._convert_spaces_to_dashes(self.args.target_type)
        for i, step in enumerate(steps):
            if i == len(steps) - 1:
                response_tag = f"{target_artifact_tag}-drafts"
                response_instructions_format = f"Output the {self.args.target_type}s in a comma-deliminated list enclosed in"
            else:
                response_tag = self._convert_spaces_to_dashes(step[name_id][0])
                deliverable = step[deliverable_id][0]
                deliverable = deliverable[:-1] if deliverable[-1] in string.punctuation else deliverable
                response_instructions_format = f"Output {deliverable} enclosed in"
            response_manager = PromptResponseManager(response_tag=response_tag,
                                                     response_instructions_format=response_instructions_format + ' {}')
            question = QuestionPrompt(step[instructions_id][0], response_manager=response_manager)
            questions.append(question)
        response_manager = PromptResponseManager(response_tag=f"{target_artifact_tag}s",
                                                 formatter=lambda tag, val: [v for v in val.split(NEW_LINE) if v],
                                                 required_tag_ids=REQUIRE_ALL_TAGS)
        questions.append(QuestionPrompt(f"Finally, output the contents of the {self.args.target_type} "
                                        f"in a comma deliminated list using the following format: "
                                        f"{result[format_id][0]}", response_manager=response_manager))
        return questions

    def _generate_artifact_content(self, questionnaire: QuestionnairePrompt, source_layer_only_dataset: PromptDataset) \
            -> List[str]:
        """
        Creates the content for the new artifacts
        :param questionnaire: The questionnaire prompt given to the model to produce the generations
        :param source_layer_only_dataset: The dataset containing only the source layer
        :return: The generated artifact content
        """
        logger.info(f"Generating {self.args.target_type}s\n")
        prompt_builder = self._get_prompt_builder_for_generation(questionnaire, include_summary=True)
        generated_artifacts_tag = questionnaire.question_prompts[-1].response_manager.response_tag
        generation_predictions = self._get_predictions(prompt_builder, source_layer_only_dataset,
                                                       response_prompt_ids=questionnaire.id,
                                                       tags_for_response=generated_artifacts_tag,
                                                       return_first=True)
        generated_artifact_content = generation_predictions[0]
        return generated_artifact_content

    def _refine_generations(self, generated_artifact_content: List[str], source_layer_only_dataset: PromptDataset) -> List[str]:
        """
        Has the model refine the artifact generations
        :param generated_artifact_content: The original generated content
        :param source_layer_only_dataset: The dataset containing only the source layer
        :return: A list of refined artifact content
        """
        try:
            logger.info(f"Refining {len(generated_artifact_content)} {self.args.target_type}s\n")
            questionnaire = SupportedPrompts.HGEN_REFINE_QUESTIONNAIRE.value
            prompt_builder = self._get_prompt_builder_for_generation(questionnaire,
                                                                     SupportedPrompts.HGEN_REFINE_PROMPT)
            target_prompt = MultiArtifactPrompt(prompt_start="{target_type}S:",
                                                build_method=MultiArtifactPrompt.BuildMethod.NUMBERED,
                                                include_ids=False, data_type=MultiArtifactPrompt.DataType.ARTIFACT)
            target_prompt.format_value(target_type=self.args.target_type.upper())
            target_prompt_content = target_prompt.build(artifacts=[{ArtifactKeys.CONTENT: c} for c in generated_artifact_content])
            prompt_builder.add_prompt(Prompt(target_prompt_content), 1)
            generated_artifacts_tag = questionnaire.question_prompts[-1].response_manager.response_tag
            refined_artifact_content = self._get_predictions(prompt_builder, source_layer_only_dataset,
                                                             response_prompt_ids=questionnaire.id,
                                                             tags_for_response=generated_artifacts_tag,
                                                             return_first=True)[0]
        except Exception:
            logger.exception("Refining the artifact content failed. Using original content instead.")
            refined_artifact_content = generated_artifact_content
        return refined_artifact_content

    def _create_trace_dataset_with_generated_artifacts(self, artifact_generations: List[str],
                                                       original_dataset_complete: Union[PromptDataset, TraceDataset],
                                                       export_path: str) -> TraceDataset:
        """
        Creates a dataset with traces between the original lower-level artifacts and the newly generated upper-level artifacts
        :param artifact_generations: A list of generated artifact content
        :param original_dataset_complete: The original dataset used for trace generation
        :param export_path: The path to export the dataset to
        :return: The dataset using the new generated artifacts
        """
        original_artifact_df = original_dataset_complete.artifact_df

        original_trace_dataset = original_dataset_complete.trace_dataset if isinstance(original_dataset_complete,
                                                                                       PromptDataset) else original_dataset_complete
        original_trace_df, original_layer_df = None, None
        if original_trace_dataset:
            original_trace_df = original_trace_dataset.trace_df
            original_layer_df = original_trace_dataset.layer_df

        target_layer_id = self._get_target_layer_id(original_dataset_complete)

        new_artifact_df = self._create_artifact_df_with_generated_artifacts(artifact_generations, target_layer_id)
        self.save_dataset_checkpoint(PromptDataset(artifact_df=new_artifact_df), export_path, filename="generated_artifacts_only")

        new_layer_df = self._create_layer_df_with_generated_artifacts(target_layer_id)
        combined_artifact_df = ArtifactDataFrame.concat(original_artifact_df, new_artifact_df)
        new_trace_df = self._create_trace_df_with_generated_artifacts(combined_artifact_df)
        self.save_dataset_checkpoint(TraceDataset(artifact_df=new_artifact_df, trace_df=new_trace_df, layer_df=new_layer_df),
                                     export_path, filename="generated_dataset_checkpoint")

        new_trace_df = TraceDatasetCreator.generate_negative_links(layer_mapping_df=new_layer_df,
                                                                   artifact_df=combined_artifact_df, trace_df=new_trace_df)
        final_trace_df = TraceDataFrame.concat(original_trace_df, new_trace_df) if original_trace_df is not None else new_trace_df
        final_layer_df = LayerDataFrame.concat(original_layer_df, new_layer_df) if original_layer_df is not None else new_layer_df

        dataset = TraceDataset(combined_artifact_df, final_trace_df, final_layer_df)

        save_path = self.save_dataset_checkpoint(dataset, export_path, filename="final_generated_dataset")
        self.save_dataset_checkpoint(dataset, save_path, filename="safa", exporter_class=SafaExporter)
        return dataset

    def _create_artifact_df_with_generated_artifacts(self, artifact_generations: List[str],
                                                     target_layer_id: str) -> ArtifactDataFrame:
        """
        Creates a dataframe with new artifacts generated to fill in an upper level of the hierarchy
        :param artifact_generations: A list of generated artifact content
        :param target_layer_id: The id for the layer with the new generated artifacts
        :return: The dataframe of generated artifacts
        """
        new_artifact_df = ArtifactDataFrame({ArtifactKeys.ID: [str(uuid.uuid4()) for _ in artifact_generations],
                                             ArtifactKeys.CONTENT: artifact_generations,
                                             ArtifactKeys.LAYER_ID: [target_layer_id for _ in artifact_generations]})
        try:
            logger.info(f"Creating names for {len(new_artifact_df)} {self.args.target_type}\n")
            name_prompt = Prompt(f"Create a name for this {self.args.target_type}.",
                                 PromptResponseManager(response_tag="name", required_tag_ids=REQUIRE_ALL_TAGS))
            artifact_prompt = ArtifactPrompt(include_id=False)
            prompt_builder = PromptBuilder(prompts=[name_prompt, artifact_prompt])
            dataset = PromptDataset(artifact_df=new_artifact_df)
            names = self._get_predictions(prompt_builder, dataset, response_prompt_ids=name_prompt.id,
                                          tags_for_response=name_prompt.response_manager.response_tag, return_first=True)
            assert len(names) == len(new_artifact_df.index), "Number of predicted names does not match number of artifacts"
            duplicated_names = {name for name, count in Counter(names).items() if count > 1}
            assert len(duplicated_names) < 1, "Found duplicate names"  # TODO handle this case in the future if this is a problem
            new_artifact_df.index = names
        except Exception:
            logger.exception("Unable to generate names for the artifacts")
        return new_artifact_df

    def _create_trace_df_with_generated_artifacts(self, artifact_df: ArtifactDataFrame) -> TraceDataFrame:
        """
        Creates a dataframe of traces including the new trace links between the original lower-level artifacts
        and the newly generated upper-level artifacts
        :return: The dataframe containing new and old trace links
        """
        logger.info(f"Predicting links between {self.args.target_type} and {self.args.source_layer_id}\n")
        tracing_job = RankingJob(artifact_df=artifact_df, ranking_args={"min_threshold": HGEN_TOP_PREDICTION_MIN_THRESHOLD})
        trace_predictions: List[TracePredictionEntry] = tracing_job.run().body.prediction_entries
        traces = {}
        for entry in trace_predictions:
            link = EnumDict({
                **entry,
                TraceKeys.SOURCE: entry[TraceKeys.SOURCE.value],
                TraceKeys.TARGET: entry[TraceKeys.TARGET.value],
                TraceKeys.LABEL: 1
            })
            DataFrameUtil.append(traces, link)
        return TraceDataFrame(traces)

    def _create_layer_df_with_generated_artifacts(self, target_layer_id: str) -> LayerDataFrame:
        """
        Creates a layer dataframe connecting the original lower-level artifacts with the newly generated upper-level artifacts
        :param target_layer_id: The id of the new target layer
        :return: The dataframe with the new layer ids added.
        """
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [self.args.source_layer_id], LayerKeys.TARGET_TYPE: [target_layer_id]})
        return layer_df

    def _get_predictions(self, prompt_builder: PromptBuilder, dataset: PromptDataset, llm_manager: AbstractLLMManager = None,
                         response_prompt_ids: Union[Set, str] = None, tags_for_response: Union[Set, str] = None,
                         return_first: bool = False) -> Any:
        """
        Gets the predictions for the given prompts on the given dataset
        :param prompt_builder: Builds the prompts for the model
        :param dataset: The dataset to use with the prompts
        :param llm_manager: The LLM manager to use for predictions
        :param response_prompt_ids: The prompt id to extract from predictions
        :param tags_for_response: The tag to extract from predictions
        :return: The model predictions
        """
        dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: dataset})
        trainer = LLMTrainer(LLMTrainerState(llm_manager=self.args.hgen_llm_manager if not llm_manager else llm_manager,
                                             trainer_dataset_manager=dataset_manager,
                                             prompt_builder=prompt_builder,
                                             completion_type=LLMCompletionType.GENERATION))
        predictions = trainer.perform_prediction().predictions
        response_prompt_ids = {response_prompt_ids} if isinstance(response_prompt_ids, str) else response_prompt_ids
        if response_prompt_ids:
            predictions = [DictUtil.combine_child_dicts(p, response_prompt_ids) for p in predictions]
            if tags_for_response:
                predictions = [DictUtil.filter_dict_keys(p, keys2keep=tags_for_response) if isinstance(tags_for_response, set)
                               else p[tags_for_response] for p in predictions]
                if return_first:
                    if isinstance(predictions[0], dict):
                        predictions = [value[0] if isinstance(value, list) else value for p in predictions for key, value in p.items()]
                    else:
                        predictions = [p[0] for p in predictions]
        return predictions

    def _get_prompt_builder_for_generation(self, questionnaire: QuestionnairePrompt,
                                           base_prompt: SupportedPrompts = SupportedPrompts.HGEN_GENERATION,
                                           include_summary: bool = False) -> PromptBuilder:
        """
        Gets the prompt builder used for the generations
        :param questionnaire: The questionnaire prompt given to the model to produce the generations
        :param base_prompt: The main prompt that starts the prompt
        :param include_summary: If True, instructions the model to create a summary of the system first
        :return: The prompt builder used for the generations
        """
        questionnaire.value = self.TASK_PREFACE + questionnaire.value
        generation_step_response_manager = questionnaire.question_prompts[-1].response_manager
        generation_step_response_manager.formatter = lambda tag, val: self._format_generated_artifact_content_from_response(val)

        artifact_prompt = MultiArtifactPrompt(prompt_start="{source_type}S:",
                                              build_method=MultiArtifactPrompt.BuildMethod.NUMBERED,
                                              include_ids=False, data_type=MultiArtifactPrompt.DataType.ARTIFACT)
        artifact_prompt.format_value(source_type=self.args.source_type.upper())
        summary_prompt = Prompt("First, write a short paragraph summarizing the system described by the code.",
                                PromptResponseManager(response_tag="summary"))
        prompts = [base_prompt.value, artifact_prompt]
        if include_summary:
            prompts.append(summary_prompt)
        prompts.append(questionnaire)
        prompt_builder = PromptBuilder(prompts)
        prompt_builder.format_prompts_with_var(source_type=self.args.source_type, target_type=self.args.target_type)
        return prompt_builder

    @staticmethod
    def _convert_spaces_to_dashes(str2convert) -> str:
        """
        Converts the str to use dashes instead of spaces
        :return: The str with dashes instead of spaces
        """
        return "-".join(str2convert.split()).lower()

    @staticmethod
    def _format_generated_artifact_content_from_response(res: str) -> List[str]:
        """
        Formats the generated artifact content from the model response into a list of the artifact content
        :param res: The response from the model containing the generated artifact content
        :return: The list of the generated artifact content
        """
        return [re.sub(r'^\d+\.\s', '', content).strip() for content in res.split(NEW_LINE) if content]

    def _get_target_layer_id(self, original_dataset_complete: PromptDataset) -> str:
        """
        Gets the id of the new target layer
        :param original_dataset_complete: The dataset containing source artifacts
        :return: The id of the new target layer
        """
        layer_id = self.args.target_type
        if self.args.target_type in original_dataset_complete.artifact_df[ArtifactKeys.LAYER_ID].values:
            layer_id = f"{layer_id}_{uuid.uuid4()}"
        return layer_id

    def _get_source_datasets_for_generation(self, export_path: str = EMPTY_STRING) -> Tuple[PromptDataset, PromptDataset]:
        """
        Gets the original source datasets used for the generation
        :param export_path: The path to export checkpoints to
        :return: The original dataset and a dataset with only the source layer
        """
        original_dataset_complete = self.args.dataset_creator_for_sources.create() if self.args.dataset_for_sources is None \
            else self.args.dataset_for_sources
        self.save_dataset_checkpoint(original_dataset_complete, export_path, filename="initial_dataset_with_sources")
        source_layer_only_dataset = self._create_dataset_with_single_layer(original_dataset_complete.artifact_df,
                                                                           self.args.source_layer_id,
                                                                           original_dataset_complete.trace_dataset.trace_df
                                                                           if original_dataset_complete.trace_dataset else None)
        return original_dataset_complete, source_layer_only_dataset

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
        if len(layer_artifact_df) == 0:
            raise NameError(f"source_layer_id: {layer_id} does not match any artifacts in the dataset")
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

    @staticmethod
    def _get_path_to_generation_questionnaire_prompt(target_type: str) -> str:
        """
        Gets the path to the generation questionnaire prompts for a given target type
        :param target_type: The target type being generated
        :return: The path to the generation questionnaire prompts for a given target type
        """
        return os.path.join(GENERATION_QUESTIONNAIRE_PROMPTS_PATH, f"{target_type}.yaml")

    @staticmethod
    def _set_max_tokens(llm_manager: AbstractLLMManager) -> int:
        """
        Tries to find the optimal number of tokens to set for the model's response
        :param llm_manager: The LLM Manager being used for the clustering
        :return: The max tokens that the model was set to
        """
        model_token_limit = ModelTokenLimits.get_token_limit_for_model(llm_manager.llm_args.model)
        max_tokens = max(HierarchyGenerator.RES_TOKENS_MIN, int(model_token_limit * LLMClustering.PERC_TOKENS_FOR_RES))
        llm_manager.llm_args.set_max_tokens(max_tokens)
        return max_tokens
