import math
from collections import namedtuple
from typing import Dict, List
from unittest import mock

from gen_common.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.data.objects.artifact import Artifact
from gen_common.data.tdatasets.dataset_role import DatasetRole
from gen_common.llm.anthropic_manager import AnthropicManager
from gen_common.llm.args.anthropic_args import AnthropicArgs
from gen_common.llm.args.open_ai_args import OpenAIArgs
from gen_common.llm.llm_responses import GenerationResponse
from gen_common.llm.llm_trainer import LLMTrainer
from gen_common.llm.llm_trainer_state import LLMTrainerState
from gen_common.llm.open_ai_manager import OpenAIManager
from gen_common.llm.prompts.artifact_prompt import ArtifactPrompt
from gen_common.llm.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.prompts.question_prompt import QuestionPrompt
from gen_common.llm.response_managers.xml_response_manager import XMLResponseManager
from gen_common.util.file_util import FileUtil
from gen_common.util.prompt_util import PromptUtil
from gen_common.util.yaml_util import YamlUtil
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.base.mock.decorators.mock_anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.testprojects.prompt_test_project import PromptTestProject

Res = namedtuple("Res", ["id"])


class TestLLMTrainer(BaseTest):
    FAKE_CLASSIFICATION_OUTPUT = {
        "classification": "DIRECT",
        "justification": "Something",
        "source_subsystem": "source_subsystem",
        "target_subsystem": "target_subsystem",
        "confidence": 0.6
    }

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
                                  response_manager=XMLResponseManager(response_tag="response1"))
        response_prompt2 = Prompt("Second response:",
                                  response_manager=XMLResponseManager(response_tag="response2"))
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
                                  response_manager=XMLResponseManager(response_tag=tag))
        response_prompt2 = Prompt("Second response:",
                                  response_manager=XMLResponseManager(response_tag=tag))

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
