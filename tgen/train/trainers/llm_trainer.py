import re
from typing import Dict, List, Union

from openai.api_resources.fine_tune import FineTune
from scipy.special import softmax

from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.supported_prompts import CLASSIFICATION_LABEL, RELATED_LABEL, RELATIONSHIP_LABEL, SCORE_LABEL, \
    SOURCE_COMPONENT_LABEL, \
    TARGET_COMPONENT_LABEL, \
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
from tgen.util.llm_response_util import LLMResponseUtil
from tgen.util.logging.logger_manager import logger
from tgen.util.uncased_dict import UncasedDict


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

    @staticmethod
    def strip_non_digits_and_periods(string):
        pattern = r'[^0-9.]'
        return re.sub(pattern, '', string)

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
        for i, r in enumerate(res.batch_responses):
            source_summary = LLMResponseUtil.parse(r, SOURCE_COMPONENT_LABEL)
            target_summary = LLMResponseUtil.parse(r, TARGET_COMPONENT_LABEL)
            related_desc = LLMResponseUtil.parse(r, RELATED_LABEL)
            unrelated_desc = LLMResponseUtil.parse(r, UNRELATED_LABEL)
            relationship_desc = LLMResponseUtil.parse(r, RELATIONSHIP_LABEL)
            classification = LLMResponseUtil.parse(r, CLASSIFICATION_LABEL).lower()
            score_str = LLMResponseUtil.parse(r, SCORE_LABEL).lower()
            score_str = LLMTrainer.strip_non_digits_and_periods(score_str)
            try:
                score = float(score_str)
            except:
                logger.info("Processing link with missing score.")
                score = 1 if classification == "yes" else 0
            entry = trace_df.iloc[i]
            scores.append(score)
            entry = {
                "source": entry["source"],
                "target": entry["target"],
                "label": entry["label"],
                "source_summary": source_summary,
                "target_summary": target_summary,
                "score": score,
                "similar": related_desc,
                "different": unrelated_desc,
                "relationship": relationship_desc,
                "classification": classification
            }
            prediction_entries.append(entry)

        output = TracePredictionOutput(predictions=scores)

        if trace_dataset is not None and len(trace_dataset.trace_df) > 0:
            metrics_manager = MetricsManager(trace_df=trace_dataset.trace_df,
                                             predicted_similarities=scores)
            output.metrics = metrics_manager.eval(self.llm_manager.llm_args.metrics)
            if output.metrics:
                logger.log_with_title(f"Metrics", repr(output.metrics))
            output.label_ids = metrics_manager.trace_matrix.labels
            output.prediction_entries = prediction_entries

        return output

    def _get_score(self, probs: Dict) -> float:
        """
        Gets the score from the predicted completions
        :param probs: The probabilities of each top completion
        :return: The softmax score from the predicted completions
        """
        assert isinstance(self.prompt_creator,
                          ClassificationPromptCreator), "Must provide a classification prompt generator to get prediction score"
        if len(probs) == 0:
            return 0.5

        probs = UncasedDict(probs)
        neg_str = self.prompt_creator.args.completion_prefix + self.prompt_creator.neg_class
        pos_str = self.prompt_creator.args.completion_prefix + self.prompt_creator.pos_class

        neg_str = neg_str.strip()
        pos_str = pos_str.strip()

        if pos_str in probs and neg_str in probs:
            v0 = probs.get(neg_str, 0)
            v1 = probs.get(pos_str, 0)
            prob_v = [v0, v1]
            score = softmax(prob_v)[1]
        elif pos_str in probs:
            score = 1
        elif neg_str in probs:
            score = 0
        else:
            score = 0.5
        return score
