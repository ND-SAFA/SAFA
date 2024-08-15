from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.definition_creator import DefinitionCreator
from common_resources.tools.variables.definition_variable import DefinitionVariable
from common_resources.tools.variables.multi_variable import MultiVariable


class TestExperimentSerializer(BaseTest):
    def test_multi_variable(self):
        variable = DefinitionCreator.create_definition_variable({
            "jobs": [
                {"name": "abc"},
                {"name": "def"}
            ]
        })

        jobs_variable = variable.get("jobs")
        self.assertIsInstance(jobs_variable, MultiVariable)
        for job in jobs_variable.value:
            self.assertIsInstance(job, DefinitionVariable)
