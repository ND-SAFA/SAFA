from typing import List, Dict

from test.jobs.health_check_jobs.health_check_utils import QUERY, EXPECTED_CONTEXT_IDS, assert_correct_related_artifacts, \
    get_dataset_for_context
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.chat_jobs.chat_job import ChatJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager, PromptRoles
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestChatJob(BaseJobTest):
    RESPONSE = "You should get a cat!"
    DATASET = get_dataset_for_context()

    @mock_anthropic
    def test_run_success(self, ai_manager: TestAIManager):
        """
        Tests that job is completed succesfully.
        """
        ai_manager.set_responses([self.response])
        self._test_run_success()

    @mock_anthropic
    def test_run_second_message(self, ai_manager: TestAIManager):
        """
        Tests that job is completed succesfully.
        """
        second_response = "You're welcome!"
        ai_manager.set_responses([second_response])
        job = self._get_job(additional_chats=[AbstractLLMManager.convert_prompt_to_message(prompt=self.RESPONSE,
                                                                                           role=PromptRoles.ASSISTANT),
                                              AbstractLLMManager.convert_prompt_to_message(prompt="Thank you!")])
        job.run()
        response, related_artifacts = job.result.body
        self.assertEqual(response, second_response)
        self.assertIsNone(related_artifacts)

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        response, related_artifacts = job_result.body
        self.assertEqual(response, self.RESPONSE)
        assert_correct_related_artifacts(self, related_artifacts)

    def response(self, prompt):
        for a_id in EXPECTED_CONTEXT_IDS:
            content = self.DATASET.artifact_df.get_artifact(a_id)[ArtifactKeys.CONTENT]
            self.assertIn(content, prompt)
        return self.RESPONSE

    def _get_job(self, additional_chats: List[Dict] = None) -> AbstractJob:
        additional_chats = [] if not additional_chats else additional_chats
        return ChatJob(JobArgs(dataset=self.DATASET),
                       chat_history=[AbstractLLMManager.convert_prompt_to_message(prompt=QUERY[ArtifactKeys.CONTENT])] +
                                    additional_chats)
