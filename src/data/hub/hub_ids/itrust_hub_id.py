from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId
from util.override import overrides


class ITrustHubId(AbstractHubId):
    """
    Describes the iTrust project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to iTrust on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/iTrust.zip"

    def get_definition(self) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "Use Cases": {
                    "path": "UC",
                    "parser": "FOLDER",
                    "params": {
                        "with_extension": False
                    }
                },
                "Java Code": {
                    "path": "itrust_v10_code/src/edu/ncsu/csc/itrust",
                    "parser": "FOLDER",
                    "params": {
                        "use_file_name": True,
                        "with_extension": False
                    }
                },
                "JSP Code": {
                    "path": "itrust_v10_code/WebRoot",
                    "parser": "FOLDER",
                    "params": {
                        "use_file_name": False,
                        "with_extension": False,
                        "exclude_ext": [".jar", ".png", ".gif"]
                    }
                }
            },
            "traces": {
                "Req2Code": {
                    "source": "Use Cases",
                    "target": "Java Code",
                    "path": "answer_req_code.xml",
                    "cols": "itrust-traces",
                    "params": {
                        "xpath": "//links/link"
                    }
                }
            },
            "conversions": {
                "itrust-artifacts": {
                    "art_id": "id",
                    "art_title": "content"
                },
                "itrust-traces": {
                    "source_artifact_id": "source",
                    "target_artifact_id": "target"
                }
            },
            "overrides": {
                "allowed_orphans": 272
            }
        }
