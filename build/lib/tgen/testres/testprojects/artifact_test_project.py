from typing import List

from common_resources.data.objects.artifact import Artifact
from common_resources.data.keys.structure_keys import StructuredKeys
from common_resources.data.readers.abstract_project_reader import AbstractProjectReader
from common_resources.data.readers.artifact_project_reader import ArtifactProjectReader
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

    @classmethod
    def get_artifact_entries(cls) -> List[Artifact]:
        project_reader = cls.get_project_reader()
        artifact_df = project_reader.read_project()
        return artifact_df.to_artifacts()

    def _get_artifacts_in_layer(cls, layer: StructuredKeys.LayerMapping) -> List[Artifact]:
        raise ValueError("No layers are allowed in artifact data frame.")
