import os
from unittest import mock

from tgen.constants.open_ai_constants import GENERATION_MODEL_DEFAULT, MAX_TOKENS_BUFFER
from tgen.data.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.models.llm.token_limits import ModelTokenLimits
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT, fake_open_ai_completion
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.util.file_util import FileUtil


class TestSummarizer(BaseTest):
    CHUNKS = ["The cat in the hat sat", "on a log with a frog and a hog."]

    @mock.patch("openai.Completion.create", )
    def test_summarize_chunks(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        llm_manager = OpenAIManager(OpenAIArgs())
        summarizer = Summarizer(llm_manager, code_or_exceeds_limit_only=False)
        prompts = [summarizer.nl_prompt_creator.create(chunk)[PromptKeys.PROMPT] for chunk in self.CHUNKS]
        summary = summarizer._summarize_chunks(llm_manager, prompts)[0]
        expected_summary = "".join(SUMMARY_FORMAT.format(chunk) for chunk in self.CHUNKS)
        self.assertEqual(summary, expected_summary)

    @mock.patch("openai.Completion.create")
    def test_summarize(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        model_name = "code-cushman-002"

        # use file content
        llm_manager = OpenAIManager(OpenAIArgs())
        summarizer = Summarizer(llm_manager, model_for_token_limit=model_name, code_or_exceeds_limit_only=False)
        content = " ".join(self.CHUNKS)
        summaries = summarizer.summarize_single(content=content)
        self.assertEqual(summaries, SUMMARY_FORMAT.format(content))

        # use path to file
        path_to_file = os.path.join(TEST_DATA_DIR, "chunker/test_python.py")
        content = FileUtil.read_file(path_to_file)
        summaries = summarizer.summarize_single(content, chunker_type=SupportedChunker.PY)
        summaries = summaries.replace("\n", "")
        expected_chunks = PythonChunker(model_name, summarizer.token_limit).chunk(FileUtil.read_file(path_to_file))
        summarized_chunks = [SUMMARY_FORMAT.format(chunk.replace("\n", "")) for chunk in expected_chunks]
        self.assertEqual("".join(summarized_chunks), summaries)

        # set code_or_exceeds_limit_only to TRUE this time
        llm_manager = OpenAIManager(OpenAIArgs())
        summarizer = Summarizer(llm_manager, code_or_exceeds_limit_only=True)
        short_text = "This is a short text under the token limit"
        summaries = summarizer.summarize_single(content=short_text)
        self.assertEqual(summaries, short_text)  # shouldn't have summarized

    @mock.patch("openai.Completion.create")
    def test_summarize_bulk(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        model_name = "code-cushman-002"

        # use file content
        llm_manager = OpenAIManager(OpenAIArgs())
        summarizer = Summarizer(llm_manager, model_for_token_limit=model_name, code_or_exceeds_limit_only=False)
        python_file_contents = FileUtil.read_file(os.path.join(TEST_DATA_DIR, "chunker/test_python.py"))
        contents = [" ".join(self.CHUNKS), python_file_contents]
        summaries = summarizer.summarize_bulk(contents=contents, chunker_types=[SupportedChunker.NL, SupportedChunker.PY])
        self.assertEqual(summaries[0], SUMMARY_FORMAT.format(contents[0]))
        summaries[1] = summaries[1].replace("\n", "")
        expected_chunks = PythonChunker(model_name, summarizer.token_limit).chunk(python_file_contents)
        summarized_chunks = [SUMMARY_FORMAT.format(chunk.replace("\n", "")) for chunk in expected_chunks]
        self.assertEqual("".join(summarized_chunks), summaries[1])

        # set code_or_exceeds_limit_only to TRUE this time
        llm_manager = OpenAIManager(OpenAIArgs())
        token_limit = ModelTokenLimits.get_token_limit_for_model(GENERATION_MODEL_DEFAULT)
        summarizer = Summarizer(llm_manager, max_tokens_for_token_limit=token_limit - MAX_TOKENS_BUFFER - 5,
                                code_or_exceeds_limit_only=True)
        long_text = "This is a text is over the token limit"
        short_text = "short text"
        summaries = summarizer.summarize_bulk(contents=[long_text, short_text])
        expected_summary = "".join([SUMMARY_FORMAT.format(chunk)
                                    for chunk in NaturalLanguageChunker(GENERATION_MODEL_DEFAULT, token_limit=5).chunk(long_text)])
        self.assertEqual(summaries[0], expected_summary)
        self.assertEqual(summaries[1], short_text)  # shouldn't have summarized

    def test_create_summarization_prompts(self):
        token_limit = ModelTokenLimits.get_token_limit_for_model(GENERATION_MODEL_DEFAULT)
        summarizer = Summarizer(OpenAIManager(OpenAIArgs()), max_tokens_for_token_limit=token_limit - MAX_TOKENS_BUFFER - 5,
                                code_or_exceeds_limit_only=True)
        short_text = "short text"
        prompts = summarizer._create_summarization_prompts(short_text)
        self.assertSize(0, prompts) # should not be summarized because it is under token limit

        long_text = "This is a text is over the token limit"
        prompts = summarizer._create_summarization_prompts(long_text)
        expected_prompts = [summarizer.nl_prompt_creator.create(chunk)[PromptKeys.PROMPT]
                            for chunk in NaturalLanguageChunker(GENERATION_MODEL_DEFAULT, token_limit=5).chunk(long_text)]
        self.assertListEqual(prompts, expected_prompts)

        python_code = "x = 1"
        prompts = summarizer._create_summarization_prompts(python_code, chunker_type=SupportedChunker.PY)
        self.assertEqual(prompts, [summarizer.code_prompt_creator.create(python_code)[PromptKeys.PROMPT]])

        short_text = "short text"
        summarizer.code_or_above_limit_only = False
        prompts = summarizer._create_summarization_prompts(short_text)
        self.assertSize(1, prompts)  # should be summarized even though it is under token limit



