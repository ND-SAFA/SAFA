import os
from typing import Dict, List

from data.datasets.creators.readers.entity.artifact_reader import ArtifactReader
from data.datasets.keys.structure_keys import StructureKeys
from data.tree.artifact import Artifact
from testres.base_test import BaseTest
from testres.paths.paths import TEST_DATA_DIR


class TestArtifactReader(BaseTest):
    PROJECT = "structure"
    ARTIFACT_FILE = "source.xml"

    ARTIFACT_MAPPINGS = {
        "1674": "The system shall improve accessibility of online clinical information and results.",
        "1688": "The system shall integrate all components of the patient record to provide comprehensive and intelligent clinical information access and reporting."
    }

    def test_create(self):
        base_path: str = os.path.join(TEST_DATA_DIR, self.PROJECT)
        conversions = {
            "artifact": {
                "art_id": StructureKeys.Artifact.ID,
                "art_title": StructureKeys.Artifact.BODY
            }
        }
        artifact_definition = {
            StructureKeys.PATH: self.ARTIFACT_FILE,
            StructureKeys.COLS: "artifact"
        }
        artifact_reader = ArtifactReader(base_path, artifact_definition, conversions=conversions)
        artifacts = artifact_reader.get_entities()
        artifact_mapping = self.create_artifact_mapping(artifacts)

        self.assertEqual(len(artifacts), 2)
        for artifact_id, artifact_body in self.ARTIFACT_MAPPINGS.items():
            self.assertEqual(artifact_mapping[artifact_id].token, artifact_body)

    @staticmethod
    def create_artifact_mapping(artifacts: List[Artifact]) -> Dict[str, Artifact]:
        artifact_mapping = {}
        for artifact in artifacts:
            if artifact.id not in artifact_mapping:
                artifact_mapping[artifact.id] = artifact
        return artifact_mapping
