from typing import Dict, Any, Set

from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summary import Summary


class SummarizerUtil:

    @staticmethod
    def get_params_for_artifact_summarizer(summarizer_args: SummarizerArgs) -> Dict[str, Any]:
        """
        Extracts the params needed for the artifact summarizer from all summarizer args
        :param summarizer_args: All arguments to the summarizer
        :return: The params needed for the artifact summarizer
        """
        params = ReflectionUtil.get_constructor_params(ArtifactsSummarizer, DataclassUtil.convert_to_dict(summarizer_args))
        return params

    @staticmethod
    def needs_project_summary(existing_summary: Summary, summarizer_args: SummarizerArgs) -> bool:
        """
        Determines if the dataset needs a project summary to be generated
        :param existing_summary: The initial project summary given to the summarizer
        :param summarizer_args: All arguments to the summarizer
        :return: True if the dataset needs a project summary to be generated, else False
        """
        return len(SummarizerUtil.missing_project_summary_sections(existing_summary, summarizer_args)) != 0

    @staticmethod
    def missing_project_summary_sections(existing_summary: Summary, summarizer_args: SummarizerArgs) -> Set[str]:
        """
        Determines the project summary sections that are not present in the dataset
         :param existing_summary: The initial project summary given to the summarizer
        :param summarizer_args: All arguments to the summarizer
        :return: True if the dataset needs a project summary to be generated, else False
        """
        existing_sections = existing_summary.keys() if existing_summary else set()
        return set(summarizer_args.project_summary_sections).difference(existing_sections)

