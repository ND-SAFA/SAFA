from typing import List

from apiTests.base_test import BaseTest
from apiTests.common.request_proxy import RequestProxy
from apiTests.common.test_data import TestData
from apiTests.common.test_data_creator import TestDataCreator
from tgen.common.objects.artifact import Artifact
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.list_util import ListUtil
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestUseCase(BaseTest):
    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager):
        """
        Tests ability to summarize a project from source artifacts, generate higher level docs, and trace links
        between them.
        """
        source_artifacts = TestDataCreator.get_source_artifacts()
        source_summaries = [a[ArtifactKeys.SUMMARY] for a in source_artifacts]
        fake_summaries = ["mock_summary" for i in range(len(source_summaries))]
        self.remove_summaries(source_artifacts)

        project_summary_json = TestData.read_summary(True)
        ai_manager.mock_summarization(responses=source_summaries)
        ai_manager.mock_project_summary(project_summary_json)

        summary_response = RequestProxy.summarize(source_artifacts)
        project_summary = summary_response["summary"]
        summarized_artifacts = [EnumDict(a) for a in summary_response["artifacts"]]

        source_batches = ListUtil.batch(project_summary.strip(), 100)
        target_batches = ListUtil.batch(TestData.read_summary().strip(), 100)
        for s, t in zip(source_batches, target_batches):
            self.assertEqual(s, t)

        for e_summary, r_artifact in zip(source_summaries, summarized_artifacts):
            self.assertEqual(e_summary, r_artifact[ArtifactKeys.SUMMARY])

    @staticmethod
    def remove_summaries(artifact: List[Artifact]) -> None:
        """
        Sets summary field of artifacts to none.
        :param artifact: The artifacts to remove summaries from
        :return:
        """
        for a in artifact:
            a[ArtifactKeys.SUMMARY] = None
