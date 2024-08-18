from typing import Dict, List, TypeVar
from unittest import TestCase

from gen_common.infra.experiment.experiment_serializer import ExperimentSerializer
from gen_common.infra.experiment.variables.definition_variable import DefinitionVariable
from gen_common.infra.experiment.variables.experimental_variable import ExperimentalVariable
from gen_common.infra.experiment.variables.variable import Variable

AppEntity = TypeVar('AppEntity')


class ExperimentSerializerTest(TestCase):
    input_data = {
        "experiment": {
            "model_path": {
                "*": ["robert-base-uncased", "~/desktop/safa"]
            },
            "output_path": "~/desktop",
            "augmentation": {
                "steps": [
                    {
                        "creator": "SAFA"
                    }
                ]
            }
        }
    }

    def test_single_variable(self):
        # A. Gather expected data
        variable_name = "output_path"
        variable_class = Variable
        expected_values = self.input_data["experiment"][variable_name]

        # 1. De-serialize data
        experiment_variables = self.deserialize([variable_name])

        # 2. Verify that resulting class is variable and value are as expected
        self.assertIn(variable_name, experiment_variables)
        parsed_variable: variable_class = experiment_variables[variable_name]
        self.assertTrue(isinstance(parsed_variable, variable_class))
        self.assertEqual(parsed_variable.value, expected_values)

    def test_multi_variable(self):
        # A. Gather expected data
        variable_name = "model_path"
        variable_class = ExperimentalVariable
        expected_values = self.input_data["experiment"][variable_name][ExperimentalVariable.SYMBOL]

        # 1. De-serialize data
        model_path_variable = self.deserialize([variable_name])

        # Check values
        processed_values = model_path_variable[variable_name]
        self.assertIsInstance(processed_values, variable_class)
        self.assertEqual(expected_values, processed_values)

    def test_definition_variable(self):
        # A. Gather expected data
        definition_key = "augmentation"
        expected_class = DefinitionVariable
        expected_values = self.input_data["experiment"][definition_key]

        # 1. De-serialize data
        experiment_parsed = self.deserialize([definition_key])

        # Check values
        self.assertIn(definition_key, experiment_parsed)

        # Extract definition variable
        definition_variable: expected_class = experiment_parsed[definition_key]
        self.assertTrue(isinstance(definition_variable, expected_class))

        # Check values
        definition_value: Dict = definition_variable.value
        self.assertIn("steps", definition_value)
        definition_steps = definition_value["steps"]
        self.assertIsInstance(definition_steps, Variable)

        for definition_step, expected_step in zip(definition_steps.value, expected_values["steps"]):
            self.assertIsInstance(definition_step, DefinitionVariable)
            for expected_key, expected_value in expected_step.items():
                self.assertIn(expected_key, definition_step)
                step_creator = definition_step[expected_key]
                self.assertIsInstance(step_creator, Variable)
                self.assertEqual(step_creator.value, expected_value)

    def deserialize(self, variable_names: List[str], is_valid: bool = True):
        """
        Creates experiment variables using subset of data in variable names.
        :param variable_names: The key names to include in experiment data.
        :param is_valid: Whether to expected serializer to be in a valid state.
        :return: Mapping between keys and variables.
        """
        variable_data = self.get_experiment_subset(variable_names)
        experiment_serializer = ExperimentSerializer(data=variable_data)
        self.assertEqual(experiment_serializer.is_valid(), is_valid)
        return experiment_serializer.save()

    def get_experiment_subset(self, fields: List[str]):
        """
        Returns experiment data with only given fields.
        :param fields: The fields to include in subset.
        :return: Dictionary containing experiment definitions of only those in defined fields.
        """
        field_dict = {field: self.input_data["experiment"][field] for field in fields}
        return {"experiment": field_dict}
