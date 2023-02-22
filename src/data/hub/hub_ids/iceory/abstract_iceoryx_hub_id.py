import os
from abc import ABC, abstractmethod
from typing import Dict, Type

from data.hub.abstract_dataset_descriptor import AbstractHubId
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.csv_project_reader import CsvProjectReader
from util.override import overrides


class IceoryxHubId(AbstractHubId, ABC):
    """
    Identifier iceoryx open source project.
    """

    @staticmethod
    @abstractmethod
    def get_file_name() -> str:
        """
        :return: Returns the file name of the dataset file to read.
        """
        pass

    @classmethod
    @overrides(AbstractHubId)
    def get_url(cls) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing definition file.
        """
        return os.path.expanduser("~/desktop/safa/datasets/test.zip")

    @classmethod
    def get_project_reader(cls) -> Type[AbstractProjectReader]:
        """
        :return: Returns reader for pre-determined splits.
        """

        def constructor(project_path: str, **kwargs):
            return CsvProjectReader(os.path.join(project_path, cls.get_file_name()), **kwargs)

        return constructor

    @classmethod
    @overrides(AbstractHubId)
    def get_definition(cls) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "Issue": {
                    "path": "issue.csv"
                },
                "Code": {
                    "path": "code.csv"
                }
            },
            "traces": {
                "code2issue": {
                    "source": "Issue",
                    "target": "Code",
                    "path": "issue2code.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 506,
                "allowed_missing_sources": 8347,
                "allowed_missing_targets": 5
            }
        }
