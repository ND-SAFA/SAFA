from abc import ABC, abstractmethod
from typing import Dict

from gen_common.infra.base_object import BaseObject


class AbstractProjectDefinition(BaseObject, ABC):
    """
    Defines interface for reading a project definition file.
    """

    @staticmethod
    @abstractmethod
    def read_project_definition(project_path: str) -> Dict:
        """
        Reads project definition.
        :param project_path: Path to project.
        :return: Project definition in the structure project format.
        """
