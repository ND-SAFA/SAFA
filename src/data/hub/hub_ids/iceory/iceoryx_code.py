import os
from typing import Dict

from data.hub.hub_ids.iceory.abstract_iceoryx_hub_id import IceoryxHubId
from data.readers.definitions.structure_project_definition import StructureProjectDefinition


class IceoryxCode(IceoryxHubId):
    """
    Identifier iceoryx open source project.
    """

    def __init__(self, stage: str):
        """
        Initialized code dataset to given stage.
        :param stage: Either train, val, or eval.
        """
        super().__init__()
        self.stage = stage

    @staticmethod
    def get_zip_name() -> str:
        """
        :return: Returns the name of the code zip file.
        """
        return "code.zip"

    def get_definition_path(self, data_dir: str) -> str:
        """
        Returns path to stage definition file.
        :param data_dir: The base project path containing all stages.
        :return: Path to stage definition file.
        """
        return os.path.join(data_dir, self.stage, StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)

    def get_definition(self) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "Code": {
                    "path": "Code.csv"
                },
                "Issue": {
                    "path": "Issue.csv"
                }
            },
            "traces": {
                "issue2code": {
                    "source": "Issue",
                    "target": "Code",
                    "path": "Issue2Code.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 0,
                "allowed_missing_sources": 0,
                "allowed_missing_targets": 0
            }
        }
