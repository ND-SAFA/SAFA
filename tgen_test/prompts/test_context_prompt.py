from copy import deepcopy

from common_resources.tools.util.enum_util import EnumDict
from common_resources.data.keys.structure_keys import ArtifactKeys
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestContextPrompt(BaseTest):
    ARTIFACTS = [EnumDict({ArtifactKeys.ID: "id1", ArtifactKeys.CONTENT: "content1"}),
                 EnumDict({ArtifactKeys.ID: "id2", ArtifactKeys.CONTENT: "content2"})]
    PROMPT = "This is a prompt"

    def test_build_ids_provided(self):
        context_prompt = self.get_context_prompt(id_to_context_artifacts={"target": deepcopy(self.ARTIFACTS)})
        prompt = context_prompt.build(artifact=EnumDict({ArtifactKeys.ID: "target", ArtifactKeys.CONTENT: ["target_content"]}),
                                      context_threshold=0.6)
        for related_artifact in self.ARTIFACTS:
            self.assertIn(related_artifact[ArtifactKeys.ID], prompt)
            self.assertIn(related_artifact[ArtifactKeys.CONTENT], prompt)

    def get_context_prompt(self, **params):
        return ContextPrompt(build_method=MultiArtifactPrompt.BuildMethod.XML, **params)
