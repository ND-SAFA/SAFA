from typing import List

from gen_common.data.objects.artifact import Artifact
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.data.readers.artifact_project_reader import ArtifactProjectReader
from gen_common_test.paths.project_paths import SAFA_PROJECT_PATH
from gen_common_test.testprojects.safa_test_project import SafaTestProject


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
