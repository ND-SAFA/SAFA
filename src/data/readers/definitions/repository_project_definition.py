from typing import Dict

from data.readers.definitions.abstract_project_definition import AbstractProjectDefinition
from data.readers.definitions.tim_project_definition import TimProjectDefinition
from data.keys.structure_keys import StructuredKeys


class RepositoryProjectDefinition(AbstractProjectDefinition):
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
            StructuredKeys.ARTIFACTS: {
                "Commit": {
                    StructuredKeys.PATH: "commit.csv",
                    StructuredKeys.COLS: StructuredKeys.ARTIFACTS
                },
                "Issue": {
                    StructuredKeys.PATH: "issue.csv",
                    StructuredKeys.COLS: StructuredKeys.ARTIFACTS
                }
            },
            StructuredKeys.TRACES: {
                "commit2issue": {
                    StructuredKeys.Trace.SOURCE: "Commit",
                    StructuredKeys.Trace.TARGET: "Issue",
                    StructuredKeys.PATH: "commit2issue.csv",
                    StructuredKeys.COLS: StructuredKeys.TRACES
                }
            },
            StructuredKeys.CONVERSIONS: {
                **TimProjectDefinition.CONVERSIONS[TimProjectDefinition.CSV]
            }
        }
