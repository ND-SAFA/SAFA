import os

from data.readers.entity.entity_reader import EntityReader
from data.readers.entity.formats.tests.test_xml_entity_format import TestXmlEntityFormat
from data.keys.structure_keys import StructuredKeys
from testres.base_test import BaseTest
from testres.paths.test_format_paths import XML_ENTITY_PATH
from testres.test_assertions import TestAssertions


class TestEntityReader(BaseTest):
    """
    Responsible for testing the reading and processing of entities.
    """

    def test_read_entities(self):
        """
        Tests that source entities are read in and conversions are applied.
        """
        project_path, file = os.path.split(XML_ENTITY_PATH)
        new_col = "new_name"
        conversion_id = "conversion-id"
        conversions = {conversion_id: {"name": new_col}}
        definition = self.create_definition(file, **{
            StructuredKeys.PARAMS: {"xpath": TestXmlEntityFormat.get_xpath()},
            "cols": conversion_id
        })
        entity_reader = EntityReader(project_path, definition, conversions)
        original_df = entity_reader.read_entities()
        converted_entities = [{new_col: e["name"]} for e in TestXmlEntityFormat.get_entities()]
        TestAssertions.verify_entities_in_df(self, converted_entities, original_df)

    def test_read_original_entities(self):
        """
        Tests that source entities are read in and all entries are present.
        """
        project_path, file = os.path.split(XML_ENTITY_PATH)
        definition = self.create_definition(file, **{StructuredKeys.PARAMS: {"xpath": TestXmlEntityFormat.get_xpath()}})
        entity_reader = EntityReader(project_path, definition)
        original_df = entity_reader.read_original_entities()
        TestAssertions.verify_entities_in_df(self, TestXmlEntityFormat.get_entities(), original_df)

    def test_read_column_conversions(self):
        """
        Tests ability to read column conversions from definition.
        """
        expected_value = 42
        definition = self.create_definition(**{StructuredKeys.COLS: "conversion-id"})
        conversions = {"conversion-id": expected_value}
        entity_reader = EntityReader("", definition, conversions)
        self.assertEqual(expected_value, entity_reader.get_column_conversion())

    def test_read_column_conversions_default_value(self):
        """
        Tests that default value is None when definition contains no column conversions.
        """
        definition = {StructuredKeys.PATH: ""}
        entity_reader = EntityReader("", definition, {})
        self.assertIsNone(entity_reader.get_column_conversion())

    @staticmethod
    def create_definition(path: str = "", **kwargs):
        return {StructuredKeys.PATH: path, **kwargs}
