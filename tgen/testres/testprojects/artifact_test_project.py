from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.testres.paths.project_paths import SAFA_PROJECT_PATH
from tgen.testres.testprojects.safa_test_project import SafaTestProject


class ArtifactTestProject(SafaTestProject):
    """
    Contains safa test project testing details.
    """

    @classmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns structured project reader for project
        """
        return ArtifactProjectReader(SAFA_PROJECT_PATH, overrides={"allowed_orphans": 2, "remove_orphans": True})
