from typing import Dict

from data.hub.abstract_hub_id import AbstractHubId


class MipHubId(AbstractHubId):
    """
    Describes the medical infusion pump dataset.
    """

    def get_url(self) -> str:
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/mip.zip"

    def get_definition(self) -> Dict:
        return {
            "artifacts": {
                "Components": {
                    "path": "clean/components.csv"
                },
                "Requirements": {
                    "path": "clean/requirements.csv"
                }
            },
            "traces": {
                "requirement2component": {
                    "source": "Requirements",
                    "target": "Components",
                    "path": "AnswerMatrix.csv"
                }
            },
            "overrides": {
                "allowed_orphans": 22
            }
        }
