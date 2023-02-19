from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractHubId
from util.override import overrides


class ICEORYXPLHubId(AbstractHubId):
    """
    Identifier iceoryx open source project.
    """

    @classmethod
    @overrides(AbstractHubId)
    def get_url(cls) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing defefinition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/iceoryx_pl.zip"

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
                "Commit": {
                    "path": "commit.csv"
                }
            },
            "traces": {
                "Pull2Issue": {
                    "source": "Pull",
                    "target": "Issue",
                    "path": "pull2issue.csv"
                },
                "commit2issue": {
                    "source": "Commit",
                    "target": "Issue",
                    "path": "commit2issue.csv"
                }
            }
        }
