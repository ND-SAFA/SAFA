from typing import Dict, List, Type

from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common.data.readers.entity.formats.json_entity_format import JsonEntityFormat
from gen_common_test.data.readers.entity.formats.abstract_entity_format_test import AbstractEntityFormatTest
from gen_common_test.paths.test_format_paths import JSON_ENTITY_PATH


class TestJsonEntityFormat(AbstractEntityFormatTest):
    """
    Tests ability to parser json file as entities.
    """

    def test_extensions(self):
        self.verify_extensions()

    def test_parser(self):
        self.verify_parser()

    @property
    def entity_format(self) -> Type[AbstractEntityFormat]:
        return JsonEntityFormat

    @property
    def data_path(self) -> str:
        return JSON_ENTITY_PATH

    @staticmethod
    def get_entities() -> List[Dict]:
        return [{"name": "1"}, {"name": "2"}]
