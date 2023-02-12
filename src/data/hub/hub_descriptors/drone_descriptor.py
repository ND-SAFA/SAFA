from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractDatasetDescriptor
from util.override import overrides


class DroneDescriptor(AbstractDatasetDescriptor):
    """
    Describes the DroneResponse project reader.
    """

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_url(cls) -> str:
        """
        :return: Returns URL to DroneResponse on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/Drone.zip"

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_definition(cls) -> Dict:
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
                "dd2codematrix.csv": {
                    "source": "Design Definitions",
                    "target": "Code",
                    "path": "Originals/TraceMatrices/dd2codematrix.txt",
                    "cols": "traces",
                    "params": {
                        "sep": " "
                    }
                },
                "reqs2DDMatrix.csv": {
                    "source": "Requirements",
                    "target": "Design Definitions",
                    "path": "Originals/TraceMatrices/reqs2DDmatrix.txt",
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
                "allowed_missing_sources": 0,
                "allowed_missing_targets": 0
            }
        }
