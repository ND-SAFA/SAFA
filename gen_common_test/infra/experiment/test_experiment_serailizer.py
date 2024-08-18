from gen_common.infra.experiment.definition_creator import DefinitionCreator
from gen_common.infra.experiment.variables.definition_variable import DefinitionVariable
from gen_common.infra.experiment.variables.multi_variable import MultiVariable
from gen_common_test.base.tests.base_test import BaseTest


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
