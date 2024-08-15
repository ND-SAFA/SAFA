import uuid
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pandas as pd
from common_resources.data.keys.prompt_keys import PromptKeys
from common_resources.data.keys.structure_keys import ArtifactKeys, StructuredKeys
from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.llm.llm_responses import GenerationResponse
from common_resources.llm.llm_task import LLMCompletionType
from common_resources.llm.prompts.context_prompt import ContextPrompt
from common_resources.llm.prompts.prompt import Prompt
from common_resources.llm.prompts.prompt_args import PromptArgs
from common_resources.llm.prompts.prompt_builder import PromptBuilder
from common_resources.tools.constants.default_model_managers import get_efficient_default_llm_manager
from common_resources.tools.constants.symbol_constants import EMPTY_STRING
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.llm_response_util import LLMResponseUtil
from common_resources.tools.util.unique_id_manager import DeterministicUniqueIDManager

from tgen.common.constants.project_summary_constants import PS_ENTITIES_TITLE
from tgen.models.tokens.token_calculator import TokenCalculator
from tgen.prompts.supported_prompts.artifact_summary_prompts import CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX, \
    NL_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX
from tgen.summarizer.artifact.artifact_summary_types import ArtifactSummaryTypes
from tgen.summarizer.summarizer_util import SummarizerUtil
from tgen.summarizer.summary import Summary


