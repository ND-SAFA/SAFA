from data.datasets.creators.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from data.datasets.creators.readers.definitions.repository_project_definition import RepositoryProjectDefinition
from data.datasets.creators.readers.structured_project_reader import StructuredProjectReader


class RepositoryProjectReader(StructuredProjectReader):
    """
    Overrides structured project to return repository project definition.
    """

    def _get_definition_reader(self) -> AbstractProjectDefinition:
        """
        :return: Returns repository project definition.
        """
        return RepositoryProjectDefinition()
