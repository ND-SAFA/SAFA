from test.data.prompts.artifact_prompt_test_util import ArtifactPromptTestUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestArtifactPrompt(BaseTest):
    ARTIFACT = EnumDict({ArtifactKeys.ID: "id", ArtifactKeys.CONTENT: "content"})
    PROMPT = "This is a prompt"

    def test_build(self):
        id_, content = self.ARTIFACT[ArtifactKeys.ID], self.ARTIFACT[ArtifactKeys.CONTENT]

        base_with_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.BASE, include_id=True)
        prompt = base_with_id._build(self.ARTIFACT)
        expected_artifact_format = f"{id_}: {content}"
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        base_without_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.BASE, include_id=False)
        prompt = base_without_id._build(self.ARTIFACT)
        expected_artifact_format = f"{content}"
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        xml_with_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.XML, include_id=True)
        prompt = xml_with_id._build(self.ARTIFACT)
        expected_artifact_format = f"<artifact>\n\t<id>{id_}</id>\n\t<body>{content}</body>\n</artifact>"
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        xml_without_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.XML, include_id=False)
        prompt = xml_without_id._build(self.ARTIFACT)
        expected_artifact_format = f"<artifact>\n\t{content}\n</artifact>"
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)
