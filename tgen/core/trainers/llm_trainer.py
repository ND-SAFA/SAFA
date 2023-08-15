import json
from typing import Any, List, Union

from openai.api_resources.fine_tune import FineTune

from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.core.args.open_ai_args import OpenAIParams
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trainers.abstract_trainer import AbstractTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.supported_prompts.classification_prompts import CLASSIFICATION_LABEL, CLASSIFICATION_SCORES, CURRENT_LABELS, \
    REVERSE_CATEGORIES
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.metrics.metrics_manager import MetricsManager
from tgen.models.llm.llm_responses import ClassificationResponse, GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.state.state_manager import StateManager


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
        self.initial_state = initial_state
        self.state_manager = StateManager(self.initial_state)

    def perform_training(self, completion_type: LLMCompletionType = LLMCompletionType.CLASSIFICATION) -> FineTune:
        """
        Handles training of the model
        :return: The training response
        """
        train_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.TRAIN])
        training_file_id = train_dataset.get_project_file_id(self.llm_manager,
                                                             prompt_builder=self.prompt_builder,
                                                             summarizer=self.summarizer)
        custom_params = {}
        instructions = {}
        include_classification_metrics = DatasetRole.VAL in self.trainer_dataset_manager
        if include_classification_metrics:
            instructions["include_classification_metrics"] = True
            instructions["prompt_builder"] = self.prompt_builder
            val_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.VAL])
            custom_params[OpenAIParams.VALIDATION_FILE] = val_dataset.get_project_file_id(
                self.llm_manager,
                prompt_builder=self.prompt_builder,
                summarizer=self.summarizer)

        res = self.llm_manager.make_fine_tune_request(completion_type=completion_type, training_file=training_file_id,
                                                      instructions=instructions, **custom_params)
        logger.info(res.events[-1].message)
        return res

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL, dataset: iDataset = None) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :param dataset: The dataset to use instead of from the dataset manager
        :return: THe prediction response
        """
        dataset: PromptDataset = self.trainer_dataset_manager[dataset_role] if not dataset else dataset
        dataset = self.convert_dataset_to_prompt_dataset(dataset)
        prompt_df = dataset.get_prompt_dataframe(summarizer=self.summarizer,
                                                 prompt_builder=self.prompt_builder,
                                                 prompt_args=self.llm_manager.prompt_args)
        if self.llm_manager.llm_args.output_dir:
            dataset.export_prompt_dataframe(prompt_df, self.llm_manager.llm_args.output_dir)
        first_prompt = prompt_df[PromptKeys.PROMPT][0]
        logger.debug(first_prompt)

        res = self.llm_manager.make_completion_request(completion_type=self.completion_type,
                                                       prompt=list(prompt_df[PromptKeys.PROMPT]))
        if isinstance(res, ClassificationResponse):
            output = self._create_classification_output(res, dataset, self.prompt_builder)
        elif isinstance(res, GenerationResponse):
            output = self._create_generation_output(res.batch_responses, self.prompt_builder)
        else:
            raise NotImplementedError(f"Unable to translate response to task: {type(res)}")
        return output

    def cleanup(self) -> None:
        """
        performs any necessary cleanup at the end of the job
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
    def _create_generation_output(responses: List[str], prompt_builder: PromptBuilder) -> TracePredictionOutput:
        """
        Creates the output for a generation
        :param responses: The response from the completion.
        :param prompt_builder: The builder responsible for building the prompts
        :return: The generation output.
        """
        return TracePredictionOutput(predictions=[prompt_builder.parse_responses(r) for r in responses])  #

    def _create_classification_output(self, res: ClassificationResponse, dataset: PromptDataset, prompt_builder: PromptBuilder):
        """
        Creates the output for a classification
        :param res: The response from the completion
        :param dataset: The dataset being predicted on
        :param prompt_builder: The builder responsible for building the prompts
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
        try:
            return self.state_manager.get(item)
        except AttributeError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
