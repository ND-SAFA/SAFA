from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.testprojects.abstract_test_project import AbstractTestProject
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject


class TestArtifactProjectReader(BaseTest):
    """
    Tests that csv project is correctly parsed.
    """
    test_project = ArtifactTestProject()

    def test_read_project(self):
        """
        Tests that the csv project can be read and translated to data frames.
        """
        self.verify_project_data_frames(self.test_project)

    def verify_project_data_frames(self, test_project: AbstractTestProject) -> None:
        """
        Verifies that entries are found in data frames created by project reader.
        :param test_project: Project containing entities to compare data frames to.
        :return: None
        """
        project_reader = test_project.get_project_reader()
        artifact_df = project_reader.read_project()
        TestAssertions.verify_entities_in_df(self, test_project.get_artifact_entries(), artifact_df)
