from abc import ABC, abstractmethod

from data.readers.project.iproject_reader import IProjectParser
from test.base_test import BaseTest


class TestDefinitionParser(BaseTest, ABC):
    @abstractmethod
    def get_definition_parser(self) -> IProjectParser:
        pass

    def test_create(self):
        definition_parser: IProjectParser = self.get_definition_parser()
     