from abc import abstractmethod
from typing import Dict, List, Type

from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common_test.base_tests.base_test import BaseTest


class AbstractEntityFormatTest(BaseTest):
    """
    Tests all entity formats by testing the common abstract functionality for all formats.
    """

    def verify_extensions(self):
        """
        Tests that all supported file extensions are valid paths in format.
        """
        entity_format = self.entity_format
        for extension in entity_format.get_file_extensions():
            self.assertTrue(entity_format.is_format(extension))

    def verify_parser(self, **kwargs) -> None:
        """
        Verifies that parser returns entities defined by class.
        :param kwargs: Any additional parameters passed to parser.
        :return: None
        """
        entity_format_parser = self.entity_format
        entity_df = entity_format_parser.parse(self.data_path, **kwargs)
        expected_entities = self.get_entities()
        self.verify_entities_in_df(expected_entities, entity_df)

    @property
    @abstractmethod
    def entity_format(self) -> Type[AbstractEntityFormat]:
        """
        :return:Returns the entity format being tested.
        """

    @property
    @abstractmethod
    def data_path(self) -> str:
        """
        :return: Returns path to data of the format being tested
        """

    @staticmethod
    @abstractmethod
    def get_entities() -> List[Dict]:
        """
        Performs the verification of the data frame processed by format.
        :param df: The data frame produced by the format parser.
        :return: None
        """
