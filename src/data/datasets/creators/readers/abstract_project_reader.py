from abc import ABC, abstractmethod
from typing import Tuple

import pandas as pd


class AbstractProjectReader(ABC):
    """
    Defines interface for objects responsible for reading projects.
    """

    @abstractmethod
    def read_project(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Reads artifact and trace links from files.
        :return: Returns data frames containing artifacts, trace links, and layer mappings.
        """

    @staticmethod
    def should_generate_negative_links() -> bool:
        """
        :return: Returns whether negative links should be implied by comparing artifacts.
        """
        return True
