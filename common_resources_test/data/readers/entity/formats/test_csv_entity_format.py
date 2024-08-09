from typing import Dict, List, Type

from common_resources.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from common_resources.data.readers.entity.formats.csv_entity_format import CsvEntityFormat
from common_resources_test.data.readers.entity.formats.abstract_entity_format_test import AbstractEntityFormatTest
from common_resources_test.paths.test_format_paths import CSV_ENTITY_PATH
from common_resources_test.testprojects.csv_test_project import CsvTestProject


class TestCsvEntityFormat(AbstractEntityFormatTest):
    """
    Tests ability of the CSV format to read csv files into data frames.
    """
    test_project = CsvTestProject()

    def test_extensions(self):
        self.verify_extensions()

    def test_parser(self):
        self.verify_parser()

    @property
    def entity_format(self) -> Type[AbstractEntityFormat]:
        return CsvEntityFormat

    @property
    def data_path(self):
        return CSV_ENTITY_PATH

    @classmethod
    def get_entities(cls) -> List[Dict]:
        return cls.test_project.get_csv_entries()
