from abc import ABC, abstractmethod
from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId
from util.override import overrides


class IceoryxHubId(AbstractHubId, ABC):
    """
    Identifier iceoryx open source project.
    """

    @staticmethod
    @abstractmethod
    def get_zip_name() -> str:
        """
        :return: Returns the name of the zip file.
        """

    @classmethod
    @overrides(AbstractHubId)
    def get_url(cls) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/iceoryx/code.zip"

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
