import itertools
import os
from typing import List, Dict, Union

import pandas as pd
from tqdm import tqdm

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.constants.model_constants import get_default_llm_manager
from tgen.constants.open_ai_constants import GENERATION_MODEL_DEFAULT, MAX_TOKENS_DEFAULT
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.token_limits import TokenLimitCalculator
from tgen.util.base_object import BaseObject


class Summarizer(BaseObject):
    """
    Summarizes bodies of code or text to create shorter, more succinct input for model
    """

    def __init__(self, llm_manager: AbstractLLMManager = None, model_for_token_limit: str = GENERATION_MODEL_DEFAULT,
                 max_tokens_for_token_limit: int = MAX_TOKENS_DEFAULT, code_or_exceeds_limit_only: bool = False,
                 nl_base_prompt: SupportedPrompts = SupportedPrompts.NL_SUMMARY,
                 code_base_prompt: SupportedPrompts = SupportedPrompts.CODE_SUMMARY):
        """
        Initializes a summarizer for a specific model
        :param model_for_token_limit: name of the model that should be used to evaluate token_limit
        :param max_tokens_for_token_limit: the max number of tokens that the model can return as the completion
        :param code_or_exceeds_limit_only: if True, only performs summarization for text that exceeds the token limit or for code
        :param nl_base_prompt: The default prompt to use for summarization.
        :param code_base_prompt: The default summarization prompt to use for code.
        """
        self.llm_manager = get_default_llm_manager() if llm_manager is None else llm_manager
        self.model_for_token_limit = model_for_token_limit
        self.token_limit = TokenLimitCalculator.calculate_token_limit(self.model_for_token_limit, max_tokens_for_token_limit)
        self.args_for_summarizer_model = self.llm_manager.llm_args
        self.code_or_above_limit_only = code_or_exceeds_limit_only
        self.prompt_args = self.llm_manager.prompt_args
        self.code_prompt_creator = GenerationPromptCreator(
            prompt_args=self.prompt_args,
            base_prompt=code_base_prompt)
        self.nl_prompt_creator = GenerationPromptCreator(
            prompt_args=self.prompt_args,
            base_prompt=nl_base_prompt)

    def summarize_bulk(self, contents: List[str], chunker_types: List[SupportedChunker] = None, ids: List[str] = None) -> List[str]:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param contents: List of content to summarize
        :param chunker_types: The list of supported chunkers to use
        :param ids: The ids associated with each content
        :return: The summarization
        """
        chunker_types = [SupportedChunker.NL for i in range(len(contents))] if not chunker_types else chunker_types
        ids = [ids for i in range(len(contents))] if not isinstance(ids, List) else ids
        assert len(chunker_types) == len(contents) and len(ids) == len(contents), "If supplying a chunker type and id, " \
                                                                                  "must provide one for all content"
        indices2summarize = set()
        prompts_for_summaries = []
        for i, content, chunker_type, id_ in zip(range(len(contents)), contents, chunker_types, ids):
            prompts = self._create_summarization_prompts(content, chunker_type, id_)
            if len(prompts) < 1:
                continue
            indices2summarize.add(i)
            prompts_for_summaries.append(prompts)
        summarized_contents = self._summarize_chunks(self.llm_manager, prompts_for_summaries)
        summaries_iter = iter(summarized_contents)
        return [next(summaries_iter) if index in indices2summarize else content for index, content in enumerate(contents)]

    def summarize_single(self, content: str, chunker_type: SupportedChunker = SupportedChunker.NL, id_: str = None) -> str:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param content: Content to summarize
        :param chunker_type: The supported chunker to use
        :param id_: The id associated with the content
        :return: The summarization
        """
        prompts = self._create_summarization_prompts(content, chunker_type, id_)
        if len(prompts) < 1:
            return content
        return self._summarize_chunks(self.llm_manager, prompts)[0]

    def summarize_dataframe(self, df: pd.DataFrame, col2summarize: str,
                            index_to_chunker_to_use: Dict[str, SupportedChunker] = None):
        """
        Summarizes the information in a dataframe in a given column
        :param df: The dataframe to summarize
        :param col2summarize: The name of the column in the dataframe to summarize
        :param index_to_chunker_to_use: Dictionary mapping index to the chunker to use for that row
        :return: The dataframe with the contents in the given column summarized
        """
        ids = list(df.index)
        chunker_types = None if index_to_chunker_to_use is None else [index_to_chunker_to_use[index] for index in ids]
        summaries = self.summarize_bulk(list(df[col2summarize]), chunker_types, ids)
        df[col2summarize] = summaries
        return df

    def exceeds_token_limit(self, content: str) -> bool:
        """
        Determines if the given content exceeds the token limit
        :param content: The content
        :return: True if the content exceeds the token limit else False
        """
        return TokenLimitCalculator.estimate_num_tokens(content, self.model_for_token_limit) > self.token_limit

    @staticmethod
    def _summarize_chunks(llm_manager: AbstractLLMManager, prompts: Union[List[str], List[List[str]]]) -> List[str]:
        """
        Summarizes all chunks using a given OpenAI model.
        :param llm_manager: The utility file containing API to AI library.
        :param prompts: The prompts used to summarize each chunk
        :return: The combined summaries of all chunks
        """
        if len(prompts) < 1:
            return prompts
        if not isinstance(prompts[0], List):
            prompts = [prompts]
        n_chunks_per_summary = [len(chunks) for chunks in prompts]
        all_prompts = list(itertools.chain.from_iterable(prompts))
        res: GenerationResponse = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                      prompt=all_prompts)
        summarizations_chunks = [r.strip() for r in res.batch_responses] if res else [EMPTY_STRING]
        summaries = [EMPTY_STRING.join(summarizations_chunks[i: i + n]) for i, n in enumerate(n_chunks_per_summary)]
        return summaries

    def _create_summarization_prompts(self, content: str, chunker_type: SupportedChunker = SupportedChunker.NL, id_: str = None) \
            -> List[str]:
        """
        Prepares for summarization by creating the necessary prompts for each chunk
        :param content: Content to summarize
        :param chunker_type: The supported chunker to use
        :param id_: The id associated with the content
        :return: The list of prompts to use for summarization
        """
        id_ = '' if not id_ else id_
        chunker = chunker_type.value(self.model_for_token_limit, token_limit=self.token_limit)
        assert content is not None, "No content to summarize."
        chunks = chunker.chunk(content=content, id_=id_)
        if self.code_or_above_limit_only and len(chunks) <= 1 and chunker_type == SupportedChunker.NL:
            return []  # skip summarizing content below token limit unless code
        prompt_creator = self.nl_prompt_creator if chunker_type == SupportedChunker.NL else self.code_prompt_creator
        return [prompt_creator.create(target_content=chunk)[PromptKeys.PROMPT.value] for chunk in chunks]
