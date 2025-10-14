import re
from string import ascii_lowercase

from bs4 import BeautifulSoup

from gen_common.constants.summary_constants import SPECIAL_TAGS_ITEMS
from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.summarize.summarizer import Summarizer
from gen_common.summarize.summarizer_args import SummarizerArgs
from gen_common.summarize.summarizer_state import SummarizerState
from gen_common.summarize.summary import Summary
from gen_common.util.dataframe_util import DataFrameUtil
from gen_common.util.str_util import StrUtil
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.responses.summary import PROJECT_SUMMARY_RESPONSES, SECTION_TAG_TO_TILE, TEST_PROJECT_SUMMARY, create
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.testprojects.safa_test_project import SafaTestProject


class TestSummarizer(BaseTest):
    N_ARTIFACTS = len(SafaTestProject.get_source_artifacts() + SafaTestProject.get_target_artifacts())
    N_PROJECT_SECTIONS = len(PROJECT_SUMMARY_RESPONSES)

    """
    NO RE-SUMMARIZATIONS SO EVERYTHING IS SUMMARIZED AT MAX ONCE
    """

    @mock_anthropic
    def test_with_no_resummarize_and_no_summaries(self, ai_manager: TestAIManager):
        args = SummarizerArgs(do_resummarize_artifacts=False)

        ai_manager.set_responses(PROJECT_SUMMARY_RESPONSES)
        summarizer = self.get_summarizer(args)
        n_expected_summarizations = self.N_ARTIFACTS + self.N_PROJECT_SECTIONS
        self._assert_summarization(summarizer, n_expected_summarizations, ai_manager)

    @mock_anthropic
    def test_with_no_resummarize_with_project_summary(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=False)

        summarizer = self.get_summarizer(args, with_project_summary=True)
        self._assert_summarization(summarizer, self.N_ARTIFACTS, ai_manager)

    @mock_anthropic
    def test_with_no_resummarize_with_artifact_summaries(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=False)

        ai_manager.set_responses(PROJECT_SUMMARY_RESPONSES)
        summarizer = self.get_summarizer(args, with_artifact_summaries=True)
        self._assert_summarization(summarizer, self.N_PROJECT_SECTIONS, ai_manager)

    @mock_anthropic
    def test_with_no_resummarize_with_all_summarized(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=False)

        summarizer = self.get_summarizer(args, with_artifact_summaries=True, with_project_summary=True)
        self._assert_summarization(summarizer, 0, ai_manager)

    """
    RE_SUMMARIZE ARTIFACTS SO ARTIFACTS ARE ALWAYS SUMMARIZED AT LEAST ONCE, PROJECT SUMMARIZED NO MORE THAN ONCE
    """

    @mock_anthropic
    def test_with_resummarize_artifacts_and_no_summaries(self, ai_manager: TestAIManager):
        args = SummarizerArgs(do_resummarize_artifacts=True)

        ai_manager.set_responses(PROJECT_SUMMARY_RESPONSES)
        summarizer = self.get_summarizer(args)
        n_expected_summarizations = 2 * self.N_ARTIFACTS + self.N_PROJECT_SECTIONS
        self._assert_summarization(summarizer, n_expected_summarizations, ai_manager)

    @mock_anthropic
    def test_with_resummarize_artifacts_with_project_summary(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=True)

        summarizer = self.get_summarizer(args, with_project_summary=True)
        self._assert_summarization(summarizer, self.N_ARTIFACTS, ai_manager)

    @mock_anthropic
    def test_with_resummarize_artifacts_with_artifact_summaries(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=True)

        ai_manager.set_responses(PROJECT_SUMMARY_RESPONSES)
        summarizer = self.get_summarizer(args, with_artifact_summaries=True)
        self._assert_summarization(summarizer, self.N_PROJECT_SECTIONS + self.N_ARTIFACTS, ai_manager)

    @mock_anthropic
    def test_with_resummarize_artifacts_with_all_summarized(self, ai_manager):
        args = SummarizerArgs(do_resummarize_artifacts=True)

        summarizer = self.get_summarizer(args, with_artifact_summaries=True, with_project_summary=True)
        self._assert_summarization(summarizer, self.N_ARTIFACTS, ai_manager)

    @mock_anthropic
    def test_with_large_project(self, ai_manager: TestAIManager):
        def assert_summary(summary, n_expected_ids):
            n_ids = len(find_ids(summary.to_string())) / (n_project_summary_sections - 2)
            self.assertEqual(n_ids, n_expected_ids)

        def find_ids(body):
            pattern = r'\[[a-zA-Z]\]'
            matches = re.findall(pattern, body)
            matches = [StrUtil.remove_substrings(match, ["[", "]"]) for match in matches]
            return matches

        def project_summary_response(prompt, **kwargs):
            artifact_ids = [tag.text for tag in BeautifulSoup(prompt, features="lxml").findAll("id")]
            if not artifact_ids:
                artifact_ids = set(find_ids(prompt))
            artifact_ids = EMPTY_STRING.join([f"[{id_}]" for id_ in artifact_ids])
            pattern = re.compile(r'<[^>]+>')
            tags = [t for t in pattern.findall(prompt) if not any([x in t for x in {"id", "body", "artifact", "versions"}])]
            tag = tags[3]
            tag = StrUtil.remove_substrings(tag, ["</", ">"])
            section_title = SECTION_TAG_TO_TILE.get(tag)
            body_prefix = artifact_ids if section_title not in SPECIAL_TAGS_ITEMS else None
            return create(title=section_title, body_prefix=body_prefix)

        n_clusters = 3
        ai_manager.mock_summarization()
        summarizer = self.get_summarizer(SummarizerArgs())
        ids = list(ascii_lowercase)
        artifact_df = ArtifactDataFrame({
            ArtifactKeys.ID: ids,
            ArtifactKeys.CONTENT: [c * 10000 for c in ids],
            ArtifactKeys.LAYER_ID: ["Large Layer"] * len(ids)
        })
        summarizer.dataset.update_artifact_df(artifact_df)
        n_project_summary_sections = len(summarizer.args.project_summary_sections)

        n_cluster_prompts = n_project_summary_sections * (n_clusters + 1)  # prompts for clusters + combination
        project_summary_responses = [project_summary_response for _ in range(n_cluster_prompts)]  # 1 for combining
        ai_manager.set_responses(project_summary_responses)
        summarizer.summarize()
        state: SummarizerState = summarizer.state
        clustered_artifacts = {a_id for c in state.batch_id_to_artifacts.values() for a_id in c}
        self.assertGreater(len(state.batch_id_to_artifacts), 1)
        for project_summary, cluster in zip(state.project_summaries, state.batch_id_to_artifacts.values()):
            assert_summary(project_summary, len(cluster))
        assert_summary(state.final_project_summary, len(clustered_artifacts))

    def _assert_summarization(self, summarizer: Summarizer, expected_summarization_calls: int, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        dataset = summarizer.summarize()
        self.assertEqual(ai_manager.mock_calls, expected_summarization_calls)
        self.assertFalse(DataFrameUtil.contains_empty_string(dataset.artifact_df[ArtifactKeys.SUMMARY]))
        self.assertFalse(DataFrameUtil.contains_na(dataset.artifact_df[ArtifactKeys.SUMMARY]))
        self.assertIsInstance(dataset.project_summary, Summary)

    def get_summarizer(self, summarizer_args: SummarizerArgs,
                       with_artifact_summaries: bool = False, with_project_summary: bool = False) -> Summarizer:
        creator = PromptDatasetCreator(trace_dataset_creator=TraceDatasetCreator(SafaTestProject.get_project_reader()))
        dataset = creator.create()
        if with_artifact_summaries:
            dataset.artifact_df[ArtifactKeys.SUMMARY] = [f"summary of {c}" for c in dataset.artifact_df[ArtifactKeys.CONTENT]]
        if with_project_summary:
            dataset.project_summary = TEST_PROJECT_SUMMARY
        summarizer_args.summarize_code_only = False
        return Summarizer(summarizer_args, dataset)
