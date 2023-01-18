from typing import Dict, List, Type

from data.datasets.creators.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from data.datasets.creators.readers.entity.formats.folder_entity_format import FolderEntityFormat
from data.datasets.creators.readers.entity.formats.tests.abstract_entity_format_test import AbstractEntityFormatTest
from data.datasets.keys.structure_keys import StructureKeys
from testres.paths.test_format_paths import FOLDER_PROJECT_PATH


class TestFolderEntityFormat(AbstractEntityFormatTest):
    def test_extensions(self):
        self.verify_extensions()

    def test_parser(self):
        self.verify_parser()

    @property
    def entity_format(self) -> Type[AbstractEntityFormat]:
        return FolderEntityFormat

    @property
    def data_path(self) -> str:
        return FOLDER_PROJECT_PATH

    @staticmethod
    def get_entities() -> List[Dict]:
        def create_body(artifact_id: int) -> Dict:
            return {
                StructureKeys.Artifact.ID: str(artifact_id) + ".txt",
                StructureKeys.Artifact.BODY: f"This is artifact {artifact_id}."
            }

        return [create_body(i) for i in range(1, 3, 1)]
