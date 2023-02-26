import os
from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId
from data.hub.hub_ids.multi_task_hub_id import MultiTaskHubId
from data.keys.structure_keys import StructuredKeys
from data.readers.definitions.structure_project_definition import StructureProjectDefinition
from util.override import overrides


class DronePLHubId(MultiTaskHubId):
    """
    Describes the DroneResponse project reader.
    """

    def __init__(self, task: str, stage: str):
        """
        Loads stage of Drone programming language task.
        :param stage: Either train, val, or eval
        """
        super().__init__(task, stage)

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to DroneResponse on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/drone_pl.zip"

    def get_definition_path(self, data_dir: str) -> str:
        """
        Returns path to stage definition file.
        :param data_dir: The base project path containing all stages.
        :return: Path to stage definition file.
        """
        return os.path.join(data_dir, self.task, self.stage, StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)

    def get_task_instruction_map(self) -> Dict:
        """
        Returns instructions for constructing task definition from base definition.
        :return: Task instructions.
        """
        return {
            "pl": {
                StructuredKeys.ARTIFACTS: ["Design Definitions", "Code"],
                StructuredKeys.TRACES: ["dd2codematrix"],
                StructuredKeys.OVERRIDES: {}
            }
        }

    @overrides(MultiTaskHubId)
    def get_base_definition(self) -> Dict:
        """
        :return: Returns the definition of the programming language tracing task.
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
                "dd2codematrix": {
                    "source": "Design Definitions",
                    "target": "Code",
                    "path": "Originals/TraceMatrices/dd2codematrix.txt",
                    "cols": "traces",
                    "params": {
                        "sep": " "
                    }
                },
                "reqs2DDMatrix": {
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
                "allowed_orphans": 341,
                "allowed_missing_sources": 0,
                "allowed_missing_targets": 0
            }
        }
