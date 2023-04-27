from typing import Dict, List, Union

from openai.api_resources.fine_tune import FineTune
from openai.openai_object import OpenAIObject
from scipy.special import softmax

from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.train.args.llm_args import LLMArgs
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.ai.params.openai_params import OpenAiParams
from tgen.util.ai.supported_ai_utils import SupportedLLMUtils
from tgen.util.logging.logger_manager import logger


class LLMTrainer(AbstractTrainer):
    """
    Interfaces with open-ai server to fine-tune models and make predictions
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, prompt_creator: AbstractPromptCreator,
                 trainer_args: LLMArgs = None, base_model: str = None, llm_util: SupportedLLMUtils = SupportedLLMUtils.OPENAI):
        """
        Initializes the trainer with the necessary arguments for training and prediction
        :param base_model: The name of the model
        :param trainer_args: The arguments for training and prediction calls
        :param trainer_dataset_manager: The dataset manager for training and prediction
        :param prompt_creator: Creates the prompts for trace link prediction.
        """
        if trainer_args is None:
            trainer_args = OpenAiArgs()
        if prompt_creator is None:
            prompt_creator = ClassificationPromptCreator(prompt_args=trainer_args.prompt_args)
        if base_model is None:
            base_model = trainer_args.base_model
        self.base_model = base_model
        self.trainer_dataset_manager = trainer_dataset_manager
        super().__init__(trainer_dataset_manager, trainer_args=trainer_args)
        self.summarizer = Summarizer(model_for_token_limit=self.base_model, code_or_exceeds_limit_only=False,
                                     max_tokens=trainer_args.max_tokens)
        self.prompt_creator = prompt_creator
        self.llm_util = llm_util.value

    def perform_training(self) -> FineTune:
        """
        Handles training of the model
        :return: The training response
        """
        train_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.TRAIN])
        training_file_id = train_dataset.get_project_file_id(prompt_creator=self.prompt_creator,
                                                             summarizer=self.summarizer)
        custom_params = {}
        include_classification_metrics = DatasetRole.VAL in self.trainer_dataset_manager
        params = self.trainer_args.to_params(TrainerTask.TRAIN, include_classification_metrics=include_classification_metrics,
                                             prompt_creator=self.prompt_creator)
        if include_classification_metrics:
            val_dataset: PromptDataset = self.convert_dataset_to_prompt_dataset(self.trainer_dataset_manager[DatasetRole.VAL])
            params[OpenAiParams.VALIDATION_FILE] = val_dataset.get_project_file_id(
                prompt_creator=self.prompt_creator,
                summarizer=self.summarizer)
        res = self.llm_util.make_fine_tune_request(training_file=training_file_id,
                                                   model=self.base_model,
                                                   **params)
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
        if self.trainer_args.output_dir:
            dataset.export_prompt_dataframe(prompt_df, self.trainer_args.output_dir)
        params = self.trainer_args.to_params(TrainerTask.PREDICT)
        res = self.llm_util.make_completion_request(model=self.base_model, prompt=list(prompt_df[PromptKeys.PROMPT]), **params)
        output = self._create_classification_output(res, dataset) \
            if isinstance(self.prompt_creator, ClassificationPromptCreator) else self._create_generation_output(res)
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
    def _create_generation_output(res: OpenAIObject):
        """
        Creates the output for a generation
        :param res: The response from the completion
        :return: The generation output
        """
        return TracePredictionOutput(predictions=[choice.text.strip() for choice in res.choices],
                                     additional_output={"id": res.id})

    def _create_classification_output(self, res: OpenAIObject, dataset: PromptDataset):
        """
        Creates the output for a classification
        :param res: The response from the completion
        :param dataset: The dataset being predicted on
        :return: The classification output
        """
        scores = list(map(lambda r: self._get_score(r.logprobs.top_logprobs), res.choices))
        trace_dataset = dataset.trace_dataset
        output = TracePredictionOutput(predictions=scores,
                                       additional_output={"id": res.id})
        if trace_dataset is not None:
            metrics_manager = MetricsManager(trace_df=trace_dataset.trace_df,
                                             link_ids=trace_dataset.get_ordered_link_ids(),
                                             predicted_similarities=scores)
            output.metrics = metrics_manager.eval(self.trainer_args.metrics)
            if output.metrics:
                logger.log_with_title(f"Metrics", repr(output.metrics))
            output.label_ids = metrics_manager.trace_matrix.labels
            output.prediction_entries = metrics_manager.get_trace_predictions()
        return output

    def _get_score(self, probs: List[Dict]) -> float:
        """
        Gets the score from the predicted completions
        :param probs: The probabilities of each top completion
        :return: The softmax score from the predicted completions
        """
        assert isinstance(self.prompt_creator,
                          ClassificationPromptCreator), "Must provide a classification prompt generator to get prediction score"
        if len(probs) < 1:
            return 0.5
        probs = probs[0]
        v0 = probs.get(self.prompt_creator.args.completion_prefix + self.prompt_creator.pos_class, 0)
        v1 = probs.get(self.prompt_creator.args.completion_prefix + self.prompt_creator.neg_class, 0)
        prob_v = [v0, v1]
        score = softmax(prob_v)[1]
        return score
