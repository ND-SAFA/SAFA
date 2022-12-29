from typing import Dict

from data.datasets.creators.readers.entity.entity_reader import EntityReader, EntityType
from data.datasets.keys.safa_format import SafaKeys
from data.tree.artifact import Artifact


class ArtifactReader(EntityReader):
    def __init__(self, base_path: str, artifact_definition: Dict, **kwargs):
        super().__init__(base_path, artifact_definition, **kwargs)

    def create(self, artifact_df) -> EntityType:
        artifacts = []
        for _, artifact_row in artifact_df.iterrows():
            artifact_id = artifact_row[SafaKeys.ARTIFACT_ID]
            if isinstance(artifact_id, float):
                artifact_id = str(int(artifact_id))
            artifacts.append(Artifact(artifact_id,
                                      artifact_row[SafaKeys.SAFA_CVS_ARTIFACT_TOKEN]))
        return artifacts
