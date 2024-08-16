from typing import Dict, List, Type

from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common.data.readers.entity.formats.folder_entity_format import FolderEntityFormat
from gen_common_test.data.readers.entity.formats.abstract_entity_format_test import AbstractEntityFormatTest
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common_test.paths.test_format_paths import FOLDER_PROJECT_PATH


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
                StructuredKeys.Artifact.ID.value: str(artifact_id) + ".txt",
                StructuredKeys.Artifact.CONTENT.value: f"This is artifact {artifact_id}."
            }

        return [create_body(i) for i in range(1, 3, 1)]
