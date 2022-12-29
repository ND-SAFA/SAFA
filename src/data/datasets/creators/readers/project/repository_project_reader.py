from typing import Dict

from data.datasets.creators.readers.project.tim_project_reader import TimProjectReader
from data.datasets.keys.safa_format import SafaKeys
from data.datasets.keys.structure_keys import StructureKeys
from util.uncased_dict import UncasedDict


class RepositoryProjectReader(TimProjectReader):
    def _read_definition(self, **kwargs) -> Dict:
        definition = {
            "DataFiles": {
                "Commit": {
                    "File": "commit.csv"
                },
                "Issue": {
                    "File": "issue.csv"
                }
            },
            "commit2issue": {
                "Source": "Commit",
                "Target": "Issue",
                "File": "commit2issue.csv"
            }
        }
        return UncasedDict(definition).rename_property(SafaKeys.FILE, StructureKeys.PATH)
