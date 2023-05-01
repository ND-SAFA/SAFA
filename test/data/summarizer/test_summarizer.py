import os
from unittest import mock

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.summarizer.chunkers.python_chunker import PythonChunker
from tgen.data.summarizer.chunkers.supported_chunker import SupportedChunker
from tgen.data.summarizer.summarizer import Summarizer
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT, fake_open_ai_completion
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.util.file_util import FileUtil
from tgen.util.llm.supported_ai_utils import SupportedLLMUtils


class TestSummarizer(BaseTest):
    CHUNKS = ["The cat in the hat sat", "on a log with a frog and a hog."]

    def test_get_chunker(self):
        self.assertEqual(Summarizer._get_chunker("file.py"), SupportedChunker.PY)
        self.assertEqual(Summarizer._get_chunker("file.java"), SupportedChunker.JAVA)
        self.assertEqual(Summarizer._get_chunker("file.txt"), SupportedChunker.NL)
        self.assertEqual(Summarizer._get_chunker(), SupportedChunker.NL)

    @mock.patch("openai.Completion.create", )
    def test_summarize_chunks(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        summarizer = Summarizer(code_or_exceeds_limit_only=False)
        summaries = summarizer._summarize_chunks(SupportedLLMUtils.OPENAI.value, summarizer.nl_prompt_creator, self.CHUNKS,
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
        summaries = summarizer.summarize(path_to_file=path_to_file)
        summaries = summaries.replace("\n", "")
        expected_chunks = PythonChunker(model_name).chunk(FileUtil.read_file(path_to_file))
        summarized_chunks = [SUMMARY_FORMAT.format(chunk.replace("\n", "")) for chunk in expected_chunks]
        self.assertEqual("".join(summarized_chunks), summaries)

        # set code_or_exceeds_limit_only to TRUE this time
        summarizer = Summarizer(code_or_exceeds_limit_only=True, model_for_summarizer=model_name)
        short_text = "This is a short text under the token limit"
        summaries = summarizer.summarize(content=short_text)
        self.assertEqual(summaries, short_text)  # shouldn't have summarized
