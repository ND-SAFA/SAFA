import json
import os.path
from typing import Any, List, Union, Dict

from openai.api_resources.fine_tune import FineTune

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.common.logging.logger_manager import logger
from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.yaml_util import YamlUtil
from tgen.core.args.open_ai_args import OpenAIParams
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trainers.abstract_trainer import AbstractTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import StructuredKeys, TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.metrics.metrics_manager import MetricsManager
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import ClassificationResponse, GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.classification_prompts import CLASSIFICATION_LABEL, CLASSIFICATION_SCORES, CURRENT_LABELS, \
    REVERSE_CATEGORIES


class LLMTrainer(AbstractTrainer):
    """
    Interfaces with open-ai server to fine-tune models and make predictions
    """

    def __init__(self, initial_state: LLMTrainerState):
        """
        Initializes the trainer with the necessary arguments for training and prediction
        :param initial_state: The current state of the trainer to use
        """
        super().__init__(initial_state.trainer_dataset_manager, trainer_args=initial_state.llm_manager.llm_args)
        self.state = initial_state

    def perform_training(self, completion_type: LLMCompletionType = LLMCompletionType.CLASSIFICATION) -> FineTune:
        """
        Handles training of the model
        :param completion_type: The type of completion task being performed.
        :return: The training response
        """
        train_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.TRAIN])
        training_file_id = train_dataset.get_project_file_id(self.llm_manager,
                                                             prompt_builder=self.prompt_builders)
        custom_params = {}
        instructions = {}
        include_classification_metrics = DatasetRole.VAL in self.trainer_dataset_manager
        if include_classification_metrics:
            instructions["include_classification_metrics"] = True
            instructions["prompt_builder"] = self.prompt_builders
            val_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.VAL])
            custom_params[OpenAIParams.VALIDATION_FILE] = val_dataset.get_project_file_id(
                self.llm_manager,
                prompt_builder=self.prompt_builders)

        res = self.llm_manager.make_fine_tune_request(completion_type=completion_type, training_file=training_file_id,
                                                      instructions=instructions, **custom_params)
        logger.info(res.events[-1].message)
        return res

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL,
                           dataset: iDataset = None, prompts: List[str] = None,
                           save_and_load_path: str = EMPTY_STRING) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :param dataset: The dataset to use instead of from the dataset manager
        :param prompts: The list of prompts to use instead of making from the dataset
        :param save_and_load_path: The path to load or save response
        :return: THe prediction response
        """
        assert not save_and_load_path or save_and_load_path.endswith(FileUtil.YAML_EXT), "Response must be saved to yaml file."

        dataset: PromptDataset = self.trainer_dataset_manager[dataset_role] if not dataset else dataset
        dataset = self.convert_dataset_to_prompt_dataset(dataset)
        prompts = self._get_prompts_for_prediction(dataset) if not prompts else prompts
        if os.path.exists(save_and_load_path):
            logger.info(f"IMPORTANT!!! Loading previous LLM responses from {save_and_load_path}")
            res = YamlUtil.read(save_and_load_path)
        else:
            res = self.llm_manager.make_completion_request(completion_type=self.completion_type,
                                                           prompt=prompts)
            if save_and_load_path:
                logger.info(f"Saved LLM responses to {save_and_load_path}")
                FileUtil.create_dir_safely(save_and_load_path)
                YamlUtil.write(res, save_and_load_path)
        batch_responses = res.batch_responses if isinstance(res, GenerationResponse) else [r.text for r in res.batch_responses]
        debugging = [p + NEW_LINE + r for p, r in zip(prompts, batch_responses)]
        prompt_builder_map = {prompt_builder.id: prompt_builder
                              for prompt_builder in (self.prompt_builders
                                                     if isinstance(self.prompt_builders, list) else [self.prompt_builders])}
        prompt_builder_ids = dataset.get_prompt_dataframe()[PromptKeys.PROMPT_BUILDER_ID]
        if isinstance(res, ClassificationResponse):
            output = self._create_classification_output(res, dataset, prompt_builder_map)
        elif isinstance(res, GenerationResponse):
            output = self._create_generation_output(res.batch_responses, prompt_builder_map, prompt_builder_ids)
        else:
            raise NotImplementedError(f"Unable to translate response to task: {type(res)}")
        return output

    def _get_prompts_for_prediction(self, dataset: PromptDataset) -> List[str]:
        """
        Gets the prompts used for the prediction
        :param dataset: The dataset to use when creating the prompts
        :return: The prompts and the prompt dataframe
        """

        prompt_df = dataset.get_prompt_dataframe(prompt_builders=self.prompt_builders,
                                                 prompt_args=self.llm_manager.prompt_args)
        prompts = list(prompt_df[PromptKeys.PROMPT])
        first_prompt = prompts[0]
        logger.debug(first_prompt)
        return prompts

    @staticmethod
    def predict_from_prompts(llm_manager: AbstractLLMManager,
                             prompt_builder: PromptBuilder,
                             prompts: List[Prompt] = None,
                             save_and_load_path: str = EMPTY_STRING, **prompt_kwargs) -> TracePredictionOutput:
        """
        Makes generation predictions from a list of prompts
        :param llm_manager: The llm manager to use for predictions
        :param prompt_builder: The prompt builder to parse the response (or additionally create prompts)
        :param prompts: The list of prompts to use unless built from prompt_builder
        :param save_and_load_path: Path used to load or save predictions
        :param prompt_kwargs: Additional arguments used when building prompts (optionally)
        :return: The output from the predictions
        """
        if not prompts:
            prompts = [prompt_builder.build(llm_manager.prompt_args, **prompt_kwargs)[PromptKeys.PROMPT]]
        prompt_df = PromptDataFrame({PromptKeys.PROMPT: prompts,
                                     PromptKeys.COMPLETION: [EMPTY_STRING for _ in prompts],
                                     PromptKeys.PROMPT_BUILDER_ID: [prompt_builder.id for _ in prompts]})
        dataset = PromptDataset(prompt_df=prompt_df)
        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: dataset})
        initial_state = LLMTrainerState(llm_manager=llm_manager, prompt_builders=prompt_builder,
                                        trainer_dataset_manager=trainer_dataset_manager)
        trainer = LLMTrainer(initial_state)
        return trainer.perform_prediction(save_and_load_path=save_and_load_path, prompts=list(prompt_df[PromptKeys.PROMPT]))

    def cleanup(self) -> None:
        """
        Performs any necessary cleanup at the end of the job
        :return: None
        """
        pass

    @staticmethod
    def convert_dataset_to_prompt_dataset(dataset: Union[PromptDataset, TraceDataset]) -> PromptDataset:
        """
        If the dataset is not a prompt dataset, it is converted to one
        :param dataset: The original dataset
        :return: The dataset a a prompt dataset
        """
        if not isinstance(dataset, PromptDataset):
            dataset = PromptDataset(trace_dataset=dataset)
        return dataset

    @staticmethod
    def _create_generation_output(responses: List[str], prompt_builder_map: Dict[str, PromptBuilder],
                                  prompt_builder_ids: List[str]) -> TracePredictionOutput:
        """
        Creates the output for a generation
        :param responses: The response from the completion.
        :param prompt_builder_map: Map of id to the builder for each prompt builder responsible for building the prompts
        :param prompt_builder_ids: List of ids for prompt builders corresponding to the order of responses
        :return: The generation output.
        """
        return TracePredictionOutput(predictions=[prompt_builder_map[p_id].parse_responses(r)
                                                  for r, p_id in zip(responses, prompt_builder_ids)],
                                     original_response=responses)  #

    def _create_classification_output(self, res: ClassificationResponse, dataset: PromptDataset,
                                      prompt_builder_map: Dict[str, PromptBuilder]):
        """
        Creates the output for a classification
        :param res: The response from the completion
        :param dataset: The dataset being predicted on
        :param prompt_builder_map: Map of id to the builder for each prompt builder responsible for building the prompts
        :return: The classification output
        """
        trace_dataset = dataset.trace_dataset
        trace_df = trace_dataset.trace_df
        prediction_entries = []

        scores = []
        classifications = []
        class2correct = {}
        for i, classification_item in enumerate(res.batch_responses):
            r = classification_item.text
            entry = LLMResponseUtil.extract_labels(r, {label: label for label in CURRENT_LABELS})
            entry[CLASSIFICATION_LABEL] = entry[CLASSIFICATION_LABEL].upper().strip()

            score = self.extract_score(entry)
            trace_row = trace_df.iloc[i]
            label = trace_row[TraceKeys.LABEL.value]
            predicted_label = 1 if score >= 0.5 else 0
            correct_label = "correct" if label == predicted_label else "wrong"

            entry[StructuredKeys.SCORE] = score
            entry[TraceKeys.SOURCE.value] = trace_row[TraceKeys.SOURCE.value]
            entry[TraceKeys.TARGET.value] = trace_row[TraceKeys.TARGET.value]
            entry[TraceKeys.LABEL.value] = trace_row[TraceKeys.LABEL.value]

            self.update_classification_metrics(class2correct, correct_label, entry, label)
            scores.append(score)
            classifications.append(entry["classification"])
            prediction_entries.append(entry)

        prediction_entries = sorted(prediction_entries, key=lambda p: p[TraceKeys.SCORE.value], reverse=True)
        output = TracePredictionOutput(prediction_entries=prediction_entries)
        if trace_dataset is not None and len(trace_dataset.trace_df[TraceKeys.LABEL].unique()) == 2:
            metrics_manager = MetricsManager(trace_df=trace_dataset.trace_df,
                                             predicted_similarities=scores)
            output.metrics = metrics_manager.eval(self.llm_manager.llm_args.metrics)
            if output.metrics:
                logger.log_with_title("Candidate Metrics", repr(output.metrics))
                logger.log_with_title("Class Counts", json.dumps(class2correct))
            output.label_ids = metrics_manager.trace_matrix.labels

        return output

    @staticmethod
    def extract_score(entry):
        """
        Extracts the score from the classification entry response.
        :param entry: Entry containing score or classification, to extract score from.
        :return: The final score as a float.
        """
        classification = entry["classification"]
        lower_bound, upper_bound = CLASSIFICATION_SCORES[classification]
        score_range = upper_bound - lower_bound
        try:
            confidence = float(entry["confidence"])
            if classification in REVERSE_CATEGORIES:
                score = upper_bound - (confidence * score_range)
            else:
                score = (confidence * score_range) + lower_bound
        except:
            score = lower_bound
            logger.info("Processing link with missing score.")

        return score

    @staticmethod
    def update_classification_metrics(class2correct, correct_label, entry, label) -> None:
        """
        Updates the classification metrics on the categories of traces.
        :param class2correct: The current metrics on the classes.
        :param correct_label: The correct label of the entry.
        :param entry: The
        :param label:
        :return:
        """
        classification = entry["classification"]
        if classification not in class2correct:
            class2correct[classification] = {c: 0 for c in [0, 1]}
        class2correct[classification][label] += 1

    def __getattr__(self, item: str) -> Any:
        """
        Gets an item from its state since it does not exist in trainer
        :param item: The name of the item to get
        :return: The item
        """
        if not item.startswith("__"):
            try:
                return getattr(self.state, item)
            except Exception as e:
                pass
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {item}")
