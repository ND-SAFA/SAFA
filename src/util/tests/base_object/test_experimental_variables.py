from models.model_manager import ModelManager
from test.base_test import BaseTest
from test.test_object_creator import TestObjectCreator
from variables.experimental_variable import ExperimentalVariable
from variables.variable import Variable


class TestExperimentalVariables(BaseTest):

    def test_initialize(self):
        DEFINITION = {
            "model_path": ExperimentalVariable([Variable("roberta-base"), Variable("bert-base")]),
        }
        result = TestObjectCreator.create(ModelManager, **DEFINITION)
        print(result)
