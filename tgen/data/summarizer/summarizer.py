import os
from typing import List

import pandas as pd

from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.base_prompt import BasePrompt
from tgen.data.prompts.creation_prompt_creator import GenerationPromptCreator
from tgen.data.summarizer.chunkers.supported_chunker import SupportedChunker
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.base_object import BaseObject
from tgen.util.file_util import FileUtil
from tgen.util.open_ai_util import OpenAiUtil


class Summarizer(BaseObject):
    """
    Summarizes bodies of code or text to create shorter, more succinct input for model
    """

    def __init__(self, model_path: str = None, args: OpenAiArgs = None, code_or_exceeds_limit_only: bool = True):
        """
        Initializes a summarizer for a specific model
        :param model_path: path of the model that should be used for summarization
        :param args: any additional args to use for summarization
        :param code_or_exceeds_limit_only: if True, only performs summarization for text that exceeds the token limit or for code
        """
        self.model_path = model_path
        self.args = OpenAiArgs() if not args else args
        self.code_or_above_limit_only = code_or_exceeds_limit_only

    def summarize(self, path_to_file: str = None, content: str = None, is_code: bool = False) -> str:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param path_to_file: Path to the file to summarize
        :param content: Content to summarize
        :param is_code: If True, file/content is code, else assumed to be natural language
        :return: The summarization
        """
        chunker = self._get_chunker(path_to_file)
        is_code = is_code or chunker != SupportedChunker.NL
        model_path = self._get_model_name_for_content(is_code) if not self.model_path else self.model_path
        chunker = chunker.value(model_path)
        content = FileUtil.read_file(path_to_file) if path_to_file else content
        assert content is not None, "No content to summarize."
        chunks = chunker.chunk(content=content)
        if self.code_or_above_limit_only and len(chunks) <= 1 and not is_code:
            return content
        prompt_creator = GenerationPromptCreator(base_prompt=BasePrompt.CODE_SUMMARY if is_code else BasePrompt.NL_SUMMARY)
        summarizations = self._summarize_chunks(chunks, prompt_creator, model_path, self.args)
        return os.linesep.join(summarizations)

    def summarize_dataframe(self, df: pd.DataFrame, col2summarize: str):
        """
        Summarizes the information in a dataframe in a given column
        :param df: The dataframe to summarize
        :param col2summarize: The name of the column in the dataframe to summarize
        :return: The dataframe with the contents in the given column summarized
        """
        df[col2summarize] = df[col2summarize].apply(lambda item: self.summarize(content=item))
        return df

    @staticmethod
    def _summarize_chunks(chunks: List[str], prompt_creator: GenerationPromptCreator, model_path: str, args: OpenAiArgs) -> List[str]:
        """
        Summarizes all chunks using a given OpenAI model
        :param model_path: The model to use for summarizations
        :param prompt_creator: The generator to use to create prompts for summarizations
        :param chunks: The chunks of text to summarize
        :return: The summaries of all chunks
        """
        prompts = [prompt_creator.create(target_content=chunk, source_content='')[PromptKeys.PROMPT.value]
                   for chunk in chunks]
        res = OpenAiUtil.make_completion_request(model=model_path, prompt=prompts,
                                                 **args.to_params(prompt_creator, TrainerTask.PREDICT))
        return [choice.text.strip() for choice in res.choices]

    @staticmethod
    def _get_chunker(path_to_file: str = None) -> SupportedChunker:
        """
        Gets the chunker responsible for breaking a file or content into smaller pieces for the model
        :param path_to_file: The path to the file being chunked
        :return: The chunker to use
        """
        default = SupportedChunker.NL
        if not path_to_file:
            return default
        ext = FileUtil.get_file_ext(path_to_file)
        try:
            return SupportedChunker[ext[1:].upper()]
        except Exception:
            return default

    @staticmethod
    def _get_model_name_for_content(is_code: bool) -> str:
        """
        Gets the best model for the content being summarized
        :param is_code: True if the content is code, else assumed to be Natural language
        :return: The best model for the content being summarized
        """
        return "text-davinci-003"
