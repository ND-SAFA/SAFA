from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractDatasetDescriptor
from util.override import overrides


class TrainControllerDescriptor(AbstractDatasetDescriptor):
    """
    Describes the TrainController project reader.
    """

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_url(cls) -> str:
        """
        :return: Returns URL to TrainController on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/TrainController.zip"

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_definition(cls) -> Dict:
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
                "ALLOW_MISSING_SOURCE": True,
                "ALLOW_MISSING_TARGET": True
            }
        }
