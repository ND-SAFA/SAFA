import json
from typing import Dict, Type

from common_resources.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from common_resources.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from common_resources.data.summarizer.artifacts_summarizer import ArtifactsSummarizer
from common_resources.data.summarizer.summary import Summary
from common_resources.data.tdatasets.idataset import iDataset
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from common_resources.tools.constants.symbol_constants import EMPTY_STRING
from common_resources.tools.util.json_util import JsonUtil
from common_resources.tools.util.param_specs import ParamSpecs
from common_resources.tools.util.reflection_util import ReflectionUtil


class SerializedDatasetCreator(AbstractDatasetCreator[PromptDataset]):
    """
    Responsible for creating PromptDataset from a json serializable dictionary.
    """

    def __init__(self, serialized_dataset: Dict = None, project_path: str = EMPTY_STRING,
                 summarizer: ArtifactsSummarizer = None, ensure_code_is_summarized: bool = False):
        """
        Initializes creator with dataset as serializable dictionary.
        :param serialized_dataset: Dataset as serializable dictionary mapping param name to serialized value.
        :param project_path: Path to the saved serializable dataset.
        :param summarizer: Summarizer used to summarize artifact content.
        :param ensure_code_is_summarized: Verifies that code is summarized and summarizes code that's not.
        """
        super().__init__()
        self.project_path = project_path
        if self.project_path:
            serialized_dataset = JsonUtil.read_json_file(self.project_path)
        assert serialized_dataset, "Must provide dataset as serializable dictionary or a path to read it from."
        self.serialized_dataset = serialized_dataset
        self.ensure_code_is_summarized = ensure_code_is_summarized
        self.summarizer = summarizer

    def create(self) -> PromptDataset:
        """
        Creates TraceDataset with links.
        :return: TraceDataset.
        """
        dataset = self._create_from_json_dict(self.serialized_dataset, PromptDataset)
        if self.ensure_code_is_summarized:
            dataset = self._conditionally_summarize_dataset(dataset)
        return dataset

    def _create_from_json_dict(self, serialized_dataset: Dict,
                               dataset_type: Type[PromptDataset | TraceDataset]) -> PromptDataset | TraceDataset:
        """
        Creates the dataset from its params stored in a json serializable dictionary.
        :param serialized_dataset: The dataset in its serialized form.
        :param dataset_type: The type of dataset being made.
        :return: The initialized dataset.
        """
        param_spec = ParamSpecs.create_from_method(dataset_type.__init__)
        params = {}
        for name, expected_type in param_spec.param_types.items():
            value = serialized_dataset.get(name, None)
            if value is None:
                continue
            if ReflectionUtil.is_type(AbstractProjectDataFrame, expected_type, name, print_on_error=False, reversible=True):
                value = ReflectionUtil.get_base_class_type(expected_type)(value)
            elif ReflectionUtil.is_type(Summary, expected_type, name, print_on_error=False, reversible=True):
                value = Summary.from_string(value)
            elif ReflectionUtil.is_type(iDataset, expected_type, name, print_on_error=False, reversible=True):
                new_dataset_type: Type[PromptDataset | TraceDataset] = ReflectionUtil.get_base_class_type(expected_type)
                value = self._create_from_json_dict(value, new_dataset_type)
            else:
                value = json.loads(value)
            params[name] = value
        return dataset_type(**params)

    def _conditionally_summarize_dataset(self, dataset: PromptDataset) -> PromptDataset:
        """
        Summarizes any code files that are not summarized
        :param dataset: The original dataset (possible without summaries)
        :return: The summarized dataset
        """
        if dataset.artifact_df is not None and not dataset.artifact_df.is_summarized(code_or_above_limit_only=True):
            summarizer = ArtifactsSummarizer(summarize_code_only=True,
                                             project_summary=dataset.project_summary)
            dataset.artifact_df.summarize_content(summarizer)  # summarize any artifacts that were not in existing summaries
        return dataset

    def get_project_path(self) -> str:
        """
        Returns the project path if provided.
        :return: The project path.
        """
        project_path = self.project_path if self.project_path else EMPTY_STRING
        return project_path

    def get_name(self) -> str:
        """
        Gets the name of the prompt dataset based on given params
        :return: The name of the prompt dataset
        """
        if self.project_path:
            return self.project_path
        return EMPTY_STRING
