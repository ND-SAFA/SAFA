import os

from tgen.constants.open_ai_constants import MAX_TOKENS_BUFFER, OPEN_AI_MODEL_DEFAULT
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
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT, TestResponseManager, mock_openai
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.util.file_util import FileUtil


class TestSummarizer(BaseTest):
    CHUNKS = ["The cat in the hat sat", "on a log with a frog and a hog."]
    CONTENT = " ".join(CHUNKS)
    TEST_FILE_PATH = os.path.join(TEST_DATA_DIR, "chunker/test_python.py")
    TEST_FILE_CONTENT = FileUtil.read_file(TEST_FILE_PATH)
    MODEL_NAME = "code-cushman-002"

    @mock_openai()
    def test_summarize_chunks(self, response_manager: TestResponseManager):
        """
        Tests ability to summarize multiple chunks associated with single entity.
        """
        response_manager.format = SUMMARY_FORMAT
        response_manager.set_responses(self.CHUNKS)
        summarizer = self.get_summarizer()
        llm_manager = summarizer.llm_manager
        chunk_prompts = self.get_chunk_summary_prompts(llm_manager.prompt_args, summarizer)
        summary = summarizer._summarize_chunks(llm_manager, chunk_prompts)[0]
        expected_summary = "".join(SUMMARY_FORMAT.format(chunk) for chunk in self.CHUNKS)
        self.assertEqual(summary, expected_summary)

    @mock_openai()
    def test_summarize(self, response_manager: TestResponseManager):
        response_manager.set_responses([self.CONTENT])
        response_manager.format = SUMMARY_FORMAT

        summarizer = self.get_summarizer()

        content_summary = summarizer.summarize_single(content=self.CONTENT)
        expected_summary = SUMMARY_FORMAT.format(self.CONTENT)
        self.assertEqual(content_summary, expected_summary)

    @mock_openai()
    def test_code_or_exceeds_limit_true(self, response_manager: TestResponseManager):
        short_text = "This is a short text under the token limit"
        response_manager.set_responses([short_text])
        summarizer = self.get_summarizer(code_or_exceeds_limit_only=True, max_completion_tokens=500)
        content_summary = summarizer.summarize_single(content=short_text)
        self.assertEqual(content_summary, short_text)  # shouldn't have summarized

    @mock_openai()
    def test_code_summarization(self, response_manager: TestResponseManager):
        max_completion_tokens = 500

        # Calculated expected chunks + summary
        max_prompt_tokens = TokenLimitCalculator.calculate_max_prompt_tokens(self.MODEL_NAME,
                                                                             max_completion_tokens=max_completion_tokens)
        expected_chunks = PythonChunker(self.MODEL_NAME, max_prompt_tokens).chunk(self.TEST_FILE_CONTENT)
        expected_summarized_chunks = [SUMMARY_FORMAT.format(chunk) for chunk in expected_chunks]
        expected_summary = "".join(expected_summarized_chunks)

        response_manager.set_responses(expected_summarized_chunks + [expected_summary])
        summarizer = self.get_summarizer(max_completion_tokens=max_completion_tokens)
        content_summary = summarizer.summarize_single(self.TEST_FILE_CONTENT, chunker_type=SupportedChunker.PY)

        actual_links = content_summary.split("\n")
        expected_lines = content_summary.split("\n")
        self.assertEqual(len(actual_links), len(expected_lines))
        for i, (line_a, line_b) in enumerate(zip(actual_links, expected_lines)):
            self.assertEqual(line_a, line_b, msg=f"Line: {i}")

    @mock_openai()
    def test_summarize_bulk(self, response_manager: TestResponseManager):
        """
        Tests ability to summarize in bulk while still using chunkers.
        """
        NL_SUMMARY = "NL_SUMMARY"
        PL_SUMMARY = "PL_SUMMARY"

        # data
        nl_content = "Hello, this is a short text."
        contents = [nl_content, self.TEST_FILE_CONTENT]
        model_name = "gpt-3.5-turbo"
        summarizer = self.get_summarizer(model_name=model_name, code_or_exceeds_limit_only=False)

        # Create chunks for responses
        expected_chunks = PythonChunker(model_name, summarizer.max_prompt_tokens).chunk(self.TEST_FILE_CONTENT)
        chunk_responses = [f"Chunk {i}" for i in range(len(expected_chunks))]
        responses = [NL_SUMMARY] + chunk_responses + [PL_SUMMARY]
        response_manager.set_responses(responses)

        summaries = summarizer.summarize_bulk(bodies=contents,
                                              chunker_types=[SupportedChunker.NL, SupportedChunker.PY])
        self.assertEqual(NL_SUMMARY, summaries[0])
        self.assertEqual(PL_SUMMARY, summaries[1])

    @mock_openai()
    def test_summarize_bulk_code_or_exceeds_limit_only(self, response_manager: TestResponseManager):
        """
        Tests bulk summaries with code or exceeds limit only.
        """
        llm_manager = OpenAIManager(OpenAIArgs())
        token_limit = ModelTokenLimits.get_token_limit_for_model(OPEN_AI_MODEL_DEFAULT)
        summarizer = Summarizer(llm_manager, max_completion_tokens=token_limit - MAX_TOKENS_BUFFER - 5,
                                code_or_exceeds_limit_only=True)
        long_text = "This is a text is over the token limit"
        short_text = "short text"
        summaries = summarizer.summarize_bulk(bodies=[long_text, short_text])
        expected_summary = "".join([SUMMARY_FORMAT.format(chunk)
                                    for chunk in NaturalLanguageChunker(OPEN_AI_MODEL_DEFAULT, token_limit=5).chunk(long_text)])
        expected_summary = "".join([SUMMARY_FORMAT.format(chunk)
                                    for chunk in NaturalLanguageChunker(OPEN_AI_MODEL_DEFAULT, token_limit=5).chunk(expected_summary)])
        self.assertEqual(summaries[0], expected_summary)
        self.assertEqual(summaries[1], short_text)  # shouldn't have summarized

    def test_create_summarization_prompts(self):
        token_limit = ModelTokenLimits.get_token_limit_for_model(OPEN_AI_MODEL_DEFAULT)
        summarizer = self.get_summarizer(max_tokens_for_token_limit=token_limit - MAX_TOKENS_BUFFER - 5,
                                         code_or_exceeds_limit_only=True)
        short_text = "short text"
        prompts = summarizer._create_chunk_prompts(short_text)
        self.assertSize(0, prompts)  # should not be summarized because it is under token limit

        long_text = "This is a text is over the token limit"
        prompts = summarizer._create_chunk_prompts(long_text)
        expected_prompts = [summarizer.nl_prompt_builder.build(OpenAIManager.prompt_args,
                                                               artifact={ArtifactKeys.CONTENT: chunk})[PromptKeys.PROMPT]
                            for chunk in NaturalLanguageChunker(OPEN_AI_MODEL_DEFAULT, token_limit=5).chunk(long_text)]
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
        orig_content = orig_content.replace("\n", "")
        orig_content = orig_content.replace(" ", "")
        orig_content = orig_content.replace("\t", "")
        return orig_content

    @staticmethod
    def get_chunk_summary_prompts(prompt_args: PromptArgs, summarizer):
        def build_prompt(chunk):
            prompt_dict = summarizer.code_prompt_builder.build(prompt_args,
                                                               artifact={ArtifactKeys.CONTENT: chunk})
            return prompt_dict[PromptKeys.PROMPT]

        prompts = [build_prompt(chunk) for chunk in TestSummarizer.CHUNKS]
        return prompts
