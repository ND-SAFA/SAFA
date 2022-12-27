from typing import Dict

from data.datasets.creators.readers.project.structure_keys import StructureKeys
from data.datasets.creators.readers.project.tim_definition_reader import TimProjectReader
from data.datasets.formats.safa_format import SafaFormat
from util.uncased_dict import UncasedDict


class RepositoryProjectReader(TimProjectReader):
    def read_definition(self, **kwargs) -> Dict:
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
        return UncasedDict(definition).rename_property(SafaFormat.FILE, StructureKeys.PATH)
