from typing import Dict

from data.formats.safa_format import SafaFormat
from data.readers.entity_reader import EntityReader, EntityType
from data.tree.artifact import Artifact


class ArtifactReader(EntityReader):
    def __init__(self, base_path: str, artifact_definition: Dict, **kwargs):
        super().__init__(base_path, artifact_definition, **kwargs)

    def create(self, artifact_df) -> EntityType:
        artifacts = []
        for _, artifact_row in artifact_df.iterrows():
            artifacts.append(Artifact(artifact_row[SafaFormat.ARTIFACT_ID],
                                      artifact_row[SafaFormat.SAFA_CVS_ARTIFACT_TOKEN]))
        return artifacts
