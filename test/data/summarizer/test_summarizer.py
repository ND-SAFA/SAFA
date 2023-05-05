import os
from unittest import mock

from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.summarizer.summarizer import Summarizer
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT, fake_open_ai_completion
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.util.file_util import FileUtil
from tgen.models.llm.supported_llm_manager import SupportedLLMManager


class TestSummarizer(BaseTest):
    CHUNKS = ["The cat in the hat sat", "on a log with a frog and a hog."]

    @mock.patch("openai.Completion.create", )
    def test_summarize_chunks(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        summarizer = Summarizer(code_or_exceeds_limit_only=False)
        summaries = summarizer._summarize_chunks(SupportedLLMManager.OPENAI.value, summarizer.nl_prompt_creator, self.CHUNKS,
                                                 "text-davinci-003", OpenAIArgs())
        for i, summary in enumerate(summaries):
            self.assertEqual(summary, SUMMARY_FORMAT.format(self.CHUNKS[i]))

    @mock.patch("openai.Completion.create")
    def test_summarize(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        model_name = "code-cushman-002"

        # use file content
        summarizer = Summarizer(code_or_exceeds_limit_only=False, model_for_token_limit=model_name)
        content = " ".join(self.CHUNKS)
        summaries = summarizer.summarize(content=content)
        self.assertEqual(summaries, SUMMARY_FORMAT.format(content))

        # use path to file
        path_to_file = os.path.join(TEST_DATA_DIR, "chunker/test_python.py")
        content = FileUtil.read_file(path_to_file)
        summaries = summarizer.summarize(content, chunker_type=SupportedChunker.PY)
        summaries = summaries.replace("\n", "")
        expected_chunks = PythonChunker(model_name, summarizer.token_limit).chunk(FileUtil.read_file(path_to_file))
        summarized_chunks = [SUMMARY_FORMAT.format(chunk.replace("\n", "")) for chunk in expected_chunks]
        self.assertEqual("".join(summarized_chunks), summaries)

        # set code_or_exceeds_limit_only to TRUE this time
        summarizer = Summarizer(code_or_exceeds_limit_only=True, model_for_summarizer=model_name)
        short_text = "This is a short text under the token limit"
        summaries = summarizer.summarize(content=short_text)
        self.assertEqual(summaries, short_text)  # shouldn't have summarized
