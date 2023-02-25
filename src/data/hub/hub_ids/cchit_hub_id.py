from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId
from util.override import overrides


class CCHITHubId(AbstractHubId):
    """
    Describes the CCHIT project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing defefinition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/CCHIT.zip"

    @overrides(AbstractHubId)
    def get_definition(self) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "Requirements": {
                    "path": "source.xml",
                    "cols": "CCHIT-artifacts"
                },
                "Regulatory Codes": {
                    "path": "target.xml",
                    "cols": "CCHIT-artifacts"
                }
            },
            "traces": {
                "requirements2regulatorycodes.csv": {
                    "source": "Requirements",
                    "target": "Regulatory Codes",
                    "path": "answer.txt",
                    "cols": "CCHIT-traces"
                }
            },
            "conversions": {
                "CCHIT-artifacts": {
                    "art_id": "id",
                    "art_title": "content"
                },
                "CCHIT-traces": {
                    "source": "source",
                    "target": "target"
                }
            },
            "overrides": {
                "allowed_orphans": 693
            }
        }
