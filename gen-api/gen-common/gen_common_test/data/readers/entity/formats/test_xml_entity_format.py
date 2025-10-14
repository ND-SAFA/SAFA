from typing import Dict, List, Type

from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common.data.readers.entity.formats.xml_entity_format import XmlEntityFormat
from gen_common_test.base.paths.format_paths import GEN_COMMON_TEST_FORMAT_XML_PATH
from gen_common_test.data.readers.entity.formats.abstract_entity_format_test import AbstractEntityFormatTest


class TestXmlEntityFormat(AbstractEntityFormatTest):
    def test_extensions(self):
        self.verify_extensions()

    def test_parser(self):
        self.verify_parser(xpath=self.get_xpath())

    @property
    def entity_format(self) -> Type[AbstractEntityFormat]:
        return XmlEntityFormat

    @property
    def data_path(self) -> str:
        return GEN_COMMON_TEST_FORMAT_XML_PATH

    @staticmethod
    def get_entities() -> List[Dict]:
        return [{"name": 1}, {"name": 2}]

    @staticmethod
    def get_xpath() -> str:
        return "/entities/entity"
