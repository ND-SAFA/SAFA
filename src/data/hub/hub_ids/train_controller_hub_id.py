from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId
from util.override import overrides


class TrainControllerHubId(AbstractHubId):
    """
    Describes the TrainController project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to TrainController on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/TrainController.zip"

    def get_definition(self) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "SRS": {
                    "path": "Originals/Source_1/SRS.csv",
                    "cols": "artifacts"
                },
                "SDD": {
                    "path": "Originals/Source_1/SDD.csv",
                    "cols": "artifacts"
                },
                "SSRS": {
                    "path": "Originals/Source_1/SSRS.csv",
                    "cols": "artifacts"
                }
            },
            "traces": {
                "SDD2SRS": {
                    "source": "SDD",
                    "target": "SRS",
                    "path": "Originals/Source_1/SDD2SRS.txt",
                    "params": {
                        "sep": " "
                    }
                },
                "SSRS2SDD": {
                    "source": "SSRS",
                    "target": "SDD",
                    "path": "Originals/Source_1/SSRS2SDD.txt",
                    "params": {
                        "sep": " "
                    }
                }
            },
            "conversions": {
                "artifacts": {
                    "id": "id",
                    "text": "content"
                }
            },
            "overrides": {
                "allowed_orphans": 150,
                "allowed_missing_sources": 16,
                "allowed_missing_targets": 23
            }
        }