class ArtifactsSummarizer(BaseObject):
    """

    Summarizes bodies of code or text to create shorter, more succinct input for model
    """
    SUMMARY_TAG = "summary"

    def __init__(self, llm_manager_for_artifact_summaries: AbstractLLMManager = None,
                 summarize_code_only: bool = True,
                 project_summary: Summary = None,
                 summary_order: Dict[str, int] = None,
                 context_mapping: Dict[str, List[EnumDict]] = None,
                 code_summary_type: ArtifactSummaryTypes = ArtifactSummaryTypes.CODE_BASE,
                 nl_summary_type: ArtifactSummaryTypes = ArtifactSummaryTypes.NL_BASE,
                 export_dir: str = None,
                 summarizer_id: str = str(uuid.uuid4())):
        """
        Initializes a summarizer for a specific model
        :param llm_manager_for_artifact_summaries: LLM manager used for the individual artifact summaries.
        :param summarize_code_only: If True, only summarizes code content
        :param project_summary: Default project summary to use.
        :param summary_order: If provided, will summarize the artifacts in the provided order (artifact id -> order #).
        :param context_mapping: Maps an artifact to the necessary artifacts to include as context.
        :param code_summary_type: The default prompt to use for summarization of code.
        :param nl_summary_type: The default prompt to use for summarization of natural language.
        :param export_dir: If provided, will save the responses there.
        :param summarizer_id: Id assigned to this summarizer.
        """
        self.save_responses_path = export_dir
        self.llm_manager = llm_manager_for_artifact_summaries if llm_manager_for_artifact_summaries \
            else get_efficient_default_llm_manager()
        self.args_for_summarizer_model = self.llm_manager.llm_args
        self.code_or_above_limit_only = summarize_code_only
        self.summary_order = summary_order
        self.context_mapping = context_mapping

        # Setup prompts
        self.prompt_args = self.llm_manager.prompt_args
        self.project_summary = project_summary
        self.code_prompt_builder, self.nl_prompt_builder = self._create_prompt_builders(code_summary_type,
                                                                                        nl_summary_type,
                                                                                        self.project_summary,
                                                                                        self.context_mapping)

        self.uuid_manager = DeterministicUniqueIDManager(summarizer_id)

    def summarize_bulk(self, bodies: List[str], ids: List[str] = None, use_content_if_unsummarized: bool = True) -> List[str]:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param bodies: List of content to summarize
        :param ids: The list of filenames to use to determine if the bodies are code or not
        :param use_content_if_unsummarized: If True, uses the artifacts orig content instead of a summary if it is not being summarized
        :return: The summarization
        """
        logger.info(f"Received {len(bodies)} artifacts to summarize.")
        summary_order = self.summary_order if self.summary_order else {}
        ids = [EMPTY_STRING for _ in bodies] if not ids else ids
        assert len(bodies) == len(ids), "length of bodies, summary types and ids must all match"
        order2indices = {}
        indices2summarize = set()
        for i, artifact_info in enumerate(zip(bodies, ids)):
            content, a_id = artifact_info
            if self.should_summarize(a_id=a_id, a_body=content):
                order = summary_order.get(a_id, 0)
                DictUtil.set_or_append_item(order2indices, order, i)
                indices2summarize.add(i)
        logger.info(f"Selected {len(indices2summarize)} artifacts to summarize in {len(order2indices)} batch(es).")

        summarized_content = bodies
        for order, indices in dict(sorted(order2indices.items())).items():
            logger.info(f"Summarizing {len(indices)} artifacts in batch {order}.")
            summary_prompts = [self._create_prompt(bodies[i], ids[i]) for i in indices]
            summarized_content = self._summarize_selective(contents=summarized_content,
                                                           indices2summarize=indices,
                                                           prompts_for_summaries=summary_prompts,
                                                           use_content_if_unsummarized=True)
            self._update_context_mapping_with_summaries(summarized_content, ids)
        if not use_content_if_unsummarized:
            summarized_content = [(summary if i in indices2summarize else None) for i, summary in enumerate(summarized_content)]
        return summarized_content

    def summarize_single(self, content: str, a_id: str = EMPTY_STRING) -> str:
        """
        Summarizes a file or body of text  to create shorter, more succinct input for model
        :param content: Content to summarize
        :param a_id: The filename to use to determine if content is code or not
        :return: The summarization
        """
        if not self.should_summarize(a_id, a_body=content):
            return content
        prompt = self._create_prompt(content, a_id)
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

    def should_summarize(self, a_id: str, a_body: str) -> bool:
        """
        True if the artifact should be summarized else False.
        :param a_id: The artifact id.
        :param a_body: The body of the artifact to summarize.
        :return: True if the artifact should be summarized else False.
        """
        if self.code_or_above_limit_only:
            if FileUtil.is_code(a_id):
                return True
            if SummarizerUtil.is_above_limit(a_body):
                return True
            return False  # skip summarizing content below token limit unless code
        else:
            return True

    def _update_context_mapping_with_summaries(self, summarized_content: List[str], ids: List[str]) -> None:
        """
        Updates the context mapping to use the new summaries.
        :param summarized_content: The recently summarized content.
        :param ids: Ids corresponding to summaries.
        :return: None (updates reference).
        """
        if not self.context_mapping:
            return
        id2summary = {a_id: summary for a_id, summary in zip(ids, summarized_content)}
        for a_id, related_artifacts in self.context_mapping.items():
            for artifact in related_artifacts:
                summary = id2summary.get(artifact[ArtifactKeys.ID], EMPTY_STRING)
                artifact[ArtifactKeys.SUMMARY] = summary

    def _summarize(self, llm_manager: AbstractLLMManager, prompts: Union[List[str], str]) -> List[str]:
        """
        Summarizes all artifacts using a given model.
        :param llm_manager: The utility file containing API to AI library.
        :param prompts: The prompts used to summarize each artifact
        :return: The combined summaries of all artifacts
        """
        if not isinstance(prompts, List):
            prompts = [prompts]

        save_and_load_path = self._get_responses_save_and_load_path()
        reloaded = LLMResponseUtil.reload_responses(save_and_load_path)
        missing_generations = isinstance(reloaded, List) or reloaded is None

        if missing_generations:
            res: GenerationResponse = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                          prompt=prompts,
                                                                          original_responses=reloaded,
                                                                          raise_exception=not self.save_responses_path)
            LLMResponseUtil.save_responses(res, save_and_load_path)
            LLMResponseUtil.get_failed_responses(res, raise_exception=True)
        else:
            res = reloaded

        batch_responses = self._parse_responses(res)
        debugging = [p + r for p, r in zip(prompts, res.batch_responses)]

        self.uuid_manager.generate_new_id()
        return batch_responses

    def _parse_responses(self, res: GenerationResponse) -> List[str]:
        """
        Parses the summary responses.
        :param res: The response from the model to parse.
        :return: The parsed responses.
        """
        if res is None:
            parsed_responses = [EMPTY_STRING]
        else:
            parsed_responses = [self._parse_response(r) for r in res.batch_responses]
        return parsed_responses

    def _parse_response(self, response: str) -> str:
        """
        Parses each of the responses using either the code or nl prompt builder.
        :param response: The LLM response.
        :return: The parsed response.
        """
        parsed_response = self.code_prompt_builder.parse_responses(response)
        summary = LLMResponseUtil.get_non_empty_responses(parsed_response)
        if not summary:
            parsed_response = self.nl_prompt_builder.parse_responses(response)
            summary = LLMResponseUtil.get_non_empty_responses(parsed_response)
        summary = summary if summary else response
        return summary.strip()

    def _create_prompt(self, content: str, a_id: str = EMPTY_STRING) -> Optional[str]:
        """
        Prepares for summarization by creating the necessary prompts for the artifact
        :param content: Content to summarize
        :param a_id: The id of the artifact to determine if the content is code or not
        :return: The list of prompts to use for summarization
        """
        prompt_builder = self.code_prompt_builder if FileUtil.is_code(a_id) else self.nl_prompt_builder
        prompt = prompt_builder.build(model_format_args=self.llm_manager.prompt_args,
                                      artifact={StructuredKeys.Artifact.CONTENT: content,
                                                StructuredKeys.Artifact.ID: a_id})[PromptKeys.PROMPT.value]
        if FileUtil.is_code(a_id):
            prompt = PromptBuilder.remove_format_for_model_from_prompt(prompt, self.llm_manager.prompt_args)
            prompt = TokenCalculator.truncate_to_fit_tokens(prompt, self.llm_manager.llm_args.model,
                                                            self.llm_manager.llm_args.get_max_tokens(),
                                                            is_code=True)
            prompt = PromptBuilder.format_prompt_for_model(prompt, self.llm_manager.prompt_args)
        return prompt

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

    def _get_responses_save_and_load_path(self) -> str:
        """
        Gets the save and load path for responses.
        :return: The save and load path for responses.
        """
        save_and_load_path = FileUtil.safely_join_paths(self.save_responses_path,
                                                        FileUtil.add_ext(f"art_sum_responses_{self.uuid_manager.get_uuid()}",
                                                                         FileUtil.YAML_EXT))
        return save_and_load_path

    @staticmethod
    def _create_prompt_builders(code_summary_type: ArtifactSummaryTypes, nl_summary_type: ArtifactSummaryTypes,
                                project_summary: Summary,
                                context_mapping: Dict[Any, List[EnumDict]]) -> Tuple[PromptBuilder, PromptBuilder]:
        """
        Creates the prompt builders for both code and nl summarizing.
        :param code_summary_type: Specifies the prompt to use for the code summary.
        :param nl_summary_type: Specifies the prompt to use for the NL summary.
        :param project_summary: If provided, the project summary will be added to the prompt.
        :param context_mapping: Maps an artifact to the necessary artifacts to include as context.
        :return: The code and nl prompt builder.
        """
        summary_prefixes = [CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX, NL_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX]
        project_summary_string = project_summary.to_string([PS_ENTITIES_TITLE]) if project_summary else EMPTY_STRING
        prompt_builders = []

        for i, a_type in enumerate([code_summary_type, nl_summary_type]):
            prompts = a_type.value
            if context_mapping:
                keywords = ["Functions", "Code"] if i == 0 else ["Artifacts", "Artifact to Summarize"]
                context_prompt = ContextPrompt(prompt_start="# Related {} to Improve Understanding of {}".format(*keywords),
                                               id_to_context_artifacts=context_mapping)
                prompts.insert(0, context_prompt)
            if project_summary_string:
                prompts.insert(0, summary_prefixes[i])
                prompts.insert(1, Prompt(project_summary_string, prompt_args=PromptArgs(allow_formatting=False)))
            prompt_builders.append(PromptBuilder(prompts=prompts))
        return prompt_builders[0], prompt_builders[1]
