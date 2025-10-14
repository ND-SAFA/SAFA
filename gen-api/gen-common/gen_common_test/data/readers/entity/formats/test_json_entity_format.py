from typing import Dict, List, Type

from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common.data.readers.entity.formats.json_entity_format import JsonEntityFormat
from gen_common_test.base.paths.format_paths import GEN_COMMON_TEST_FORMAT_JSON_PATH
from gen_common_test.data.readers.entity.formats.abstract_entity_format_test import AbstractEntityFormatTest


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
        return GEN_COMMON_TEST_FORMAT_JSON_PATH

    @staticmethod
    def get_entities() -> List[Dict]:
        return [{"name": "1"}, {"name": "2"}]
