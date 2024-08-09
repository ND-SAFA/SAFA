from typing import Any, Dict, Set

from common_resources.tools.constants.model_constants import MAX_NL_SIZE_BEFORE_SUMMARIZATION
from common_resources.tools.util.dataclass_util import DataclassUtil
from common_resources.tools.util.reflection_util import ReflectionUtil
from common_resources.llm.tokens.token_calculator import TokenCalculator


class SummarizerUtil:

    @staticmethod
    def get_params_for_artifact_summarizer(summarizer_args: "SummarizerArgs") -> Dict[str, Any]:
        """
        Extracts the params needed for the artifact summarizer from all summarizer args
        :param summarizer_args: All arguments to the summarizer
        :return: The params needed for the artifact summarizer
        """
        from common_resources.data.summarizer.artifacts_summarizer import ArtifactsSummarizer
        params = ReflectionUtil.get_constructor_params(ArtifactsSummarizer, DataclassUtil.convert_to_dict(summarizer_args))
        return params

    @staticmethod
    def needs_project_summary(existing_summary: "Summary", summarizer_args: "SummarizerArgs") -> bool:
        """
        Determines if the dataset needs a project summary to be generated
        :param existing_summary: The initial project summary given to the summarizer
        :param summarizer_args: All arguments to the summarizer
        :return: True if the dataset needs a project summary to be generated, else False
        """
        return len(SummarizerUtil.missing_project_summary_sections(existing_summary, summarizer_args)) != 0

    @staticmethod
    def missing_project_summary_sections(existing_summary: "Summary", summarizer_args: "SummarizerArgs") -> Set[str]:
        """
        Determines the project summary sections that are not present in the dataset
         :param existing_summary: The initial project summary given to the summarizer
        :param summarizer_args: All arguments to the summarizer
        :return: True if the dataset needs a project summary to be generated, else False
        """
        existing_sections = existing_summary.keys() if existing_summary else set()
        return set(summarizer_args.project_summary_sections).difference(existing_sections)

    @staticmethod
    def is_above_limit(content: str) -> bool:
        """
        Returns whether content is above the summarize token limit.
        :param content: The content of the summarizer to count.
        :return: Whether content is above limit.
        """
        n_tokens = TokenCalculator.estimate_num_tokens(content)
        return n_tokens > MAX_NL_SIZE_BEFORE_SUMMARIZATION
