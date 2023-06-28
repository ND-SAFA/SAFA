from typing import List

from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt import Prompt


class TracePrompt(Prompt):
    def __init__(self, value: str, artifact_prompts: List[ArtifactPrompt]):
        super().__init__(value)
        self.artifact_prompts = artifact_prompts

    def set_artifacts(self, artifact_prompts: List[ArtifactPrompt]):
        self.artifact_prompts = artifact_prompts

    def build_as_numbered(self):
        """
        1. [ID]: [BODY]
        2. [ID]: [BODY]
        """
        raise NotImplementedError()
