from typing import Dict

from data.hub.abstract_dataset_descriptor import AbstractDatasetDescriptor
from util.override import overrides


class CCHITReader(AbstractDatasetDescriptor):
    """
    Describes the CCHIT project reader.
    """

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_description(cls) -> str:
        """
        :return: Description of CCHIT from coest.org.
        """
        return "Provides trace links between CCHIT healthcare regulatory codes and requirements for World Vista. Dataset is " \
               "industrial and created by research team."

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_url(cls) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing defefinition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/CCHIT.zip"

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_citation(cls) -> str:
        """
        TODO: Find original paper citation
        :return: Returns the citation for CCHIT dataset.
        """
        return "Under construction."

    @classmethod
    @overrides(AbstractDatasetDescriptor)
    def get_definition(cls) -> Dict:
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
            }
        }
