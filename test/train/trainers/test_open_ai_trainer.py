from collections import namedtuple
from copy import deepcopy
from typing import Dict, List
from unittest import mock

from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_open_ai_responses import FINE_TUNE_REQUEST, FINE_TUNE_RESPONSE_DICT
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.testprojects.prompt_test_project import PromptTestProject

Res = namedtuple("Res", ["id"])


class TestOpenAiTrainer(BaseTest):
    FAKE_CLASSIFICATION_OUTPUT = {
        "classification": "DIRECT",
        "justification": "Something",
        "source_subsystem": "source_subsystem",
        "target_subsystem": "target_subsystem",
        "confidence": 0.6
    }

    @mock.patch("openai.FineTune.create")
    @mock.patch("openai.File.create")
    def test_perform_training_classification(self, mock_file_create: mock.MagicMock = None,
                                             mock_fine_tune_create: mock.MagicMock = None):
        mock_file_create.return_value = Res(id="file_id")
        mock_fine_tune_create.side_effect = self.fake_fine_tune_create
        prompt = BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Are these two artifacts related?")
        prompt_builder = PromptBuilder(prompts=[prompt])
        for dataset_creator in self.get_all_dataset_creators().values():
            trainer = self.get_llm_trainer(dataset_creator, [DatasetRole.TRAIN], prompt_builder=prompt_builder)
            res = trainer.perform_training()

    @mock.patch("openai.FineTune.create")
    @mock.patch("openai.File.create")
    def test_perform_training_with_validation(self, mock_file_create: mock.MagicMock = None,
                                              mock_fine_tune_create: mock.MagicMock = None):
        mock_file_create.return_value = Res(id="file_id")
        mock_fine_tune_create.side_effect = self.fake_fine_tune_create_classification_metrics
        prompt = BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Are these two artifacts related?")
        prompt_builder = PromptBuilder(prompts=[prompt])
        for type_, dataset_creator in self.get_all_dataset_creators().items():
            trainer = self.get_llm_trainer(dataset_creator, [DatasetRole.TRAIN, DatasetRole.VAL], prompt_builder=prompt_builder)
            res = trainer.perform_training()

    @mock.patch("openai.FineTune.create")
    @mock.patch("openai.File.create")
    def test_perform_training_generation(self, mock_file_create: mock.MagicMock = None, mock_fine_tune_create: mock.MagicMock = None):
        mock_file_create.return_value = Res(id="file_id")
        mock_fine_tune_create.side_effect = self.fake_fine_tune_create
        prompt = QuestionPrompt("Tell me about this artifact: ")
        prompt_builder = PromptBuilder([prompt])
        for dataset_creator in self.get_all_dataset_creators().values():
            trainer = self.get_llm_trainer(dataset_creator, [DatasetRole.TRAIN], prompt_builder=prompt_builder)
            res = trainer.perform_training()

    @mock_openai
    @mock.patch.object(LLMResponseUtil, "extract_labels")
    def test_perform_prediction_classification(self, ai_manager: TestAIManager, llm_response_mock: mock.MagicMock):
        choice_responses = [
            f"<choice>yes</choice>" for i in range(12)
        ]
        other_responses = [
            ("<choice>yes</choice>", [0.1, 0.8]) for i in range(18)
        ]
        ai_manager.mock_summarization()
        ai_manager.set_responses(choice_responses + other_responses + other_responses + ["here is details about this artifact"] * 3)
        llm_response_mock.return_value = self.FAKE_CLASSIFICATION_OUTPUT

        dataset_creators = self.get_all_dataset_creators()
        dataset_creators.pop("id")
        dataset_creators.pop("prompt")

        classification_prompt_builder, generation_prompt_builder = self.create_prompt_builders()

        for i, builder in enumerate([classification_prompt_builder, generation_prompt_builder]):
            for type_, dataset_creator in dataset_creators.items():
                builder_local = deepcopy(builder)
                if i == 0:
                    if (type_ == "dataset" or type_ == "trace"):
                        builder_local.add_prompt(MultiArtifactPrompt(data_type=MultiArtifactPrompt.DataType.TRACES))
                    else:
                        builder_local.add_prompt(ArtifactPrompt())
                trainer: LLMTrainer = self.get_llm_trainer(dataset_creator, [DatasetRole.EVAL], prompt_builder=builder_local,
                                                           completion_type=LLMCompletionType.CLASSIFICATION
                                                           if (type_ == "dataset" or type_ == "trace") and i == 0
                                                           else LLMCompletionType.GENERATION)
                res = trainer.perform_prediction()
                if (type_ == "dataset" or type_ == "trace") and i == 0:  # classification
                    self.assertIsNotNone(res.label_ids)
                    self.assertGreater(len(res.prediction_entries), 1)
                    self.assertIsNotNone(res.metrics)
                else:
                    self.assertGreaterEqual(len(res.predictions), 1)

    @staticmethod
    def create_prompt_builders():
        classification_prompt = BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Are these two artifacts related?")
        classification_prompt_builder = PromptBuilder(prompts=[classification_prompt])
        generation_prompt = QuestionPrompt("Tell me about this artifact: ")
        generation_prompt_builder = PromptBuilder([generation_prompt])
        return classification_prompt_builder, generation_prompt_builder

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
        prompt_dataset_creator = PromptDatasetCreator(project_reader=PromptTestProject.get_project_reader())
        return prompt_dataset_creator

    @staticmethod
    def get_dataset_creator_with_trace_dataset():
        return PromptDatasetCreator(trace_dataset_creator=PromptTestProject.get_trace_dataset_creator())

    @staticmethod
    def get_dataset_creator_with_project_file_id():
        return PromptDatasetCreator(project_file_id="project_file_id")

    @staticmethod
    def get_dataset_creator_as_trace_dataset_creator():
        return PromptTestProject.get_trace_dataset_creator()

    @staticmethod
    def get_llm_trainer(dataset_creator: AbstractDatasetCreator, roles: List[DatasetRole],
                        prompt_builder: PromptBuilder, **params) -> LLMTrainer:
        trainer_dataset_manager = TrainerDatasetManager.create_from_map({role: dataset_creator for role in roles})
        llm_manager = OpenAIManager(OpenAIArgs())
        return LLMTrainer(LLMTrainerState(trainer_dataset_manager=trainer_dataset_manager,
                                          prompt_builder=prompt_builder, llm_manager=llm_manager, **params))

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
