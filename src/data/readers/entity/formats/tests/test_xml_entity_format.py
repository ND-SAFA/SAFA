from typing import Dict, List, Type

from data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from data.readers.entity.formats.tests.abstract_entity_format_test import AbstractEntityFormatTest
from data.readers.entity.formats.xml_entity_format import XmlEntityFormat
from testres.paths.test_format_paths import XML_ENTITY_PATH


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
        return XML_ENTITY_PATH

    @staticmethod
    def get_entities() -> List[Dict]:
        return [{"name": 1}, {"name": 2}]

    @staticmethod
    def get_xpath() -> str:
        return "/entities/entity"
