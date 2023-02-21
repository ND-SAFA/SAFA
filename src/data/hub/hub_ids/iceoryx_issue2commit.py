from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractHubId
from util.override import overrides


class IceoryxIssue2CommitDiff(AbstractHubId):
    """
    Identifier iceoryx open source project.
    """

    @classmethod
    @overrides(AbstractHubId)
    def get_url(cls) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing defefinition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/iceoryx.zip"

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
                "Pull": {
                    "path": "pull.csv"
                },
                "Commit Diff": {
                    "path": "commit_diff.csv"
                }
            },
            "traces": {
                "commit_diff2issue": {
                    "source": "Commit Diff",
                    "target": "Issue",
                    "path": "commit_diff2issue.csv"
                }
                , "commit_diff2pull": {
                    "source": "Commit Diff",
                    "target": "Pull",
                    "path": "commit_diff2pull.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 252,
                "allowed_missing_sources": 1519,
                "allowed_missing_targets": 2
            }
        }
