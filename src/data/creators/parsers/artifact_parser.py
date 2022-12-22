from typing import Dict

from data.creators.parsers.entity_parser import EntityParser
from data.formats.safa_format import SafaFormat
from data.tree.artifact import Artifact


class ArtifactParser(EntityParser):
    def __init__(self, project_path: str, artifact_definition: Dict, **kwargs):
        super().__init__(project_path, artifact_definition, **kwargs)
        artifact_df = self.get_entities()
        artifacts = []
        for _, artifact_row in artifact_df.iterrows():
            artifacts.append(Artifact(artifact_row[SafaFormat.ARTIFACT_ID],
                                      artifact_row[SafaFormat.SAFA_CVS_ARTIFACT_TOKEN]))
        self.artifacts = artifacts

    def __iter__(self) -> Artifact:
        for artifact in self.artifacts:
            yield artifact
