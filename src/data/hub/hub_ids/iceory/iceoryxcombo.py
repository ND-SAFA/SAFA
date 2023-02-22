from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractHubId
from data.hub.hub_ids.iceory.abstract_iceoryx_hub_id import IceoryxHubId
from util.override import overrides


class IceoryxCombo(IceoryxHubId):
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
                "Commit Diff": {
                    "path": "commit_diff.csv"
                },
                "Code": {
                    "path": "code.csv"
                }
            },
            "traces": {
                "commit_diff2issue": {
                    "source": "Commit Diff",
                    "target": "Issue",
                    "path": "commit_diff2issue.csv"
                },
                "code2code": {
                    "source": "Code",
                    "target": "Code",
                    "path": "code2code.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 523,
                "allowed_missing_targets": 2
            }
        }
