from typing import List

from tgen.common.objects.artifact import Artifact
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition


def create_api_dataset(artifacts: List[Artifact], project_summary: str = None) -> PromptDatasetCreator:
    """
    Creates a prompt dataset containing trace dataset entities.
    :param artifacts: The artifacts of the dataset.
    :param project_summary: Optional project summary to include in the dataset.
    :return: Prompt dataset.
    """
    api_definition = ApiDefinition(artifacts=artifacts)
    api_project_reader = ApiProjectReader(api_definition=api_definition)
    trace_dataset_creator = TraceDatasetCreator(project_reader=api_project_reader)
    dataset = PromptDatasetCreator(trace_dataset_creator=trace_dataset_creator, project_summary=project_summary)
    return dataset
