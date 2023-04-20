import os
from unittest import mock

from tgen.data.prompts.base_prompt import BasePrompt
from tgen.data.prompts.creation_prompt_creator import GenerationPromptCreator
from tgen.data.summarizer.chunkers.python_chunker import PythonChunker
from tgen.data.summarizer.chunkers.supported_chunker import SupportedChunker
from tgen.data.summarizer.summarizer import Summarizer
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT, fake_open_ai_completion
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.util.file_util import FileUtil


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
        summarizer = Summarizer()
        summaries = summarizer._summarize_chunks(self.CHUNKS,
                                                 GenerationPromptCreator(BasePrompt.NL_SUMMARY), "text-davinci-003", OpenAiArgs())
        for i, summary in enumerate(summaries):
            self.assertEqual(summary, SUMMARY_FORMAT.format(self.CHUNKS[i]))

    @mock.patch("openai.Completion.create")
    def test_summarize(self, mock_completion: mock.MagicMock):
        mock_completion.side_effect = fake_open_ai_completion
        summarizer = Summarizer()
        content = " ".join(self.CHUNKS)
        summaries = summarizer.summarize(content=content)
        self.assertEqual(summaries, SUMMARY_FORMAT.format(content))

        model_name = summarizer._get_model_name_for_content(is_code=True)
        path_to_file = os.path.join(TEST_DATA_DIR, "chunker/test_python.py")
        summaries = summarizer.summarize(path_to_file=path_to_file)
        expected_chunks = PythonChunker(model_name).chunk(FileUtil.read_file(path_to_file))
        summarized_chunks = [SUMMARY_FORMAT.format(chunk) for chunk in expected_chunks]
        self.assertEqual("\n".join(summarized_chunks), summaries)
