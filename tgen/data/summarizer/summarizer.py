import os
from typing import List

import pandas as pd

from tgen.constants import GENERATION_MODEL_DEFAULT, MAX_TOKENS_DEFAULT, SUMMARIZATION_MODEL_DEFAULT
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.data.summarizer.chunkers.abstract_chunker import AbstractChunker
from tgen.data.summarizer.chunkers.supported_chunker import SupportedChunker
from tgen.train.args.open_ai_args import OpenAiArgs
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.ai.open_ai_util import OpenAIUtil
from tgen.util.base_object import BaseObject
from tgen.util.file_util import FileUtil


class Summarizer(BaseObject):
    """
    Summarizes bodies of code or text to create shorter, more succinct input for model
    """

    def __init__(self, model_for_summarizer: str = SUMMARIZATION_MODEL_DEFAULT, model_for_token_limit: str = GENERATION_MODEL_DEFAULT,
                 args_for_summarizer_model: OpenAiArgs = None, max_tokens: int = MAX_TOKENS_DEFAULT,
                 code_or_exceeds_limit_only: bool = True):
        """
        Initializes a summarizer for a specific model
        :param model_for_summarizer: path of the model that should be used for summarization
        :param model_for_token_limit: name of the model that should be used to evaluate token_limit
        :param args_for_summarizer_model: any additional args to use for summarization
        :param max_tokens: the max number of tokens that the model can return as the completion
        :param code_or_exceeds_limit_only: if True, only performs summarization for text that exceeds the token limit or for code
        """
        self.model_for_summarizer = model_for_summarizer
        self.model_for_token_limit = model_for_token_limit
        self.args_for_summarizer_model = OpenAiArgs() if not args_for_summarizer_model else args_for_summarizer_model
        self.code_or_above_limit_only = code_or_exceeds_limit_only
        self.max_tokens = max_tokens
        self.prompt_args = self.args_for_summarizer_model.prompt_args

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
        chunker = chunker.value(self.model_for_token_limit, max_tokens=self.max_tokens)
        content = FileUtil.read_file(path_to_file) if path_to_file else content
        assert content is not None, "No content to summarize."
        chunks = chunker.chunk(content=content)
        if self.code_or_above_limit_only and len(chunks) <= 1 and not is_code:
            return content
        self.args_for_summarizer_model.prompt_creator = GenerationPromptCreator(
            prompt_args=self.prompt_args,
            base_prompt=SupportedPrompts.CODE_SUMMARY if is_code else SupportedPrompts.NL_SUMMARY)
        summarizations = self._summarize_chunks(chunks, self.model_for_summarizer, self.args_for_summarizer_model)
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

    def exceeds_token_limit(self, content: str) -> bool:
        """
        Determines if the given content exceeds the token limit
        :param content: The content
        :return: True if the content exceeds the token limit else False
        """
        chunker_type: SupportedChunker = self._get_chunker()
        chunker: AbstractChunker = chunker_type.value(self.model_for_token_limit, max_tokens=self.max_tokens)
        return chunker.exceeds_token_limit(content)

    @staticmethod
    def _summarize_chunks(chunks: List[str], model_path: str, args: OpenAiArgs) -> List[str]:
        """
        Summarizes all chunks using a given OpenAI model
        :param model_path: The model to use for summarizations
        :param chunks: The chunks of text to summarize
        :return: The summaries of all chunks
        """
        prompts = [args.prompt_creator.create(target_content=chunk, source_content='')[PromptKeys.PROMPT.value]
                   for chunk in chunks]
        res = OpenAIUtil.make_completion_request(model=model_path, prompt=prompts,
                                                 **args.to_params(TrainerTask.PREDICT))
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
