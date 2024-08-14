import os
import re
from typing import Union

from common_resources.tools.constants.symbol_constants import NEW_LINE, SPACE, TAB, EMPTY_STRING
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.prompt_util import PromptUtil
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.prompt_keys import PromptKeys
from common_resources.data.keys.structure_keys import ArtifactKeys, TraceKeys
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from tgen.summarizer.artifact.artifact_summary_types import ArtifactSummaryTypes
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.steps.step_summarize_artifacts import StepSummarizeArtifacts
from tgen.testres.base_tests.base_test import BaseTest
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager
from tgen.testres.paths.paths import TEST_DATA_DIR


class TestSummarizer(BaseTest):
    CHUNKS = ["The cat in the hat sat", "on a log with a frog and a hog."]
    CONTENT = " ".join(CHUNKS)
    CODE_FILE_PATH = os.path.join(TEST_DATA_DIR, "chunker/test_python.py")
    CODE_CONTENT = FileUtil.read_file(CODE_FILE_PATH)
    MODEL_NAME = "gpt-4"
    MAX_COMPLETION_TOKENS = 500

    @mock_anthropic
    def test_summarize(self, response_manager: TestAIManager):
        """
        Tests ability to summarize single artifacts.
        - Verifies that code is chunked according to model token limit via data manager.
        - Verifies that summarized chunks are re-summarized.
        """
        NL_SUMMARY = "NL_SUMMARY"
        summarizer = self.get_summarizer()
        response_manager.set_responses([lambda prompt: self.get_response(prompt, ArtifactSummaryTypes.NL_BASE, NL_SUMMARY)])
        content_summary = summarizer.summarize_single(content="This is some text.")
        self.assertEqual(content_summary, NL_SUMMARY)

    @mock_anthropic
    def test_code_or_exceeds_limit_true(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        short_text = "This is a short text under the token limit"
        summarizer = self.get_summarizer(summarize_code_only=True)
        content_summary = summarizer.summarize_single(content=short_text)
        self.assertEqual(content_summary, short_text)  # shouldn't have summarized

    @mock_anthropic
    def test_code_summarization(self, ai_manager: TestAIManager):
        ai_manager.set_responses([lambda prompt: self.get_response(prompt, ArtifactSummaryTypes.CODE_BASE, CODE_SUMMARY)])
        CODE_SUMMARY = "CODE_SUMMARY"
        summarizer = self.get_summarizer()
        content_summary = summarizer.summarize_single(self.CODE_CONTENT, a_id="file.py")
        self.assertEqual(content_summary, CODE_SUMMARY)

    @mock_anthropic
    def test_summarize_bulk(self, response_manager: TestAIManager):
        """
        Tests ability to summarize in bulk while still using chunkers.
        - Verifies that content under limit is not summarized
        - Verifies that content over limit is summarized
        - Verifies that mix of content under and over limit work well together.
        """
        NL_SUMMARY = "NL_SUMMARY"
        PL_SUMMARY = "PL_SUMMARY"

        # data
        nl_content = "Hello, this is a short text."
        contents = [nl_content, self.CODE_CONTENT]
        summarizer = self.get_summarizer(summarize_code_only=False)

        response_manager.set_responses([lambda prompt: self.get_response(prompt, ArtifactSummaryTypes.NL_BASE, NL_SUMMARY),
                                        lambda prompt: self.get_response(prompt, ArtifactSummaryTypes.CODE_BASE, PL_SUMMARY)])

        summaries = summarizer.summarize_bulk(bodies=contents,
                                              ids=["natural language", "file.py"])
        self.assertEqual(NL_SUMMARY, summaries[0])
        self.assertEqual(PL_SUMMARY, summaries[1])

    @mock_anthropic
    def test_summarize_bulk_summarize_code_only(self, response_manager: TestAIManager):
        """
        Tests bulk summaries with code or exceeds limit only.
        - Verifies that only content over limit is summarized.
        """
        summarizer = self.get_summarizer(
            summarize_code_only=True)
        TEXT_1 = self.CODE_CONTENT
        TEXT_2 = "short text"
        TEXTS = [TEXT_1, TEXT_2]
        SUMMARY_1 = "SUMMARY_1"
        response_manager.set_responses([
            PromptUtil.create_xml(ArtifactsSummarizer.SUMMARY_TAG, SUMMARY_1)  # The re-summarization of the artifact.
        ])
        summaries = summarizer.summarize_bulk(bodies=TEXTS, ids=["file.py", "unknown"])

        self.assertEqual(summaries[0], SUMMARY_1)
        self.assertEqual(summaries[1], TEXT_2)  # shouldn't have summarized

    @mock_anthropic
    def test_context_summary(self, ai_manager: TestAIManager):
        links = [(8, 7), (2, 3), (1, 3), (7, 3), (1, 4), (3, 6), (3, 5), (6, 9)]
        links = [(self.convert_id_to_code_file(s), self.convert_id_to_code_file(t)) for s, t in links]
        trace_df = TraceDataFrame({TraceKeys.SOURCE: [s for s, _ in links],
                                   TraceKeys.TARGET: [t for _, t in links],
                                   TraceKeys.LABEL: [1 for _ in links]})
        artifact_ids = list(trace_df.get_artifact_ids())
        content = ["content" + id_ for id_ in artifact_ids]
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: artifact_ids, ArtifactKeys.CONTENT: content,
                                         ArtifactKeys.LAYER_ID: ["layer" for _ in artifact_ids]})
        context_mapping = TraceDataset(artifact_df=artifact_df, trace_df=trace_df,
                                       layer_df=LayerDataFrame()).create_dependency_mapping()
        for s, t in links:
            self.assertIn(s, [art[ArtifactKeys.ID] for art in context_mapping[t]])

        ai_manager.set_responses([lambda p: self.assert_context_prompt(p, context_mapping) for _ in artifact_ids])
        order = StepSummarizeArtifacts.get_summary_order(trace_df)
        expected_order = {0: [1, 2, 8],
                          1: [4, 7],
                          2: [3],
                          3: [5, 6],
                          4: [9]}
        self.assertDictEqual(order, {self.convert_id_to_code_file(node): order
                                     for order, nodes in expected_order.items() for node in nodes})
        summarizer = ArtifactsSummarizer(context_mapping=context_mapping, summary_order=order)
        artifact_df.summarize_content(summarizer)

    def assert_context_prompt(self, p, context_mapping):
        summary_response_format = "Summary of {}"
        summary = TestAIManager.create_summarization_response(p)
        content = summary.replace(summary_response_format.format(EMPTY_STRING), EMPTY_STRING)
        id_num = re.findall(r'\d+', content)[0]
        full_id = self.convert_id_to_code_file(id_num)
        if full_id in context_mapping:
            for related_artifact in context_mapping[full_id]:
                self.assertIn(summary_response_format.format(related_artifact[ArtifactKeys.CONTENT]), p)
        return summary

    def convert_id_to_code_file(self, orig_id: Union[int, str]):
        return f"{orig_id}.py"

    def get_summarizer(self, **kwargs):
        internal_kwargs = {"summarize_code_only": False}
        internal_kwargs.update(kwargs)
        summarizer = ArtifactsSummarizer(**internal_kwargs)
        return summarizer

    @staticmethod
    def _remove_irrelevant_chars(orig_content):
        orig_content = orig_content.replace(NEW_LINE, "")
        orig_content = orig_content.replace(SPACE, "")
        orig_content = orig_content.replace(TAB, "")
        return orig_content

    @staticmethod
    def get_chunk_summary_prompts(prompt_args: LLMPromptBuildArgs, summarizer):
        def build_prompt(chunk):
            prompt_dict = summarizer.code_prompt_builder.build(prompt_args,
                                                               artifact={ArtifactKeys.CONTENT: chunk})
            return prompt_dict[PromptKeys.PROMPT]

        prompts = [build_prompt(chunk) for chunk in TestSummarizer.CHUNKS]
        return prompts

    @staticmethod
    def get_response(prompt: str, summary_type: ArtifactSummaryTypes, expected_summary: str):
        if summary_type.value[0].value not in prompt:
            return "fail"
        return PromptUtil.create_xml(ArtifactsSummarizer.SUMMARY_TAG, expected_summary)
