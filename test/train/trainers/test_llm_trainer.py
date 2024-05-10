import math
from collections import namedtuple
from copy import deepcopy
from typing import Dict, List
from unittest import mock

from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.util.yaml_util import YamlUtil
from tgen.core.args.anthropic_args import AnthropicArgs
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_open_ai_responses import FINE_TUNE_REQUEST, FINE_TUNE_RESPONSE_DICT
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.testprojects.prompt_test_project import PromptTestProject

Res = namedtuple("Res", ["id"])


class TestLLMTrainer(BaseTest):
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
            trainer = self.get_llm_trainer(dataset_creator, [DatasetRole.TRAIN], prompt_builder=prompt_builder,
                                           use_anthropic=False)
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
            trainer = self.get_llm_trainer(dataset_creator, [DatasetRole.TRAIN, DatasetRole.VAL], prompt_builder=prompt_builder,
                                           use_anthropic=False)
            res = trainer.perform_training()

    @mock.patch("openai.FineTune.create")
    @mock.patch("openai.File.create")
    def test_perform_training_generation(self, mock_file_create: mock.MagicMock = None, mock_fine_tune_create: mock.MagicMock = None):
        mock_file_create.return_value = Res(id="file_id")
        mock_fine_tune_create.side_effect = self.fake_fine_tune_create
        prompt = QuestionPrompt("Tell me about this artifact: ")
        prompt_builder = PromptBuilder([prompt])
        for dataset_creator in self.get_all_dataset_creators().values():
            trainer = self.get_llm_trainer(dataset_creator, [DatasetRole.TRAIN], prompt_builder=prompt_builder,
                                           use_anthropic=False)
            res = trainer.perform_training()

    @mock.patch.object(FileUtil, "safely_check_path_exists", return_value=True)
    @mock.patch.object(YamlUtil, "read")
    @mock_anthropic
    def test_perform_prediction_reloaded(self, test_ai_manager: TestAIManager, read_mock: mock.MagicMock,
                                         file_exists_mock: mock.MagicMock):

        prompt = ArtifactPrompt("Tell me about this artifact: ")
        prompt_builder = PromptBuilder([prompt])
        dataset_creator = TestLLMTrainer.get_dataset_creator_with_artifact_df()
        trainer = self.get_llm_trainer(dataset_creator, [DatasetRole.EVAL], prompt_builder=prompt_builder)

        n_prompts = len(dataset_creator.create().artifact_df)
        n_good_res = 5
        n_bad_res = n_prompts - n_good_res
        test_ai_manager.set_responses(["res" for i in range(n_bad_res)])

        good_res = ['res' for _ in range(n_good_res)]
        bad_res = [Exception('fake exception') for _ in range(n_bad_res)]
        read_mock.return_value = GenerationResponse(batch_responses=good_res + bad_res)

        res = trainer.perform_prediction(raise_exception=False)
        self.assertEqual(len(res.original_response), n_prompts)
        self.assertListEqual(good_res[:1] * n_prompts, res.original_response)

    @mock_anthropic
    def test_perform_prediction_multiple_prompt_builders(self, test_ai_manager: TestAIManager):

        artifact_prompt = ArtifactPrompt("Tell me about this artifact: ")
        response_prompt1 = Prompt("First response:",
                                  response_manager=PromptResponseManager(response_tag="response1"))
        response_prompt2 = Prompt("Second response:",
                                  response_manager=PromptResponseManager(response_tag="response2"))
        prompt_ids = [response_prompt1.args.prompt_id, response_prompt2.args.prompt_id]
        prompt_builder1 = PromptBuilder([artifact_prompt, response_prompt1])
        prompt_builder2 = PromptBuilder([artifact_prompt, response_prompt2])
        dataset_creator = TestLLMTrainer.get_dataset_creator_with_artifact_df()
        trainer = self.get_llm_trainer(dataset_creator, [DatasetRole.EVAL], prompt_builder=[prompt_builder1, prompt_builder2])
        prompts = trainer._create_prompts_for_prediction(dataset_creator.create(), [prompt_builder1, prompt_builder2])[
            PromptKeys.PROMPT]

        n_prompts = len(dataset_creator.create().artifact_df)
        responses1 = [PromptUtil.create_xml("response1", "Here is my first response.") for _ in range(n_prompts)]
        responses2 = [PromptUtil.create_xml("response2", "Here is my second response.") for _ in range(n_prompts)]
        test_ai_manager.set_responses(responses1 + responses2)

        res = trainer.perform_prediction()
        predictions = res.predictions
        for i in range(len(predictions)):
            response_num = math.floor(i / n_prompts)
            tag = f"response{response_num + 1}"
            prompt_response = predictions[i][prompt_ids[response_num]]
            self.assertIn(tag, prompts[i])
            self.assertIn(tag, prompt_response)

    @mock_anthropic
    def test_predict_from_prompts(self, test_ai_manager: TestAIManager):
        artifact_content = "system_prompt_artifact"
        response = "response"
        tag = "response"
        system_prompt_identifier = "First"
        n_responses = 4
        responses = iter([response + str(i) for i in range(n_responses)])

        test_ai_manager.set_responses([lambda prompt: self.assert_message_prompt(prompt, artifact_content, next(responses),
                                                                                 tag, system_prompt_identifier)
                                       for _ in range(n_responses)])

        artifact_prompt1 = ArtifactPrompt("Context artifacts: ",
                                          prompt_args=PromptArgs(system_prompt=True))
        response_prompt1 = Prompt(f"{system_prompt_identifier} response:",
                                  response_manager=PromptResponseManager(response_tag=tag))
        response_prompt2 = Prompt("Second response:",
                                  response_manager=PromptResponseManager(response_tag=tag))

        artifact_prompt2 = ArtifactPrompt("Message artifact: ",
                                          prompt_args=PromptArgs(system_prompt=False))

        prompt_builder1 = PromptBuilder([artifact_prompt1, response_prompt1])
        prompt_builder2 = PromptBuilder([artifact_prompt2, response_prompt2])
        artifact = Artifact(id="id1", content=artifact_content, layer_id="layer_id")

        llm_trainer = AnthropicManager()

        res = LLMTrainer.predict_from_prompts(llm_trainer, prompt_builder1, artifact=artifact)
        self.assertEqual(res.predictions[0][response_prompt1.args.prompt_id][response_prompt1.get_all_response_tags()[0]][0],
                         response + str(0))

        prompt1_dict = prompt_builder1.build(llm_trainer.prompt_args, artifact=artifact)
        prompt2_dict = prompt_builder2.build(llm_trainer.prompt_args, artifact=artifact)
        res = LLMTrainer.predict_from_prompts(llm_trainer, prompt_builder1, message_prompts=[p[PromptKeys.PROMPT]
                                                                                             for p in [prompt1_dict, prompt2_dict]],
                                              system_prompts=[p[PromptKeys.SYSTEM]
                                                              for p in [prompt1_dict, prompt2_dict]]
                                              )
        for i, pred in enumerate(res.predictions):
            self.assertEqual(pred[response_prompt1.args.prompt_id][response_prompt1.get_all_response_tags()[0]][0],
                             response + str(i + 1))

        res = LLMTrainer.predict_from_prompts(llm_trainer, prompt_builder1, message_prompts=[prompt2_dict[PromptKeys.PROMPT]],
                                              system_prompts=None)
        self.assertEqual(res.predictions[0][response_prompt1.args.prompt_id][response_prompt1.get_all_response_tags()[0]][0],
                         response + str(3))

    def assert_message_prompt(self, prompt: str, expected_system_prompt: str, response: str, xml_tag: str,
                              system_prompt_identifier):
        user_prompt, system_prompt = prompt if isinstance(prompt, tuple) else (prompt, None)
        expected_in_prompt: bool = system_prompt_identifier not in user_prompt
        if expected_in_prompt:
            self.assertIn(expected_system_prompt, user_prompt)
        else:
            self.assertNotIn(expected_system_prompt, user_prompt)
        return PromptUtil.create_xml(xml_tag, response)

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
                                                           else LLMCompletionType.GENERATION,
                                                           use_anthropic=False)
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
        datasets = {"artifact": TestLLMTrainer.get_dataset_creator_with_artifact_df(),
                    "prompt": TestLLMTrainer.get_dataset_creator_with_prompt_df(),
                    "dataset": TestLLMTrainer.get_dataset_creator_with_trace_dataset(),
                    "id": TestLLMTrainer.get_dataset_creator_with_project_file_id(),
                    "trace": TestLLMTrainer.get_dataset_creator_as_trace_dataset_creator()}
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
                        prompt_builder: PromptBuilder, use_anthropic: bool = True, **params) -> LLMTrainer:
        trainer_dataset_manager = TrainerDatasetManager.create_from_map({role: dataset_creator for role in roles})
        if use_anthropic:
            llm_manager = AnthropicManager(AnthropicArgs())
        else:
            llm_manager = OpenAIManager(OpenAIArgs())
        return LLMTrainer(LLMTrainerState(trainer_dataset_manager=trainer_dataset_manager,
                                          prompt_builders=prompt_builder, llm_manager=llm_manager, **params))

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
