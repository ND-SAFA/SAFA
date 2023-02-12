from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractDatasetDescriptor
from util.override import overrides


class CM1Descriptor(AbstractDatasetDescriptor):
    """
    Describes the CM1 project reader.
    """

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_url(cls) -> str:
        """
        :return: Returns URL to CM1 on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/CM1.zip"

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_definition(cls) -> Dict:
        """
        :return: Returns this project's structured project definition.
        """
        return {
            "artifacts": {
                "High Level Requirements": {
                    "path": "CM1-sourceArtifacts.xml",
                    "cols": "CM1-artifacts"
                },
                "Low Level Requirements": {
                    "path": "CM1-targetArtifacts.xml",
                    "cols": "CM1-artifacts"
                }
            },
            "traces": {
                "high2low.csv": {
                    "source": "High Level Requirements",
                    "target": "Low Level Requirements",
                    "path": "CM1-answerSet.xml",
                    "cols": "CM1-traces"
                }
            },
            "conversions": {
                "CM1-artifacts": {
                    "id": "id",
                    "content": "content"
                },
                "CM1-traces": {
                    "source_artifact_id": "source",
                    "target_artifact_id": "target"
                }
            },
            "overrides": {
                "allowed_orphans": 26
            }
        }
