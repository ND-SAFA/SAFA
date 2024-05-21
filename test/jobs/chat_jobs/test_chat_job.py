from typing import List

from test.jobs.health_check_jobs.health_check_utils import EXPECTED_CONTEXT_IDS, assert_correct_related_artifacts, \
    get_dataset_for_context, get_chat_history
from tgen.chat.chat_node_ids import ChatNodeIDs
from tgen.chat.message_meta import MessageMeta
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.chat_jobs.chat_job import ChatJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.models.llm.abstract_llm_manager import PromptRoles, Message
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
        ai_manager.set_responses(
            [PromptUtil.create_xml(LLMNode.response_tag, "yes"), PromptUtil.create_xml(LLMNode.response_tag, "all"),
             PromptUtil.create_xml(LLMNode.response_tag, "Best pet to get"),
             self.response])
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

        ai_manager.set_responses([PromptUtil.create_xml(LLMNode.response_tag, "no"),
                                  lambda prompt: self.response(prompt, expected_context_artifacts + EXPECTED_CONTEXT_IDS,
                                                               second_response)])
        job = self._get_job(additional_chats=[MessageMeta(message=Message(content=self.RESPONSE, role=PromptRoles.ASSISTANT)),
                                              MessageMeta(message=Message(content="Do cars make the same sound as cats?",
                                                                          role=PromptRoles.USER),
                                                          artifact_ids=set(expected_context_artifacts))],
                            artifact_ids=EXPECTED_CONTEXT_IDS)
        job.run()
        self.assert_job_succeeded(job.result)

        message_meta: MessageMeta = job.result.body
        self.assertEqual(message_meta.message["content"], second_response)
        self.assertSetEqual(set(expected_context_artifacts), message_meta.artifact_ids)

    @mock_anthropic
    def test_skip_nodes(self, ai_manager: TestAIManager):
        """
        Tests that job is completed succesfully.
        """

        ai_manager.set_responses([PromptUtil.create_xml(LLMNode.response_tag, "yes"),
                                  self.response])
        job = self._get_job(nodes2skip={ChatNodeIDs.CONTEXT_TYPE, ChatNodeIDs.REWRITE_QUERY})
        job.run()
        self.assert_job_succeeded(job.result)
        self._assert_success(job, job.result)

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

    def _get_job(self, additional_chats: List[MessageMeta] = None,
                 artifact_ids: List = None, nodes2skip=None) -> AbstractJob:
        additional_chats = [] if not additional_chats else additional_chats
        return ChatJob(JobArgs(dataset=self.DATASET),
                       chat_history=get_chat_history(artifact_ids) + additional_chats,
                       nodes2skip=nodes2skip)
