from typing import Dict, List, Optional, Set, Union

import pandas as pd

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.project_summary_constants import PS_ENTITIES_TITLE
from tgen.common.util.base_object import BaseObject
from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.artifact_summary_prompts import CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX, \
    NL_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX
from tgen.summarizer.artifact.artifact_summary_types import ArtifactSummaryTypes
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary import Summary


class ArtifactsSummarizer(BaseObject):
    """

    Summarizes bodies of code or text to create shorter, more succinct input for model
    """
    SUMMARY_TAG = "summary"

    def __init__(self, summarizer_args: SummarizerArgs, project_summary: Summary = None,
                 nl_summary_type: ArtifactSummaryTypes = ArtifactSummaryTypes.NL_BASE):
        """
        Initializes a summarizer for a specific model
        :param summary_args: The args for the summary
        :param nl_summary_type: The default prompt to use for summarization.
        """
        self.llm_manager = summarizer_args.llm_manager_for_artifact_summaries
        self.args_for_summarizer_model = self.llm_manager.llm_args
        self.code_or_above_limit_only = summarizer_args.summarize_code_only
        self.prompt_args = self.llm_manager.prompt_args
        self.project_summary = project_summary
        code_prompts = summarizer_args.code_summary_type.value
        nl_prompts = nl_summary_type.value
        if self.project_summary:
            project_summary = self.project_summary.to_string([PS_ENTITIES_TITLE])

            nl_prompts.insert(0, NL_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX)
            nl_prompts.insert(1, Prompt(project_summary, allow_formatting=False))

            code_prompts.insert(0, CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX)
            code_prompts.insert(1, Prompt(project_summary, allow_formatting=False))
        self.code_prompt_builder = PromptBuilder(prompts=code_prompts)
        self.nl_prompt_builder = PromptBuilder(nl_prompts)

    def summarize_bulk(self, bodies: List[str], filenames: List[str] = None, use_content_if_unsummarized: bool = True) -> List[str]:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param bodies: List of content to summarize
        :param filenames: The list of filenames to use to determine if the bodies are code or not
        :param use_content_if_unsummarized: If True, uses the artifacts orig content instead of a summary if it is not being summarized
        :return: The summarization
        """
        logger.info(f"Received {len(bodies)} artifacts to summarize.")
        filenames = [EMPTY_STRING for _ in bodies] if not filenames else filenames
        assert len(bodies) == len(filenames), "length of bodies, summary types and ids must all match"
        summary_prompts = []
        indices2summarize = set()
        for i, artifact_info in enumerate(zip(bodies, filenames)):
            content, filename = artifact_info
            prompt = self._create_prompt(content, filename, self.code_or_above_limit_only)
            if prompt:
                summary_prompts.append(prompt)
                indices2summarize.add(i)
        logger.info(f"Selected {len(indices2summarize)} artifacts to summarize.")
        summarized_content = self._summarize_selective(contents=bodies,
                                                       indices2summarize=indices2summarize,
                                                       prompts_for_summaries=summary_prompts,
                                                       use_content_if_unsummarized=use_content_if_unsummarized)
        return summarized_content

    def summarize_single(self, content: str, filename: str = EMPTY_STRING) -> str:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param content: Content to summarize
        :param filename: The filename to use to determine if content is code or not
        :return: The summarization
        """
        prompt = self._create_prompt(content, filename, code_or_above_limit_only=self.code_or_above_limit_only)
        if not prompt:
            return content
        summary = self._summarize(self.llm_manager, prompt)
        assert len(summary) == 1, f"Expected single summary but received {len(summary)}."
        return summary.pop()

    def summarize_dataframe(self, df: pd.DataFrame, col2summarize: str, col4filename: str = None,
                            index_to_filename: Dict[str, ArtifactSummaryTypes] = None) -> List[str]:
        """
        Summarizes the information in a dataframe in a given column
        :param df: The dataframe to summarize
        :param col2summarize: The name of the column in the dataframe to summarize
        :param col4filename: The column to use for filenames to determine the type of summary
        :param index_to_filename: Dictionary mapping index to the summary to use for that row
        :return: The summaries for the column
        """
        ids = list(df.index)
        if index_to_filename:
            filenames = [index_to_filename[index] for index in ids]
        elif col4filename:
            use_id = col4filename == df.index.name
            filenames = ids if use_id else df[col4filename]
        else:
            filenames = [EMPTY_STRING for _ in ids]

        summaries = self.summarize_bulk(list(df[col2summarize]), filenames, use_content_if_unsummarized=False)
        return summaries

    @staticmethod
    def _summarize(llm_manager: AbstractLLMManager, prompts: Union[List[str], str]) -> List[str]:
        """
        Summarizes all artifacts using a given model.
        :param llm_manager: The utility file containing API to AI library.
        :param prompts: The prompts used to summarize each artifact
        :return: The combined summaries of all artifacts
        """
        if not isinstance(prompts, List):
            prompts = [prompts]
        res: GenerationResponse = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                      prompt=prompts)
        if res is None:
            batch_responses = [EMPTY_STRING]
        else:
            parsed_responses = [LLMResponseUtil.parse(r, ArtifactsSummarizer.SUMMARY_TAG, return_res_on_failure=True)[0] for r in
                                res.batch_responses]
            batch_responses = [r.strip() for r in parsed_responses]

        return batch_responses

    def _create_prompt(self, content: str, filename: str = EMPTY_STRING, code_or_above_limit_only: bool = None) -> Optional[str]:
        """
        Prepares for summarization by creating the necessary prompts for the artifact
        :param content: Content to summarize
        :param filename: The name of the file to determine if the content is code or not
        :param code_or_above_limit_only: Needed only if different from self.code_or_above_limit_only
        :return: The list of prompts to use for summarization
        """
        code_or_above_limit_only = self.code_or_above_limit_only if code_or_above_limit_only is None else code_or_above_limit_only
        assert content is not None, "No content to summarize."
        if code_or_above_limit_only and not FileUtil.is_code(filename):
            return  # skip summarizing content below token limit unless code
        prompt_builder = self.code_prompt_builder if FileUtil.is_code(filename) else self.nl_prompt_builder
        return prompt_builder.build(model_format_args=self.llm_manager.prompt_args,
                                    artifact={StructuredKeys.Artifact.CONTENT: content})[PromptKeys.PROMPT.value]

    def _summarize_selective(self, contents: List[str], indices2summarize: Set[int], prompts_for_summaries: List[str],
                             use_content_if_unsummarized: bool) -> List[str]:
        """
        Summarizes only the content whose index is in indices2summarize
        :param contents: Contents to summarize
        :param indices2summarize: Index of the content that should be summarized
        :param prompts_for_summaries: The prompts for summarization (corresponds to only the content selected for summarization)
        :param use_content_if_unsummarized: If True, uses the artifacts orig content instead of a summary if it is not being summarized
        :return: The summarization if summarized else the original content
        """
        summarized_contents = self._summarize(self.llm_manager, prompts_for_summaries)
        summaries_iter = iter(summarized_contents)
        summaries = []
        for index, content in enumerate(contents):
            default = content if use_content_if_unsummarized else None
            summary = next(summaries_iter) if index in indices2summarize else default
            summaries.append(summary)
        return summaries
