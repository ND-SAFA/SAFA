import os
from typing import Dict, List

import openai
import pandas as pd
from openai.openai_object import OpenAIObject
from scipy.special import softmax

from tgen.constants import OPEN_AI_KEY, OPEN_AI_ORG
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_generator import AbstractPromptGenerator
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.train.itrainer import iTrainer
from tgen.train.metrics.metrics_manager import MetricsManager
from tgen.train.open_ai.open_ai_args import OpenAIArgs
from tgen.train.open_ai.open_ai_task import OpenAITask
from tgen.data.prompts.classification_prompt_generator import ClassificationPromptGenerator
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger

assert OPEN_AI_ORG and OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_ORG=}'.split('=')[0]} " \
                                    f"and {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
openai.organization = OPEN_AI_ORG
openai.api_key = OPEN_AI_KEY


class OpenAITrainer(iTrainer):
    """
    Interfaces with open-ai server to fine-tune models and make predictions
    """

    def __init__(self, data_output_path: str, trainer_dataset_manager: TrainerDatasetManager, base_model: str = "ada",
                 trainer_args: OpenAIArgs = OpenAIArgs(),
                 prompt_generator: AbstractPromptGenerator = AbstractPromptGenerator()):
        """
        Initializes the trainer with the necessary arguments for training and prediction
        :param base_model: The name of the model
        :param data_output_path: The path to where data files will be saved
        :param trainer_args: The arguments for training and prediction calls
        :param trainer_dataset_manager: The dataset manager for training and prediction
        :param prompt_generator: Determines the expected prompt and completion format
        """
        self.base_model = base_model
        self.data_output_path = data_output_path
        self.trainer_args = trainer_args
        self.trainer_dataset_manager = trainer_dataset_manager
        self.prompt_generator = prompt_generator
        FileUtil.create_dir_safely(self.data_output_path)

    def perform_training(self, checkpoint: str = None) -> OpenAIObject:
        """
        Handles training of the model
        :param checkpoint: If provided, will resume training from given checkpoint
        :return: The training response
        """
        training_file_id = self.create_dataset_file_id(DatasetRole.TRAIN)
        params = self.trainer_args.to_params(self.prompt_generator, OpenAITask.FINE_TUNE)
        if DatasetRole.VAL in self.trainer_dataset_manager:
            params["validation_file"] = self.create_dataset_file_id(DatasetRole.VAL)
        res = openai.FineTune.create(training_file=training_file_id,
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
        res = openai.FineTune.retrieve(fine_tune_id)
        logger.info(res.events[-1].message)
        return res

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :return: THe prediction response
        """
        prompt_df = self.convert_to_prompts_dataset(self.trainer_dataset_manager[dataset_role])
        res = openai.Completion.create(model=self.base_model, prompt=list(prompt_df[self.prompt_generator.PROMPT_KEY]),
                                       **self.trainer_args.to_params(self.prompt_generator, OpenAITask.PREDICT))
        return self._create_classification_output(res, dataset_role) \
            if isinstance(self.prompt_generator, ClassificationPromptGenerator) else self._create_generation_output(res)

    def cleanup(self) -> None:
        """
        performs any necessary cleanup at the end of the job
        :return: None
        """
        pass

    def export_prompt_dataset(self, dataset_role: DatasetRole) -> str:
        """
        Exports the prompt dataset
        :param dataset_role: Role of the dataset role to create
        :return: The path to the dataset
        """
        prompt_df = self.convert_to_prompts_dataset(self.trainer_dataset_manager[dataset_role])
        export_path = os.path.join(self.data_output_path, f"{dataset_role.value}.jsonl")
        prompt_df.to_json(export_path, orient='records', lines=True)
        return export_path

    def create_dataset_file_id(self, dataset_role: DatasetRole) -> str:
        """
        Creates a dataset file id for open ai
        :param dataset_role: Role of the dataset role to create id for
        :return: The dataset file id for open ai
        """
        dataset_file_path = self.export_prompt_dataset(dataset_role)
        res = openai.File.create(file=open(dataset_file_path), purpose=OpenAITask.FINE_TUNE.value)
        return res.id

    def convert_to_prompts_dataset(self, dataset: TraceDataset) -> pd.DataFrame:
        """
        Converts trace links in to prompt format for generation model.
        :return: A prompts based dataset.
        """
        entries = []
        for i, row in dataset.trace_df.iterrows():
            source, target = dataset.get_link_source_target_artifact(link_id=i)
            entry = self.prompt_generator.generate(source[ArtifactKeys.CONTENT], target[ArtifactKeys.CONTENT],
                                                   row[TraceKeys.LABEL.value])
            entries.append(entry)
        return pd.DataFrame(entries)

    @staticmethod
    def _create_generation_output(res: OpenAIObject):
        """
        Creates the output for a generation
        :param res: The response from the completion
        :return: The generation output
        """
        return TracePredictionOutput(predictions=[choice.text.strip() for choice in res["choices"]],
                                     additional_output={"id": res["id"]})

    def _create_classification_output(self, res: OpenAIObject, dataset_role: DatasetRole):
        """
        Creates the output for a classification
        :param res: The response from the completion
        :param dataset_role: The role of the dataset being predicted on
        :return: The classification output
        """
        scores = list(map(lambda r: self._get_score(r["logprobs"]["top_logprobs"]), res["choices"]))
        dataset = self.trainer_dataset_manager[dataset_role]
        metrics_manager = MetricsManager(trace_df=dataset.trace_df,
                                         link_ids=dataset.get_ordered_link_ids(),
                                         trace_predictions=scores)
        eval_metrics = metrics_manager.eval(self.trainer_args.metrics)
        logger.log_with_title(f"{dataset_role.name} Metrics", repr(eval_metrics))
        return TracePredictionOutput(predictions=metrics_manager.get_scores(),
                                     label_ids=metrics_manager.trace_matrix.labels,
                                     metrics=eval_metrics,
                                     prediction_entries=metrics_manager.get_trace_predictions(),
                                     additional_output={"id": res["id"]})

    def _get_score(self, probs: List[Dict]) -> float:
        """
        Gets the score from the predicted completions
        :param probs: The probabilities of each top completion
        :return: The softmax score from the predicted completions
        """
        if len(probs) < 1:
            return 0.5
        probs = probs[0]
        v0 = probs.get(self.prompt_generator.COMPLETION_START + self.prompt_generator.pos_class, 0)
        v1 = probs.get(self.prompt_generator.COMPLETION_START + self.prompt_generator.neg_class, 0)
        prob_v = [v0, v1]
        score = softmax(prob_v)[1]
        return score
