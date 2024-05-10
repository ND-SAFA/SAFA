from typing import List

from test.jobs.health_check_jobs.health_check_utils import QUERY, EXPECTED_CONTEXT_IDS, assert_correct_related_artifacts, \
    get_dataset_for_context
from tgen.chat.message_meta import MessageMeta
from tgen.common.util.status import Status
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.chat_jobs.chat_job import ChatJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager, PromptRoles, Message
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
        second_response = "No, cars go vroom and cats go meow."
        vroom_artifact = [a_id for a_id, artifact in self.DATASET.artifact_df.itertuples()
                          if "vroom" in artifact[ArtifactKeys.CONTENT]][0]
        expected_context_artifacts = [vroom_artifact]
        ai_manager.set_responses([lambda prompt: self.response(prompt, expected_context_artifacts + EXPECTED_CONTEXT_IDS,
                                                               second_response)])
        job = self._get_job(additional_chats=[MessageMeta(message=Message(content=self.RESPONSE, role=PromptRoles.ASSISTANT)),
                                              MessageMeta(message=Message(content="Do cats make the same sound as cars?",
                                                                          role=PromptRoles.USER),
                                                          artifact_ids=expected_context_artifacts)],
                            artifact_ids=EXPECTED_CONTEXT_IDS)
        job.run()
        assert job.result.status == Status.SUCCESS, "Job failed"
        message_meta: MessageMeta = job.result.body
        self.assertEqual(message_meta.message["content"], second_response)
        self.assertListEqual(expected_context_artifacts, message_meta.artifact_ids)

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        message_meta: MessageMeta = job.result.body
        self.assertEqual(message_meta.message["content"], self.RESPONSE)
        assert_correct_related_artifacts(self, message_meta.artifact_ids)

    def response(self, prompt, expected_context_ids=EXPECTED_CONTEXT_IDS, response=RESPONSE):
        user_prompt, system_prompt = prompt

        for a_id in expected_context_ids:
            content = self.DATASET.artifact_df.get_artifact(a_id)[ArtifactKeys.CONTENT]
            self.assertIn(content, system_prompt)
        return response

    def _get_job(self, additional_chats: List[MessageMeta] = None, artifact_ids: List = None) -> AbstractJob:
        additional_chats = [] if not additional_chats else additional_chats
        artifact_ids = [] if not artifact_ids else artifact_ids
        return ChatJob(JobArgs(dataset=self.DATASET),
                       chat_history=[MessageMeta(
                           message=AbstractLLMManager.convert_prompt_to_message(prompt=QUERY[ArtifactKeys.CONTENT]),
                           artifact_ids=artifact_ids)] +
                                    additional_chats)
