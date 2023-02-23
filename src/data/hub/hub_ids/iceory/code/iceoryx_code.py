from abc import ABC
from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractHubId
from data.hub.hub_ids.iceory.abstract_iceoryx_hub_id import IceoryxHubId
from util.override import overrides


class IceoryxCode(IceoryxHubId, ABC):
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
                "Code": {
                    "path": "Code.csv"
                },
                "Issue": {
                    "path": "Issue.csv"
                }
            },
            "traces": {
                "issue2code": {
                    "source": "Issue",
                    "target": "Code",
                    "path": "Issue2Code.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 640,
                "allowed_missing_sources": 6,
                "allowed_missing_targets": 8346
            }
        }
