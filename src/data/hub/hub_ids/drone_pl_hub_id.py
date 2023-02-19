from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractHubId
from util.override import overrides


class DronePLHubId(AbstractHubId):
    """
    Describes the DroneResponse project reader.
    """

    @classmethod
    @overrides(AbstractHubId)
    def get_url(cls) -> str:
        """
        :return: Returns URL to DroneResponse on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/Drone.zip"

    @classmethod
    @overrides(AbstractHubId)
    def get_definition(cls) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "Design Definitions": {
                    "path": "Originals/Definitions/designdefinitions.csv",
                    "cols": "artifacts"
                },
                "Code": {
                    "path": "Originals/Definitions/flatCode",
                    "cols": "artifacts"
                }
            },
            "traces": {
                "dd2codematrix.csv": {
                    "source": "Design Definitions",
                    "target": "Code",
                    "path": "Originals/TraceMatrices/dd2codematrix.txt",
                    "cols": "traces",
                    "params": {
                        "sep": " "
                    }
                }
            },
            "conversions": {
                "artifacts": {
                    "id": "id",
                    "content": "content"
                },
                "traces": {
                    "source": "source",
                    "target": "target"
                }
            },
            "overrides": {
                "allowed_orphans": 362,
                "allowed_missing_sources": 98,
                "allowed_missing_targets": 74
            }
        }
