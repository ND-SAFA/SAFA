from typing import Dict

from data.hub.abstract_hub_id import AbstractDatasetDescriptor
from util.override import overrides


class DroneFullDescriptor(AbstractDatasetDescriptor):
    """
    Describes the DroneResponse project reader.
    """

    @overrides(AbstractDatasetDescriptor)
    def get_url(self) -> str:
        """
        :return: Returns URL to DroneResponse on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/Drone.zip"

    @overrides(AbstractDatasetDescriptor)
    def get_definition(self) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "Requirements": {
                    "path": "Originals/Definitions/requirements.csv",
                    "cols": "artifacts"
                },
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
                "reqs2DDMatrix.csv": {
                    "source": "Requirements",
                    "target": "Design Definitions",
                    "path": "Originals/TraceMatrices/reqs2DDmatrix.txt",
                    "cols": "traces",
                    "params": {
                        "sep": " "
                    }
                },
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
                "allowed_orphans": 341,
                "allowed_missing_sources": 98,
                "allowed_missing_targets": 74
            }
        }
