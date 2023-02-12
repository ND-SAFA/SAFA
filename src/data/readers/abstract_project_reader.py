from abc import ABC, abstractmethod
from typing import Dict, Tuple

import pandas as pd

from util.base_object import BaseObject


class AbstractProjectReader(BaseObject, ABC):
    """
    Defines interface for objects responsible for reading projects.
    """

    def __init__(self, overrides: dict = None):
        """
        Initialized project reader with overrides.
        :param overrides: The overrides to apply to project creator.
        """
        self.overrides = overrides if overrides else {}

    @abstractmethod
    def read_project(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Reads artifact and trace links from files.
        :return: Returns data frames containing artifacts, trace links, and layer mappings.
        """

    @abstractmethod
    def get_project_name(self) -> str:
        """
        :return:  Returns the name of the project being read.
        """

    @staticmethod
    def should_generate_negative_links() -> bool:
        """
        :return: Returns whether negative links should be implied by comparing artifacts.
        """
        return True

    def get_overrides(self) -> Dict:
        """
        Returns any properties that should be overriden. This is a commonly used to set rules like
        allowing missing source / target references in trace links.
        :return: Dictionary of parameter names to their new values to override.
        """
        return self.overrides
