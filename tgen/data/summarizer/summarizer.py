import itertools
from typing import Dict, List, Set, Union

import pandas as pd

from tgen.common.util.base_object import BaseObject
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.deliminator_constants import EMPTY_STRING, SPACE
from tgen.constants.model_constants import get_efficient_default_llm_manager
from tgen.constants.open_ai_constants import MAX_TOKENS_DEFAULT, OPEN_AI_MODEL_DEFAULT
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.token_limits import TokenLimitCalculator


class Summarizer(BaseObject):
    """

    Summarizes bodies of code or text to create shorter, more succinct input for model
    """
    SUMMARY_TAG = "summary"

    def __init__(self, llm_manager: AbstractLLMManager = None, model_name: str = OPEN_AI_MODEL_DEFAULT,
                 max_completion_tokens: int = MAX_TOKENS_DEFAULT, code_or_exceeds_limit_only: bool = False,
                 nl_base_prompt: SupportedPrompts = SupportedPrompts.NL_SUMMARY,
                 code_base_prompt: SupportedPrompts = SupportedPrompts.CODE_SUMMARY):
        """
        Initializes a summarizer for a specific model
        :param model_name: name of the model that should be used to evaluate token_limit
        :param max_completion_tokens: the max number of tokens that the model can return as the completion
        :param code_or_exceeds_limit_only: if True, only performs summarization for text that exceeds the token limit or for code
        :param nl_base_prompt: The default prompt to use for summarization.
        :param code_base_prompt: The default summarization prompt to use for code.
        """
        max_prompt_tokens = TokenLimitCalculator.calculate_max_prompt_tokens(model_name,
                                                                             max_completion_tokens)
        if max_prompt_tokens < 0:
            raise ValueError("Tokens requested exceeds size of model context size with buffer.")
        self.llm_manager = get_efficient_default_llm_manager() if llm_manager is None else llm_manager
        self.model_name = model_name
        self.max_prompt_tokens = max_prompt_tokens
        self.args_for_summarizer_model = self.llm_manager.llm_args
        self.code_or_above_limit_only = code_or_exceeds_limit_only
        self.prompt_args = self.llm_manager.prompt_args
        self.code_prompt_builder = PromptBuilder(
            prompts=code_base_prompt.value)
        self.nl_prompt_builder = PromptBuilder(
            prompts=nl_base_prompt.value)

    def summarize_bulk(self, bodies: List[str], chunker_types: List[SupportedChunker] = None, ids: List[str] = None) -> List[str]:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param bodies: List of content to summarize
        :param chunker_types: The list of supported chunkers to use
        :param ids: The ids associated with each content
        :return: The summarization
        """
        selective_summary_payload = self.construct_select_summary_payload(bodies,
                                                                          chunker_types=chunker_types,
                                                                          ids=ids)
        indices2summarize, indices2resummarize, summary_prompts = selective_summary_payload
        logger.info(f"\nSummarizing {len(indices2summarize)} artifacts")
        summarized_content = self._chunk_and_summarize_selective(contents=bodies,
                                                                 indices2summarize=indices2summarize,
                                                                 prompts_for_summaries=summary_prompts)
        prompts_for_resummarization = self.create_resummarization_chunk_prompts(indices2resummarize, summarized_content)
        summaries = self._chunk_and_summarize_selective(contents=summarized_content,
                                                        indices2summarize=indices2resummarize,
                                                        prompts_for_summaries=prompts_for_resummarization)
        return summaries

    def create_resummarization_chunk_prompts(self, indices2resummarize: Set[int], summarized_content: List[str]):
        """
        Creates prompts enabling some artifacts to be re-summarized.
        :param indices2resummarize: The indices in content to resummarize.
        :param summarized_content: List of content global content.
        :return:
        """
        prompts_for_resummarization = []
        for i, content in enumerate(summarized_content):
            if i not in indices2resummarize:
                continue
            resummarization_prompt = self._create_chunk_prompts(content, code_or_above_limit_only=False)
            prompts_for_resummarization.append(resummarization_prompt)
        return prompts_for_resummarization

    def construct_select_summary_payload(self, bodies: List[str], chunker_types: List[SupportedChunker] = None, ids: List[str] = None):
        if chunker_types is None:
            chunker_types = [SupportedChunker.NL for _ in range(len(bodies))]
        if not isinstance(ids, List):
            ids = [ids for i in range(len(bodies))]
        assert len(chunker_types) == len(bodies) and len(ids) == len(bodies), "If supplying a chunker type and id, " \
                                                                              "must provide one for all content"

        indices2summarize = set()
        indices2resummarize = set()
        summary_prompts = []
        for i, body, chunker_type, id_ in zip(range(len(bodies)), bodies, chunker_types, ids):
            chunk_prompts = self._create_chunk_prompts(body, chunker_type, id_,
                                                       code_or_above_limit_only=self.code_or_above_limit_only)
            if len(chunk_prompts) < 1:  # no prompt because does not need summarized
                continue
            # Summarize the summarized chunks to have one congruent summary at the end
            if len(chunk_prompts) > 1:
                indices2resummarize.add(i)
            indices2summarize.add(i)
            summary_prompts.append(chunk_prompts)
        return indices2summarize, indices2resummarize, summary_prompts

    def summarize_single(self, content: str, chunker_type: SupportedChunker = SupportedChunker.NL, id_: str = None) -> str:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param content: Content to summarize
        :param chunker_type: The supported chunker to use
        :param id_: The id associated with the content
        :return: The summarization
        """
        chunk_prompts = self._create_chunk_prompts(content, chunker_type, id_,
                                                   code_or_above_limit_only=self.code_or_above_limit_only)
        if len(chunk_prompts) < 1:
            return content
        chunk_summaries = self._summarize_chunks(self.llm_manager, chunk_prompts)
        assert len(chunk_summaries) == 1, f"Expected single summary but received {len(chunk_summaries)}."
        content_summary = chunk_summaries[0]
        content_resummarized = self._summarize_chunks(self.llm_manager, [content_summary])
        assert len(content_resummarized) == 1, f"Expected single summary but received {len(content_resummarized)}."
        return content_resummarized[0]

    def summarize_dataframe(self, df: pd.DataFrame, col2summarize: str, col2use4chunker: str = None,
                            index_to_chunker_to_use: Dict[str, SupportedChunker] = None) -> pd.DataFrame:
        """
        Summarizes the information in a dataframe in a given column
        :param df: The dataframe to summarize
        :param col2summarize: The name of the column in the dataframe to summarize
        :param index_to_chunker_to_use: Dictionary mapping index to the chunker to use for that row
        :return: The dataframe with the contents in the given column summarized
        """
        ids = list(df.index)
        chunker_types = None
        if index_to_chunker_to_use:
            chunker_types = [index_to_chunker_to_use[index] for index in ids]
        elif col2use4chunker:
            chunker_types = [SupportedChunker.get_chunker_from_ext(row[col2use4chunker]) for _, row in df.iterrows()]
        summaries = self.summarize_bulk(list(df[col2summarize]), chunker_types, ids)
        df[col2summarize] = summaries
        return df

    def exceeds_token_limit(self, content: str) -> bool:
        """
        Determines if the given content exceeds the token limit
        :param content: The content
        :return: True if the content exceeds the token limit else False
        """
        prompt_tokens = TokenLimitCalculator.estimate_num_tokens(content, self.model_name)
        return prompt_tokens > self.max_prompt_tokens

    @staticmethod
    def _summarize_chunks(llm_manager: AbstractLLMManager, chunk_prompts: Union[List[str], List[List[str]]]) -> List[str]:
        """
        Summarizes all chunks using a given OpenAI model.
        :param llm_manager: The utility file containing API to AI library.
        :param chunk_prompts: The prompts used to summarize each chunk
        :return: The combined summaries of all chunks
        """
        if len(chunk_prompts) < 1:
            return chunk_prompts
        if not isinstance(chunk_prompts[0], List):
            chunk_prompts = [chunk_prompts]
        n_chunks_per_summary = [len(chunks) for chunks in chunk_prompts]
        all_prompts = list(itertools.chain.from_iterable(chunk_prompts))
        res: GenerationResponse = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                      prompt=all_prompts)
        if res is None:
            batch_responses = [EMPTY_STRING]
        else:
            parsed_responses = [LLMResponseUtil.parse(r, Summarizer.SUMMARY_TAG)[0] if Summarizer.SUMMARY_TAG in r else r for r in
                                res.batch_responses]
            batch_responses = [r.strip() for r in parsed_responses]

        summaries = []
        start_index = 0
        for n in n_chunks_per_summary:
            summaries.append(SPACE.join(batch_responses[start_index: start_index + n]))
            start_index += n
        return summaries

    def _create_chunk_prompts(self, content: str, chunker_type: SupportedChunker = SupportedChunker.NL, id_: str = None,
                              code_or_above_limit_only: bool = None) -> List[str]:
        """
        Prepares for summarization by creating the necessary prompts for each chunk
        :param content: Content to summarize
        :param chunker_type: The supported chunker to use
        :param id_: The id associated with the content
        :param code_or_above_limit_only: Needed only if different from self.code_or_above_limit_only
        :return: The list of prompts to use for summarization
        """
        code_or_above_limit_only = self.code_or_above_limit_only if code_or_above_limit_only is None else code_or_above_limit_only
        id_ = '' if not id_ else id_
        chunker = chunker_type.value(self.model_name, max_prompt_tokens=self.max_prompt_tokens)
        assert content is not None, "No content to summarize."
        chunks = chunker.chunk(content=content, id_=id_)
        if code_or_above_limit_only and len(chunks) <= 1 and chunker_type == SupportedChunker.NL:
            return []  # skip summarizing content below token limit unless code
        prompt_builder = self.nl_prompt_builder if chunker_type == SupportedChunker.NL else self.code_prompt_builder
        return [prompt_builder.build(model_format_args=self.llm_manager.prompt_args,
                                     artifact={ArtifactKeys.CONTENT: chunk})[PromptKeys.PROMPT.value] for chunk in chunks]

    def _chunk_and_summarize_selective(self,
                                       contents: List[str],
                                       indices2summarize: Set[int],
                                       prompts_for_summaries) -> List[str]:
        """
        Summarizes only the content whose index is in indices2summarize
        :param contents: Contents to summarize
        :param indices2summarize: Index of the content that should be summarized
        :param prompts_for_summaries: The prompts for summarization (corresponds to only the content selected for summarization)
        :return: The summarization if summarized else the original content
        """
        summarized_contents = self._summarize_chunks(self.llm_manager, prompts_for_summaries)
        summaries_iter = iter(summarized_contents)
        summaries = []
        for index, content in enumerate(contents):
            summary = next(summaries_iter) if index in indices2summarize else content
            summaries.append(summary)
        return summaries
