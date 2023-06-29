import json
from typing import List, Union

from openai.api_resources.fine_tune import FineTune

from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.supported_prompts import CLASSIFICATION_LABEL, CLASSIFICATION_SCORES, JUSTIFICATION, RELATED_LABEL, SCORE_LABEL, \
    UNRELATED_LABEL
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import ClassificationResponse, GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.open_ai_args import OpenAIParams
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.dict_util import DictUtil
from tgen.util.llm_response_util import LLMResponseUtil
from tgen.util.logging.logger_manager import logger

DISPLAY_LABELS = ["label", "score", "justification", "source", "target"]


class LLMTrainer(AbstractTrainer):
    """
    Interfaces with open-ai server to fine-tune models and make predictions
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, prompt_creator: AbstractPromptCreator,
                 llm_manager: AbstractLLMManager, summarizer: Summarizer = None, **kwargs):
        """
        Initializes the trainer with the necessary arguments for training and prediction
        :param trainer_dataset_manager: The dataset manager for training and prediction
        :param prompt_creator: Creates the prompts for trace link prediction.
        :param summarizer: The summarizer to use for shortening artifacts over the token limit.
        :param kwargs: Ignored.
        """
        if summarizer is None:
            summarizer = Summarizer(llm_manager, model_for_token_limit=llm_manager.llm_args.model,
                                    code_or_exceeds_limit_only=False,
                                    max_tokens_for_token_limit=llm_manager.llm_args.get_max_tokens())
        super().__init__(trainer_dataset_manager, trainer_args=llm_manager.llm_args)
        self.llm_manager = llm_manager
        self.summarizer = summarizer
        self.prompt_creator = prompt_creator

    def perform_training(self, completion_type: LLMCompletionType = LLMCompletionType.CLASSIFICATION) -> FineTune:
        """
        Handles training of the model
        :return: The training response
        """
        train_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.TRAIN])
        training_file_id = train_dataset.get_project_file_id(self.llm_manager,
                                                             prompt_creator=self.prompt_creator,
                                                             summarizer=self.summarizer)
        custom_params = {}
        instructions = {}
        include_classification_metrics = DatasetRole.VAL in self.trainer_dataset_manager
        if include_classification_metrics:
            instructions["include_classification_metrics"] = True
            instructions["prompt_creator"] = self.prompt_creator
            val_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.VAL])
            custom_params[OpenAIParams.VALIDATION_FILE] = val_dataset.get_project_file_id(
                self.llm_manager,
                prompt_creator=self.prompt_creator,
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
        prompt_df = dataset.get_prompts_dataframe(summarizer=self.summarizer, prompt_creator=self.prompt_creator)
        if self.llm_manager.llm_args.output_dir:
            dataset.export_prompt_dataframe(prompt_df, self.llm_manager.llm_args.output_dir)
        task = LLMCompletionType.CLASSIFICATION if isinstance(self.prompt_creator, ClassificationPromptCreator) \
            else LLMCompletionType.GENERATION
        res = self.llm_manager.make_completion_request(completion_type=task,
                                                       prompt=list(prompt_df[PromptKeys.PROMPT]))

        if isinstance(res, ClassificationResponse):
            output = self._create_classification_output(res, dataset)
        elif isinstance(res, GenerationResponse):
            output = self._create_generation_output(res.batch_responses)
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
    def _create_generation_output(responses: List[str]):
        """
        Creates the output for a generation
        :param responses: The response from the completion.
        :return: The generation output.
        """
        return TracePredictionOutput(predictions=[r.strip() for r in responses])  #

    def _create_classification_output(self, res: ClassificationResponse, dataset: PromptDataset):
        """
        Creates the output for a classification
        :param res: The response from the completion
        :param dataset: The dataset being predicted on
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
            entry = LLMResponseUtil.extract_labels(r, {
                SCORE_LABEL: "score",
                CLASSIFICATION_LABEL: "classification",
                JUSTIFICATION: "justification",
                RELATED_LABEL: "similarity",
                UNRELATED_LABEL: "difference"
            })
            entry["classification"] = entry["classification"].upper().strip()
            entry["score"] = LLMResponseUtil.strip_non_digits_and_periods(entry["score"].lower())

            score = self.extract_score(entry)
            trace_row = trace_df.iloc[i]
            label = trace_row["label"]
            predicted_label = 1 if score >= 0.5 else 0
            correct_label = "correct" if label == predicted_label else "wrong"

            entry["source"] = trace_row["source"]
            entry["target"] = trace_row["target"]
            entry["label"] = trace_row["label"]

            self.update_classification_metrics(class2correct, correct_label, entry, label)
            entry = DictUtil.order(entry, DISPLAY_LABELS)
            scores.append(score)
            classifications.append(entry["classification"])
            prediction_entries.append(entry)

        prediction_entries = sorted(prediction_entries, key=lambda p: p["score"], reverse=True)
        output = TracePredictionOutput(prediction_entries=prediction_entries)
        if trace_dataset is not None and len(trace_dataset.trace_df) > 0:
            metrics_manager = MetricsManager(trace_df=trace_dataset.trace_df,
                                             predicted_similarities=scores)
            output.metrics = metrics_manager.eval(self.llm_manager.llm_args.metrics)
            if output.metrics:
                logger.log_with_title(f"Metrics", repr(output.metrics))
                logger.info(json.dumps(class2correct, indent=1))
            output.label_ids = metrics_manager.trace_matrix.labels

        return output

    @staticmethod
    def extract_score(entry):
        """
        Extracts the score from the classification entry response.
        :param entry: Entry containing score or classification, to extract score from.
        :return: The final score as a float.
        """
        try:
            score = float(entry["score"])
        except:
            logger.info("Processing link with missing score.")
            score = CLASSIFICATION_SCORES[entry["classification"]]
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
