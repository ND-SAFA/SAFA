from typing import Dict, Any

from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs


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
    def needs_project_summary(dataset: PromptDataset, summarizer_args: SummarizerArgs) -> bool:
        """
        Determines if the dataset needs a project summary to be generated
        :param dataset: The initial dataset given to the summarizer
        :param summarizer_args: All arguments to the summarizer
        :return: True if the dataset needs a project summary to be generated, else False
        """
        if dataset.project_summary:
            return len(set(summarizer_args.project_summary_sections).difference(dataset.project_summary.keys())) != 0
        return True
