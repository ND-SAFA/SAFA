from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractHubId
from data.hub.hub_ids.iceory.abstract_iceoryx_hub_id import IceoryxHubId
from util.override import overrides


class IceoryxCode(IceoryxHubId):
    """
    Identifier iceoryx open source project.
    """

    @staticmethod
    def get_stage_name() -> str:
        """
        :return: Returns the name of the eval data file.
        """
        return "code"

    @classmethod
    @overrides(AbstractHubId)
    def get_definition(cls) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "Code": {
                    "path": "code.csv"
                }
            },
            "traces": {
                "code2issue": {
                    "source": "Code",
                    "target": "Code",
                    "path": "code2code.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 640,
                "allowed_missing_sources": 8347,
                "allowed_missing_targets": 5
            }
        }
