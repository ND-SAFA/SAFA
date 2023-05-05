import os
from typing import List

import pandas as pd
from tqdm import tqdm

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.constants.open_ai_constants import GENERATION_MODEL_DEFAULT, MAX_TOKENS_DEFAULT, SUMMARIZATION_MODEL_DEFAULT
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.token_limits import TokenLimitCalculator
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.base_object import BaseObject


class Summarizer(BaseObject):
    """
    Summarizes bodies of code or text to create shorter, more succinct input for model
    """

    def __init__(self, llm_manager: AbstractLLMManager, model_for_summarizer: str = SUMMARIZATION_MODEL_DEFAULT,
                 model_for_token_limit: str = GENERATION_MODEL_DEFAULT, max_tokens_for_token_limit: int = MAX_TOKENS_DEFAULT,
                 code_or_exceeds_limit_only: bool = True, nl_base_prompt: SupportedPrompts = SupportedPrompts.NL_SUMMARY,
                 code_base_prompt: SupportedPrompts = SupportedPrompts.CODE_SUMMARY):
        """
        Initializes a summarizer for a specific model
        :param model_for_summarizer: path of the model that should be used for summarization
        :param model_for_token_limit: name of the model that should be used to evaluate token_limit
        :param args_for_summarizer_model: any additional args to use for summarization
        :param max_tokens_for_token_limit: the max number of tokens that the model can return as the completion
        :param code_or_exceeds_limit_only: if True, only performs summarization for text that exceeds the token limit or for code
        :param nl_base_prompt: The default prompt to use for summarization.
        :param code_base_prompt: The default summarization prompt to use for code.
        """
        self.llm_manager = llm_manager
        self.model_for_summarizer = model_for_summarizer
        self.model_for_token_limit = model_for_token_limit
        self.token_limit = TokenLimitCalculator.calculate_token_limit(self.model_for_token_limit, max_tokens_for_token_limit)
        self.args_for_summarizer_model = llm_manager.llm_args
        self.code_or_above_limit_only = code_or_exceeds_limit_only
        self.prompt_args = llm_manager.prompt_args
        self.code_prompt_creator = GenerationPromptCreator(
            prompt_args=self.prompt_args,
            base_prompt=code_base_prompt)
        self.nl_prompt_creator = GenerationPromptCreator(
            prompt_args=self.prompt_args,
            base_prompt=nl_base_prompt)

    def summarize(self, content: str, chunker_type: SupportedChunker = SupportedChunker.NL, id_: str = None) -> str:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param content: Content to summarize
        :param chunker_type: The supported chunker to use
        :param id_: The id associated with the content
        :return: The summarization
        """
        id_ = '' if not id_ else id_
        chunker = chunker_type.value(self.model_for_token_limit, token_limit=self.token_limit)
        assert content is not None, "No content to summarize."
        chunks = chunker.chunk(content=content, id_=id_)
        if self.code_or_above_limit_only and len(chunks) <= 1 and chunker_type == SupportedChunker.NL:
            return content  # skip summarizing content below token limit unless code
        prompt_creator = self.code_prompt_creator if chunker_type else self.nl_prompt_creator
        summarizations = self._summarize_chunks(self.llm_manager, prompt_creator, chunks, self.model_for_summarizer)
        return os.linesep.join(summarizations)

    def summarize_dataframe(self, df: pd.DataFrame, col2summarize: str, chunker_type=SupportedChunker.NL):
        """
        Summarizes the information in a dataframe in a given column
        :param df: The dataframe to summarize
        :param col2summarize: The name of the column in the dataframe to summarize
        :param chunker_type: The type of chunker to use
        :return: The dataframe with the contents in the given column summarized
        """
        loading_bar = tqdm(total=len(df), desc="Summarizing dataframe.")

        def summarize_item(item: str):
            summary = self.summarize(content=item, chunker_type=chunker_type)
            loading_bar.update()
            return summary

        df[col2summarize] = df[col2summarize].apply(summarize_item)
        return df

    def exceeds_token_limit(self, content: str) -> bool:
        """
        Determines if the given content exceeds the token limit
        :param content: The content
        :return: True if the content exceeds the token limit else False
        """
        return TokenLimitCalculator.estimate_num_tokens(content, self.model_for_summarizer) > self.token_limit

    @staticmethod
    def _summarize_chunks(llm_manager: AbstractLLMManager, prompt_creator: AbstractPromptCreator, chunks: List[str],
                          model_path: str) -> \
            List[str]:
        """
        Summarizes all chunks using a given OpenAI model.
        :param llm_manager: The utility file containing API to AI library.
        :param prompt_creator: The creator responsible for creating summarization prompts.
        :param model_path: The model to use for summarizations
        :param chunks: The chunks of text to summarize
        :return: The summaries of all chunks
        """
        prompts = [prompt_creator.create(target_content=chunk, source_content=EMPTY_STRING)[PromptKeys.PROMPT.value] for chunk in
                   chunks]
        res: GenerationResponse = llm_manager.make_completion_request(trainer_task=TrainerTask.PREDICT,
                                                                      completion_type=LLMCompletionType.GENERATION,
                                                                      model=model_path, prompt=prompts)
        return [r.strip() for r in res.batch_responses] if res else [EMPTY_STRING]
