import os
from typing import Dict

import openai
import pandas as pd

from constants import OPEN_AI_ORG, OPEN_AI_KEY
from data.creators.split_dataset_creator import SplitDatasetCreator
from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.dataframes.artifact_dataframe import ArtifactKeys
from data.dataframes.trace_dataframe import TraceKeys
from data.datasets.dataset_role import DatasetRole
from data.datasets.trace_dataset import TraceDataset
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from data.readers.structured_project_reader import StructuredProjectReader
from testres.paths.paths import TEST_OUTPUT_DIR
from train.itrainer import iTrainer
from train.open_ai.open_ai_args import OpenAIArgs
from train.open_ai.open_ai_task import OpenAITask
from train.open_ai.prompt_generator import PromptGenerator
from util.file_util import FileUtil
from util.logging.logger_manager import logger

assert OPEN_AI_ORG and OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_ORG=}'.split('=')[0]} " \
                                    f"and {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
openai.organization = OPEN_AI_ORG
openai.api_key = OPEN_AI_KEY


class OpenAITrainer(iTrainer):

    """
    Interfaces with open-ai server to fine-tune models and make predictions
    """

    def __init__(self, data_output_path: str, trainer_dataset_manager: TrainerDatasetManager, base_model: str = "ada",
                 trainer_args: OpenAIArgs = OpenAIArgs(), prompt_generator: PromptGenerator = PromptGenerator()):
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

    def perform_training(self, checkpoint: str = None) -> Dict:
        """
        Handles training of the model
        :param checkpoint: If provided, will resume training from given checkpoint
        :return: The training response
        """
        training_file_id = self.create_dataset_file_id(DatasetRole.TRAIN)
        params = self.trainer_args.to_params(OpenAITask.FINE_TUNE)
        if DatasetRole.VAL in self.trainer_dataset_manager:
            params["validation_file"] = self.create_dataset_file_id(DatasetRole.VAL)
        res = openai.FineTune.create(training_file=training_file_id,
                                     model=self.base_model,
                                     classification_positive_class=self.prompt_generator.pos_class,
                                     **params)
        logger.info(res.events[-1].message)
        return res

    @staticmethod
    def check_fine_tune_status(fine_tune_id: str) -> Dict:
        """
        Checks on the status of a fine tune job
        :param fine_tune_id: The id of the fine tune job
        :return: The response for the fine tune job
        """
        res = openai.FineTune.retrieve(fine_tune_id)
        logger.info(res.events[-1].message)
        return res

    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> Dict:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :return: THe prediction response
        """
        eval_dataset_path = self.export_prompt_dataset(dataset_role)
        res = openai.Completion.create(model=self.base_model, prompt=eval_dataset_path,
                                       **self.trainer_args.to_params(OpenAITask.PREDICT))
        return res

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
