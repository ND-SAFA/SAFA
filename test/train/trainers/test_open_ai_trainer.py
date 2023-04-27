from collections import namedtuple
from typing import Dict, List
from unittest import mock

from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_open_ai_responses import COMPLETION_REQUEST, FINE_TUNE_REQUEST, FINE_TUNE_RESPONSE_DICT, fake_open_ai_completion
from tgen.testres.testprojects.prompt_test_project import PromptTestProject
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.train.trainers.ai_trainer import AITrainer

Res = namedtuple("Res", ["id"])


class TestOpenAiTrainer(BaseTest):

    @mock.patch("openai.FineTune.create")
    @mock.patch("openai.File.create")
    def test_perform_training_classification(self, mock_file_create: mock.MagicMock = None,
                                             mock_fine_tune_create: mock.MagicMock = None):
        mock_file_create.return_value = Res(id="file_id")
        mock_fine_tune_create.side_effect = self.fake_fine_tune_create
        for dataset_creator in self.get_all_dataset_creators().values():
            trainer = self.get_open_ai_trainer(dataset_creator, [DatasetRole.TRAIN])
            res = trainer.perform_training()

    @mock.patch("openai.FineTune.create")
    @mock.patch("openai.File.create")
    def test_perform_training_generation(self, mock_file_create: mock.MagicMock = None, mock_fine_tune_create: mock.MagicMock = None):
        mock_file_create.return_value = Res(id="file_id")
        mock_fine_tune_create.side_effect = self.fake_fine_tune_create
        for dataset_creator in self.get_all_dataset_creators().values():
            trainer = self.get_open_ai_trainer(dataset_creator, [DatasetRole.TRAIN], prompt_creator=GenerationPromptCreator())
            res = trainer.perform_training()

    @mock.patch("openai.FineTune.create")
    @mock.patch("openai.File.create")
    def test_perform_training_with_validation(self, mock_file_create: mock.MagicMock = None,
                                              mock_fine_tune_create: mock.MagicMock = None):
        mock_file_create.return_value = Res(id="file_id")
        mock_fine_tune_create.side_effect = self.fake_fine_tune_create_classification_metrics
        for type_, dataset_creator in self.get_all_dataset_creators().items():
            trainer = self.get_open_ai_trainer(dataset_creator, [DatasetRole.TRAIN, DatasetRole.VAL])
            res = trainer.perform_training()

    @mock.patch("openai.Completion.create")
    def test_perform_prediction_classification(self, mock_completion_create: mock.MagicMock = None):
        mock_completion_create.side_effect = self.fake_completion_create
        dataset_creators = self.get_all_dataset_creators()
        dataset_creators.pop("id")
        for creator in [ClassificationPromptCreator(), GenerationPromptCreator()]:
            for type_, dataset_creator in dataset_creators.items():
                trainer = self.get_open_ai_trainer(dataset_creator, [DatasetRole.EVAL], prompt_creator=creator)
                res = trainer.perform_prediction()
                self.assertGreater(len(res.predictions), 1)
                if (type_ == "dataset" or type_ == "trace") and isinstance(trainer.trainer_args.prompt_creator,
                                                                           ClassificationPromptCreator):
                    self.assertIsNotNone(res.label_ids)
                    self.assertIsNotNone(res.prediction_entries)
                    self.assertIsNotNone(res.metrics)

    @staticmethod
    def get_all_dataset_creators() -> Dict[str, PromptDatasetCreator]:
        datasets = {"artifact": TestOpenAiTrainer.get_dataset_creator_with_artifact_df(),
                    "prompt": TestOpenAiTrainer.get_dataset_creator_with_prompt_df(),
                    "dataset": TestOpenAiTrainer.get_dataset_creator_with_trace_dataset(),
                    "id": TestOpenAiTrainer.get_dataset_creator_with_project_file_id(),
                    "trace": TestOpenAiTrainer.get_dataset_creator_as_trace_dataset_creator()}
        return datasets

    @staticmethod
    def get_dataset_creator_with_artifact_df():
        return PromptDatasetCreator(project_reader=PromptTestProject.get_artifact_project_reader())

    @staticmethod
    def get_dataset_creator_with_prompt_df():
        return PromptDatasetCreator(project_reader=PromptTestProject.get_project_reader())

    @staticmethod
    def get_dataset_creator_with_trace_dataset():
        return PromptDatasetCreator(trace_dataset_creator=PromptTestProject.get_trace_dataset_creator())

    @staticmethod
    def get_dataset_creator_with_project_file_id():
        return PromptDatasetCreator(project_file_id="project_file_id")

    @staticmethod
    def get_dataset_creator_as_trace_dataset_creator():
        return PromptTestProject.get_trace_dataset_creator()

    def fake_completion_create(self, **params):
        self.assertGreater(len(params), 0)
        for param in params:
            self.assertIn(param, COMPLETION_REQUEST)
        return fake_open_ai_completion(**params)

    def fake_fine_tune_create(self, not_classification: bool = True, **params):
        self.assertGreater(len(params), 0)
        for param in params:
            self.assertIn(param, FINE_TUNE_REQUEST)
        if not_classification:
            self.assertNotIn("compute_classification_metrics", params)
            self.assertNotIn("validation_file", params)
        return FINE_TUNE_RESPONSE_DICT

    def fake_fine_tune_create_classification_metrics(self, **params):
        self.assertIn("compute_classification_metrics", params)
        self.assertIn("validation_file", params)
        return self.fake_fine_tune_create(not_classification=False, **params)

    def get_open_ai_trainer(self, dataset_creator: AbstractDatasetCreator, roles: List[DatasetRole], **params):
        trainer_dataset_manager = TrainerDatasetManager.create_from_map({role: dataset_creator for role in roles})
        return AITrainer(trainer_dataset_manager=trainer_dataset_manager, trainer_args=OpenAiArgs(**params))
