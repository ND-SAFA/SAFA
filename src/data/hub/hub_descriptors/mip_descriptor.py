from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractDatasetDescriptor


class MipDescriptor(AbstractDatasetDescriptor):
    """
    Describes the medical infusion pump dataset.
    """

    @classmethod
    def get_url(cls) -> str:
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/mip.zip"

    @classmethod
    def get_definition(cls) -> Dict:
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
