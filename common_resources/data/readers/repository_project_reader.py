from common_resources.data.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from common_resources.data.readers.definitions.repository_project_definition import RepositoryProjectDefinition
from common_resources.data.readers.structured_project_reader import StructuredProjectReader


class RepositoryProjectReader(StructuredProjectReader):
    """
    Overrides structured project to return repository project definition.
    """

    def get_definition_reader(self) -> AbstractProjectDefinition:
        """
        :return: Returns repository project definition.
        """
        return RepositoryProjectDefinition()
