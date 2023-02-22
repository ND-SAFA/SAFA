from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractHubId
from data.hub.hub_ids.iceory.abstract_iceoryx_hub_id import IceoryxHubId
from util.override import overrides


class IceoryxCode2Issue(IceoryxHubId):
    """
    Identifier iceoryx open source project.
    """

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
                    "source": "Code",
                    "target": "Issue",
                    "path": "code2issue.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 506,
                "allowed_missing_sources": 8347,
                "allowed_missing_targets": 5
            }
        }
