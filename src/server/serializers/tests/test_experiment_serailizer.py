from experiments.experiment_step import ExperimentStep
from test.base_test import BaseTest
from util.definition_creator import DefinitionCreator
from util.object_creator import ObjectCreator
from variables.definition_variable import DefinitionVariable
from variables.multi_variable import MultiVariable


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

    def test_playground(self):
        step = ObjectCreator.create(ExperimentStep)
        print(step)
