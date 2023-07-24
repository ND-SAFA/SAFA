import os

from tgen.common.util.file_util import FileUtil
from tgen.constants.deliminator_constants import NEW_LINE, SPACE, TAB
from tgen.constants.open_ai_constants import MAX_TOKENS_BUFFER, OPEN_AI_MODEL_DEFAULT
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.models.llm.token_limits import ModelTokenLimits, TokenLimitCalculator
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_openai
from tgen.testres.testprojects.mocking.test_open_ai_responses import SUMMARY_FORMAT
from tgen.testres.testprojects.mocking.test_response_manager import TestResponseManager


class TestSummarizer(BaseTest):
    CHUNKS = ["The cat in the hat sat", "on a log with a frog and a hog."]
    CONTENT = " ".join(CHUNKS)
    CODE_FILE_PATH = os.path.join(TEST_DATA_DIR, "chunker/test_python.py")
    CODE_CONTENT = FileUtil.read_file(CODE_FILE_PATH)
    MODEL_NAME = "gpt-3.5-turbo"
    MAX_COMPLETION_TOKENS = 500

    @mock_openai
    def test_summarize_chunks(self, response_manager: TestResponseManager):
        """
        Tests ability to summarize multiple chunks and combine them.
        - Verifies that each chunk is summarized.
        - Verifies that summarized chunks are combined together.
        """
        response_manager.set_responses(["CHUNK_1", "CHUNK_2"])
        summarizer = self.get_summarizer()
        llm_manager = summarizer.llm_manager
        chunk_prompts = self.get_chunk_summary_prompts(llm_manager.prompt_args, summarizer)
        summary = summarizer._summarize_chunks(llm_manager, chunk_prompts)[0]
        expected_summary = "CHUNK_1 CHUNK_2"
        self.assertEqual(summary, expected_summary)

    @mock_openai
    def test_summarize(self, response_manager: TestResponseManager):
        """
        Tests ability to summarize single artifacts.
        - Verifies that code is chunked according to model token limit via data manager.
        - Verifies that summarized chunks are re-summarized.
        """
        CODE_SUMMARY = "CODE_SUMMARY"
        summarizer = self.get_summarizer()
        chunks = self.get_chunks(self.CODE_CONTENT, summarizer)
        response_manager.set_responses(["CH" for i in chunks] + [CODE_SUMMARY])
        content_summary = summarizer.summarize_single(content=self.CODE_CONTENT)
        self.assertEqual(content_summary, CODE_SUMMARY)

    @mock_openai(test_expected_responses=False)
    def test_code_or_exceeds_limit_true(self, response_manager: TestResponseManager):
        short_text = "This is a short text under the token limit"
        summarizer = self.get_summarizer(code_or_exceeds_limit_only=True, max_completion_tokens=500)
        content_summary = summarizer.summarize_single(content=short_text)
        self.assertEqual(content_summary, short_text)  # shouldn't have summarized

    @mock_openai
    def test_code_summarization(self, response_manager: TestResponseManager):
        max_completion_tokens = 500

        # Calculated expected chunks + summary
        max_prompt_tokens = TokenLimitCalculator.calculate_max_prompt_tokens(self.MODEL_NAME,
                                                                             max_completion_tokens=max_completion_tokens)
        expected_chunks = PythonChunker(self.MODEL_NAME, max_prompt_tokens).chunk(self.CODE_CONTENT)
        expected_summarized_chunks = [SUMMARY_FORMAT.format(chunk) for chunk in expected_chunks]
        expected_summary = "".join(expected_summarized_chunks)

        response_manager.set_responses(expected_summarized_chunks + [expected_summary])
        summarizer = self.get_summarizer(max_completion_tokens=max_completion_tokens)
        content_summary = summarizer.summarize_single(self.CODE_CONTENT, chunker_type=SupportedChunker.PY)

        actual_links = content_summary.split(NEW_LINE)
        expected_lines = content_summary.split(NEW_LINE)
        self.assertEqual(len(actual_links), len(expected_lines))
        for i, (line_a, line_b) in enumerate(zip(actual_links, expected_lines)):
            self.assertEqual(line_a, line_b, msg=f"Line: {i}")

    @mock_openai
    def test_summarize_bulk(self, response_manager: TestResponseManager):
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
        model_name = "gpt-3.5-turbo"
        summarizer = self.get_summarizer(model_name=model_name, code_or_exceeds_limit_only=False)

        # Create chunks for responses
        expected_chunks = PythonChunker(model_name, summarizer.max_prompt_tokens).chunk(self.CODE_CONTENT)
        chunk_responses = [f"Chunk {i}" for i in range(len(expected_chunks))]
        responses = [NL_SUMMARY] + chunk_responses + [PL_SUMMARY]
        response_manager.set_responses(responses)

        summaries = summarizer.summarize_bulk(bodies=contents,
                                              chunker_types=[SupportedChunker.NL, SupportedChunker.PY])
        self.assertEqual(NL_SUMMARY, summaries[0])
        self.assertEqual(PL_SUMMARY, summaries[1])

    @mock_openai
    def test_summarize_bulk_code_or_exceeds_limit_only(self, response_manager: TestResponseManager):
        """
        Tests bulk summaries with code or exceeds limit only.
        - Verifies that only content over limit is summarized.
        """
        MAX_PROMPT_TOKENS = 5
        token_limit = ModelTokenLimits.get_token_limit_for_model(self.MODEL_NAME)
        summarizer = self.get_summarizer(
            max_completion_tokens=token_limit - MAX_TOKENS_BUFFER - MAX_PROMPT_TOKENS,
            code_or_exceeds_limit_only=True)
        TEXT_1 = "This is a text is over the token limit"
        TEXT_2 = "short text"
        TEXTS = [TEXT_1, TEXT_2]
        SUMMARY_1 = "SUMMARY_1"
        response_manager.set_responses([
            "CH",  # Summary of chunk 1 for long prompt, must be 1-2 tokens to avoid re-summarization.
            "TH",  # Summary of chunk 1 for long prompt, must be 1-2 tokens
            SUMMARY_1  # The re-summarization of the artifact.
        ])
        summaries = summarizer.summarize_bulk(bodies=TEXTS)

        self.assertEqual(summaries[0], SUMMARY_1)
        self.assertEqual(summaries[1], TEXT_2)  # shouldn't have summarized

    def test_create_summarization_prompts(self):
        """
        Tests the ability to create prompts for chunks of content.
        """
        MAX_PROMPT_TOKENS = 5
        token_limit = ModelTokenLimits.get_token_limit_for_model(self.MODEL_NAME)
        summarizer = self.get_summarizer(max_completion_tokens=token_limit - MAX_TOKENS_BUFFER - MAX_PROMPT_TOKENS,
                                         code_or_exceeds_limit_only=True)
        short_text = "short text"
        prompts = summarizer._create_chunk_prompts(short_text)
        self.assertSize(0, prompts)  # should not be summarized because it is under token limit

        long_text = "This is a text is over the token limit"
        prompts = summarizer._create_chunk_prompts(long_text)
        expected_prompts = [summarizer.nl_prompt_builder.build(OpenAIManager.prompt_args,
                                                               artifact={ArtifactKeys.CONTENT: chunk})[PromptKeys.PROMPT]
                            for chunk in NaturalLanguageChunker(OPEN_AI_MODEL_DEFAULT, max_prompt_tokens=5).chunk(long_text)]
        self.assertListEqual(prompts, expected_prompts)

        python_code = "x = 1"
        prompts = summarizer._create_chunk_prompts(python_code, chunker_type=SupportedChunker.PY)
        self.assertEqual(prompts,
                         [summarizer.code_prompt_builder.build(artifact={ArtifactKeys.CONTENT: python_code},
                                                               model_format_args=OpenAIManager.prompt_args)[PromptKeys.PROMPT]])

        short_text = "short text"
        summarizer.code_or_above_limit_only = False
        prompts = summarizer._create_chunk_prompts(short_text)
        self.assertSize(1, prompts)  # should be summarized even though it is under token limit

    def get_summarizer(self, **kwargs):
        internal_kwargs = {"model_name": self.MODEL_NAME, "code_or_exceeds_limit_only": False}
        internal_kwargs.update(kwargs)
        llm_manager = OpenAIManager(OpenAIArgs())
        summarizer = Summarizer(llm_manager, **internal_kwargs)
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
    def get_chunks(content: str, summarizer: Summarizer, chunker_type: SupportedChunker = SupportedChunker.PY):
        model = summarizer.model_name
        max_prompt_tokens = summarizer.max_prompt_tokens
        expected_chunks = chunker_type.value(model, max_prompt_tokens).chunk(content)
        expected_summarized_chunks = [SUMMARY_FORMAT.format(chunk) for chunk in expected_chunks]
        return expected_summarized_chunks
