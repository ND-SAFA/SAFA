import os
from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId
from data.readers.definitions.structure_project_definition import StructureProjectDefinition
from util.override import overrides


class DronePLHubId(AbstractHubId):
    """
    Describes the DroneResponse project reader.
    """

    def __init__(self, stage: str):
        """
        Loads stage of Drone programming language task.
        :param stage: Either train, val, or eval
        """
        self.stage = stage

    def get_definition_path(self, data_dir: str) -> str:
        """
        Returns path to stage definition file.
        :param data_dir: The base project path containing all stages.
        :return: Path to stage definition file.
        """
        return os.path.join(data_dir, self.stage, StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to DroneResponse on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/drone_pl.zip"

    @overrides(AbstractHubId)
    def get_definition(self) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {

                "Design Definitions": {
                    "path": "../Originals/Definitions/designdefinitions.csv",
                    "cols": "artifacts"
                },
                "Code": {
                    "path": "../Originals/Definitions/flatCode",
                    "cols": "artifacts"
                }
            },
            "traces": {
                "dd2codematrix.csv": {
                    "source": "Design Definitions",
                    "target": "Code",
                    "path": "../Originals/TraceMatrices/dd2codematrix.txt",
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
                "allowed_missing_sources": 4,
                "allowed_missing_targets": 17
            }
        }
