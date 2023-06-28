from typing import List

from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt import Prompt


class BulkArtifactPrompt(Prompt):

    def __init__(self, value: str, artifact_prompts: List[ArtifactPrompt] = None):
        super().__init__(value)
        self.artifact_prompts = artifact_prompts

    def set_artifacts(self, artifact_prompts: List[ArtifactPrompt]):
        self.artifact_prompts = artifact_prompts

    def build_as_numbered(self):
        """
        1. BODY
        2. BODY
        """
        raise NotImplementedError()

    def build_as_xml(self, artifacts: List[ArtifactPrompt]):
        """
        <artifact>
            <id>ID</id>
            <body>BODY</body>
        <artifact>
        """
        raise NotImplementedError()
