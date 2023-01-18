from data.datasets.creators.readers.entity.formats.csv_entity_format import CsvEntityFormat
from data.datasets.creators.readers.entity.formats.folder_entity_format import FolderEntityFormat
from data.datasets.creators.readers.entity.formats.json_entity_format import JsonEntityFormat
from data.datasets.creators.readers.entity.formats.xml_entity_format import XmlEntityFormat
from data.datasets.creators.readers.entity.supported_entity_formats import SupportedEntityFormats
from data.datasets.keys.structure_keys import StructureKeys
from testres.base_test import BaseTest
from testres.paths.test_format_paths import CSV_ENTITY_PATH, FOLDER_PROJECT_PATH, JSON_ENTITY_PATH, XML_ENTITY_PATH


class TestSupportedEntityFormat(BaseTest):
    """
    Test entity format's ability to retrieve correct format.
    """
    DATUM = {
        CsvEntityFormat: CSV_ENTITY_PATH,
        FolderEntityFormat: FOLDER_PROJECT_PATH,
        XmlEntityFormat: XML_ENTITY_PATH,
        JsonEntityFormat: JSON_ENTITY_PATH
    }

    def test_get_entity_parser(self):
        """
        Tests ability to retrieve parser using implied methods. Includes testing all
        types of extensions.
        """
        for entity_format, data_path in self.DATUM.items():
            retrieved_parser = SupportedEntityFormats.get_parser(data_path)
            self.assertEqual(retrieved_parser, entity_format.get_parser())

    def test_get_entity_parser_explicit(self):
        """
        Tests ability to retrieve parser when it is explicitly set.
        """
        for entity_format_name, entity_format in SupportedEntityFormats.FORMATS.items():
            data_path = self.DATUM[entity_format]
            retrieved_parser = SupportedEntityFormats.get_parser(data_path, {StructureKeys.PARSER: entity_format_name})
            self.assertEqual(retrieved_parser, entity_format.get_parser())
