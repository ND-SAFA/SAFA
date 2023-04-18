from typing import Dict, List

from openai.openai_object import OpenAIObject
from scipy.special import softmax

from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_generator import AbstractPromptGenerator
from tgen.data.prompts.classification_prompt_generator import ClassificationPromptGenerator
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.logging.logger_manager import logger
from tgen.util.open_ai_util import OpenAiUtil


class OpenAiTrainer(AbstractTrainer):
    """
    Interfaces with open-ai server to fine-tune models and make predictions
    """

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, base_model: str = "ada",
                 trainer_args: OpenAiArgs = OpenAiArgs(),
                 prompt_generator: AbstractPromptGenerator = ClassificationPromptGenerator()):
        """
        Initializes the trainer with the necessary arguments for training and prediction
        :param base_model: The name of the model
        :param trainer_args: The arguments for training and prediction calls
        :param trainer_dataset_manager: The dataset manager for training and prediction
        :param prompt_generator: In charge of generator promtps for dataset
        """
        self.base_model = base_model
        self.trainer_args = trainer_args
        self.trainer_dataset_manager = trainer_dataset_manager
        self.prompt_generator = prompt_generator
        super().__init__(trainer_dataset_manager)

    def perform_training(self) -> OpenAIObject:
        """
        Handles training of the model
        :return: The training response
        """
        train_dataset: PromptDataset = self.trainer_dataset_manager[DatasetRole.TRAIN]
        training_file_id = train_dataset.get_project_file_id()
        params = self.trainer_args.to_params(self.prompt_generator, TrainerTask.TRAIN)
        if DatasetRole.VAL in self.trainer_dataset_manager:
            val_dataset: PromptDataset = self.trainer_dataset_manager[DatasetRole.VAL]
            params["validation_file"] = val_dataset.get_project_file_id()
        res = OpenAiUtil.make_fine_tune_request(training_file=training_file_id,
                                                model=self.base_model,
                                                **params)
        logger.info(res.events[-1].message)
        return res

    @staticmethod
    def check_fine_tune_status(fine_tune_id: str) -> OpenAIObject:
        """
        Checks on the status of a fine tune job
        :param fine_tune_id: The id of the fine tune job
        :return: The response for the fine tune job
        """
        res = OpenAiUtil.retrieve_fine_tune_request(id=fine_tune_id)
        logger.info(res.events[-1].message)
        return res

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL, dataset: iDataset = None) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :param dataset: The dataset to use instead of from the dataset manager
        :return: THe prediction response
        """
        dataset = self.trainer_dataset_manager[dataset_role] if not dataset else dataset
        if isinstance(dataset, TraceDataset):
            dataset = PromptDataset(trace_dataset=dataset)
        prompt_df = dataset.to_trainer_dataset(self.prompt_generator)
        res = OpenAiUtil.make_completion_request(model=self.base_model, prompt=list(prompt_df[PromptKeys.PROMPT]),
                                                 **self.trainer_args.to_params(self.prompt_generator, TrainerTask.PREDICT))
        return self._create_classification_output(res, dataset) \
            if isinstance(self.prompt_generator, ClassificationPromptGenerator) else self._create_generation_output(res)

    def cleanup(self) -> None:
        """
        performs any necessary cleanup at the end of the job
        :return: None
        """
        pass

    @staticmethod
    def _create_generation_output(res: OpenAIObject):
        """
        Creates the output for a generation
        :param res: The response from the completion
        :return: The generation output
        """
        return TracePredictionOutput(predictions=[choice["text"].strip() for choice in res["choices"]],
                                     additional_output={"id": res["id"]})

    def _create_classification_output(self, res: OpenAIObject, dataset: PromptDataset):
        """
        Creates the output for a classification
        :param res: The response from the completion
        :param dataset: The dataset being predicted on
        :return: The classification output
        """
        scores = list(map(lambda r: self._get_score(r["logprobs"]["top_logprobs"]), res["choices"]))
        trace_dataset = dataset.trace_dataset
        output = TracePredictionOutput(predictions=scores,
                                       additional_output={"id": res["id"]})
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
        assert isinstance(self.prompt_generator,
                          ClassificationPromptGenerator), "Must provide a classification prompt generator to get prediction score"
        if len(probs) < 1:
            return 0.5
        probs = probs[0]
        v0 = probs.get(self.prompt_generator.COMPLETION_START + self.prompt_generator.pos_class, 0)
        v1 = probs.get(self.prompt_generator.COMPLETION_START + self.prompt_generator.neg_class, 0)
        prob_v = [v0, v1]
        score = softmax(prob_v)[1]
        return score
