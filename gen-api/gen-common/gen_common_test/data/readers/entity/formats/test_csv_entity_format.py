from typing import Dict, List, Type

from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common.data.readers.entity.formats.csv_entity_format import CsvEntityFormat
from gen_common_test.base.paths.format_paths import GEN_COMMON_TEST_FORMAT_CSV_PATH
from gen_common_test.data.readers.entity.formats.abstract_entity_format_test import AbstractEntityFormatTest
from gen_common_test.testprojects.csv_test_project import CsvTestProject


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
        return GEN_COMMON_TEST_FORMAT_CSV_PATH

    @classmethod
    def get_entities(cls) -> List[Dict]:
        return cls.test_project.get_csv_entries()
