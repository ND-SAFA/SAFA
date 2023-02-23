from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractHubId
from data.hub.hub_ids.iceory.abstract_iceoryx_hub_id import IceoryxHubId
from util.override import overrides


class IceoryxCommits(IceoryxHubId):
    """
    Identifier iceoryx open source project.
    """

    @staticmethod
    def get_stage_name() -> str:
        """
        :return: Returns the name of the eval data file.
        """
        return "commits"

    @classmethod
    @overrides(AbstractHubId)
    def get_definition(cls) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "Commit": {
                    "path": "commit.csv"
                },
                "Diff": {
                    "path": "diff.csv"
                }
            },
            "traces": {
                "commit2commit_diff": {
                    "source": "Commit",
                    "target": "Diff",
                    "path": "commit2diff.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 0,
                "allowed_missing_sources": 0,
                "allowed_missing_targets": 0
            }
        }
