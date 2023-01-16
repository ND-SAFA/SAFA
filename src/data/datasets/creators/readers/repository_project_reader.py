from typing import Dict

from data.datasets.creators.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from data.datasets.creators.readers.definitions.tim_project_definition import TimProjectDefinition
from data.datasets.keys.structure_keys import StructureKeys


class RepositoryProjectReader(AbstractProjectDefinition):
    """
    Reads project extracted from GitHub repository.
    """

    @staticmethod
    def read_project_definition(_: str) -> Dict:
        """
        Creates definition for reading GitHub repository composed of commit and issues.
        :return: Project definition for repository.
        """
        return {
            StructureKeys.ARTIFACTS: {
                "Commit": {
                    StructureKeys.PATH: "commit.csv",
                    StructureKeys.COLS: StructureKeys.ARTIFACTS
                },
                "Issue": {
                    StructureKeys.PATH: "issue.csv",
                    StructureKeys.COLS: StructureKeys.ARTIFACTS
                }
            },
            StructureKeys.TRACES: {
                "commit2issue": {
                    StructureKeys.Trace.SOURCE: "Commit",
                    StructureKeys.Trace.TARGET: "Issue",
                    StructureKeys.PATH: "commit2issue.csv",
                    StructureKeys.COLS: StructureKeys.TRACES
                }
            },
            StructureKeys.COLS: {
                **TimProjectDefinition.CONVERSIONS[TimProjectDefinition.CSV]
            }
        }
