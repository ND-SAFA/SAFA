from typing import List

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import LayerKeys, TraceKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.llm_tools.tool_models import ExploreArtifactNeighborhood, RequestAssistance, RetrieveAdditionalInformation
from gen_common.graph.nodes.generate_node import GenerateNode
from gen_common.jobs.abstract_job import AbstractJob, JobResult
from gen_common.jobs.job_args import JobArgs
from gen_common.llm.message_meta import MessageMeta
from gen_common.util.status import Status
from gen_common_test.base.mock.decorators.chat import mock_chat_model
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.tests.base_job_test import BaseJobTest

from gen.chat.job import ChatJob
from gen_test.health.health_check_utils import get_chat_history


class TestChatJob(BaseJobTest):
    CONCEPT_LAYER_ID = "concepts"
    PET_LAYER_ID = "pets"
    FACTS_LAYER_ID = "facts"
    ARTIFACT_CONTENT = ["dogs", "cats",  # 0, 1
                        "Cat1: Michael", "Dog1: Scruffy", "Cat2: Meredith", "Dog2: Rocky",  # 2, 3, 4, 5
                        "Michael is quite fat", "Meredith bites a lot", "Rocky loves bubbles", "Scruffy has a toupee",  # 6, 7, 8, 9
                        "Cats are better than dogs"]  # 10
    ARTIFACT_IDS = [f"{i}" for i, _ in enumerate(ARTIFACT_CONTENT)]
    LAYER_IDS = [CONCEPT_LAYER_ID] * 2 + [PET_LAYER_ID] * 4 + [FACTS_LAYER_ID] * 5
    TRACES = {
        0: [3, 5, 10],
        1: [2, 4, 10],
        2: [6],
        3: [9],
        4: [7],
        5: [8],
    }
    QUESTION = "What pet should I get?"
    ANSWER = "Michael seems like the best option since cats are better than dogs and meredith bites a lot which is less preferable."
    REFERENCE_IDS = ["6", "7", "2", "10"]

    @mock_chat_model
    def test_run_with_failed_res(self, response_manager: TestResponseManager):
        response_manager.set_responses(["I don't know"])
        result = self.get_job().run()
        assert result.status == Status.SUCCESS
        message_meta = result.body
        self.assertEqual(message_meta.message["content"], ChatJob.ERROR_RESPONSE)

    @mock_chat_model
    def test_run_request_assistance(self, response_manager: TestResponseManager):
        request_assistance = RequestAssistance()
        response_manager.set_responses([request_assistance])
        result = self.get_job().run()
        assert result.status == Status.SUCCESS
        message_meta = result.body
        self.assertEqual(message_meta.message["content"], ChatJob.UNKNOWN_RESPONSE)

    @mock_chat_model
    def test_run_success(self, response_manager: TestResponseManager):
        """
        Tests that job is completed succesfully.
        """
        first_res = RetrieveAdditionalInformation(retrieval_query="best pet")
        second_res = ExploreArtifactNeighborhood(artifact_ids=1, artifact_types="pets")
        third_res = ExploreArtifactNeighborhood(artifact_ids=[2, 4])
        repeat_res = RetrieveAdditionalInformation(retrieval_query="best pet")
        final_res = GenerateNode(self.get_args()).get_agent().create_response_obj([self.ANSWER, self.REFERENCE_IDS])
        response_manager.set_responses([first_res, second_res, third_res, repeat_res, final_res])
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        message_meta: MessageMeta = job.result.body
        self.assertEqual(message_meta.message["content"], self.ANSWER)
        related_ids = message_meta.artifact_ids
        self.assertEqual(len(self.REFERENCE_IDS), len(related_ids))
        for a_id in self.REFERENCE_IDS:
            self.assertIn(a_id, related_ids)

    def construct_dataset(self):
        trace_df = TraceDataFrame([{TraceKeys.child_label(): str(child), TraceKeys.parent_label(): str(parent), TraceKeys.LABEL: 1}
                                   for parent, children in self.TRACES.items() for child in children])
        artifact_df = ArtifactDataFrame([Artifact(id=self.ARTIFACT_IDS[i], content=content,
                                                  layer_id=self.LAYER_IDS[i]) for i, content in enumerate(self.ARTIFACT_CONTENT)])
        layer_df = LayerDataFrame([{LayerKeys.SOURCE_TYPE: self.PET_LAYER_ID, LayerKeys.TARGET_TYPE: self.CONCEPT_LAYER_ID},
                                   {LayerKeys.SOURCE_TYPE: self.FACTS_LAYER_ID, LayerKeys.TARGET_TYPE: self.PET_LAYER_ID}
                                   ])
        trace_dataset = TraceDataset(artifact_df, trace_df, layer_df)
        prompt_dataset = PromptDataset(trace_dataset=trace_dataset)
        return prompt_dataset

    def get_args(self):
        args = GraphArgs(user_question=self.QUESTION, dataset=self.construct_dataset())
        return args

    def _get_job(self, additional_chats: List[MessageMeta] = None,
                 artifact_ids: List = None) -> AbstractJob:
        chat_args = self.get_args()
        additional_chats = [] if not additional_chats else additional_chats
        return ChatJob(JobArgs(dataset=chat_args.dataset),
                       chat_history=get_chat_history(artifact_ids) + additional_chats)
