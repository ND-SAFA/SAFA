import os

from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.constants.deliminator_constants import NEW_LINE, SPACE, TAB
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.prompts.prompt_args import PromptArgs
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary_types import SummaryTypes
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestSummarizer(BaseTest):
    CHUNKS = ["The cat in the hat sat", "on a log with a frog and a hog."]
    CONTENT = " ".join(CHUNKS)
    CODE_FILE_PATH = os.path.join(TEST_DATA_DIR, "chunker/test_python.py")
    CODE_CONTENT = FileUtil.read_file(CODE_FILE_PATH)
    MODEL_NAME = "gpt-3.5-turbo"
    MAX_COMPLETION_TOKENS = 500

    @mock_openai
    def test_summarize(self, response_manager: TestAIManager):
        """
        Tests ability to summarize single artifacts.
        - Verifies that code is chunked according to model token limit via data manager.
        - Verifies that summarized chunks are re-summarized.
        """
        NL_SUMMARY = "NL_SUMMARY"
        summarizer = self.get_summarizer()
        response_manager.set_responses([ lambda prompt: self.get_response(prompt, SummaryTypes.NL_BASE, NL_SUMMARY)])
        content_summary = summarizer.summarize_single(content="This is some text.")
        self.assertEqual(content_summary, NL_SUMMARY)

    @mock_openai
    def test_code_or_exceeds_limit_true(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        short_text = "This is a short text under the token limit"
        summarizer = self.get_summarizer(summarize_code_only=True)
        content_summary = summarizer.summarize_single(content=short_text)
        self.assertEqual(content_summary, short_text)  # shouldn't have summarized

    @mock_openai
    def test_code_summarization(self, ai_manager: TestAIManager):
        ai_manager.set_responses([ lambda prompt: self.get_response(prompt, SummaryTypes.CODE_BASE, CODE_SUMMARY)])
        CODE_SUMMARY = "CODE_SUMMARY"
        summarizer = self.get_summarizer()
        content_summary = summarizer.summarize_single(self.CODE_CONTENT, filename="file.py")
        self.assertEqual(content_summary, CODE_SUMMARY)

    @mock_openai
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

        response_manager.set_responses([lambda prompt: self.get_response(prompt, SummaryTypes.NL_BASE, NL_SUMMARY),
                                        lambda prompt: self.get_response(prompt, SummaryTypes.CODE_BASE, PL_SUMMARY)])

        summaries = summarizer.summarize_bulk(bodies=contents,
                                              filenames=["natural language", "file.py"])
        self.assertEqual(NL_SUMMARY, summaries[0])
        self.assertEqual(PL_SUMMARY, summaries[1])

    @mock_openai
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
        summaries = summarizer.summarize_bulk(bodies=TEXTS, filenames=["file.py", "unknown"])

        self.assertEqual(summaries[0], SUMMARY_1)
        self.assertEqual(summaries[1], TEXT_2)  # shouldn't have summarized

    def get_summarizer(self, **kwargs):
        internal_kwargs = {"summarize_code_only": False}
        internal_kwargs.update(kwargs)
        llm_manager = OpenAIManager(OpenAIArgs())
        summarizer = ArtifactsSummarizer(SummarizerArgs(llm_manager_for_artifact_summaries=llm_manager, **internal_kwargs))
        return summarizer

    @staticmethod
    def _remove_irrelevant_chars(orig_content):
        orig_content = orig_content.replace(NEW_LINE, "")
        orig_content = orig_content.replace(SPACE, "")
        orig_content = orig_content.replace(TAB, "")
        return orig_content

    @staticmethod
    def get_chunk_summary_prompts(prompt_args: PromptArgs, summarizer):
        def build_prompt(chunk):
            prompt_dict = summarizer.code_prompt_builder.build(prompt_args,
                                                               artifact={ArtifactKeys.CONTENT: chunk})
            return prompt_dict[PromptKeys.PROMPT]

        prompts = [build_prompt(chunk) for chunk in TestSummarizer.CHUNKS]
        return prompts

    @staticmethod
    def get_response(prompt: str, summary_type: SummaryTypes, expected_summary: str):
        if summary_type.value[0].value not in prompt:
            return "fail"
        return PromptUtil.create_xml(ArtifactsSummarizer.SUMMARY_TAG, expected_summary)
