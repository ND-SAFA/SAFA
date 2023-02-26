from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId
from util.override import overrides


class CM1HubId(AbstractHubId):
    """
    Describes the CM1 project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to CM1 on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/CM1.zip"

    def get_definition(self) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "High Level Requirements": {
                    "path": "CM1-sourceArtifacts.xml",
                    "cols": "CM1-artifacts"
                },
                "Low Level Requirements": {
                    "path": "CM1-targetArtifacts.xml",
                    "cols": "CM1-artifacts"
                }
            },
            "traces": {
                "high2low.csv": {
                    "source": "High Level Requirements",
                    "target": "Low Level Requirements",
                    "path": "CM1-answerSet.xml",
                    "cols": "CM1-traces"
                }
            },
            "conversions": {
                "CM1-artifacts": {
                    "id": "id",
                    "content": "content"
                },
                "CM1-traces": {
                    "source_artifact_id": "source",
                    "target_artifact_id": "target"
                }
            },
            "overrides": {
                "allowed_orphans": 26
            }
        }
