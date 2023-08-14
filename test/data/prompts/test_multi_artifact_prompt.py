from test.data.prompts.artifact_prompt_test_util import ArtifactPromptTestUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestMultiArtifactPrompt(BaseTest):
    ARTIFACTS = [EnumDict({ArtifactKeys.ID: "id1", ArtifactKeys.CONTENT: "content1"}),
                 EnumDict({ArtifactKeys.ID: "id2", ArtifactKeys.CONTENT: "content2"})]
    PROMPT = "This is a prompt"

    def test_build(self):
        artifact1, artifact2 = self.ARTIFACTS[0], self.ARTIFACTS[1]

        num_with_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.NUMBERED, include_ids=True)
        prompt = num_with_id._build(self.ARTIFACTS)
        expected_artifact_format = [f"1. {artifact1[ArtifactKeys.ID]}: {artifact1[ArtifactKeys.CONTENT]}",
                                    f"2. {artifact2[ArtifactKeys.ID]}: {artifact2[ArtifactKeys.CONTENT]}"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        num_without_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.NUMBERED, include_ids=False)
        prompt = num_without_id._build(self.ARTIFACTS)
        expected_artifact_format = [f"1. {artifact1[ArtifactKeys.CONTENT]}",
                                    f"2. {artifact2[ArtifactKeys.CONTENT]}"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        xml_with_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.XML, include_ids=True)
        prompt = xml_with_id._build(self.ARTIFACTS)
        expected_artifact_format = [
            f"<artifact>\n\t<id>{artifact1[ArtifactKeys.ID]}</id>\n\t<body>{artifact1[ArtifactKeys.CONTENT]}</body>\n</artifact>",
            f"<artifact>\n\t<id>{artifact2[ArtifactKeys.ID]}</id>\n\t<body>{artifact2[ArtifactKeys.CONTENT]}</body>\n</artifact>"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        xml_without_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.XML, include_ids=False)
        prompt = xml_without_id._build(self.ARTIFACTS)
        expected_artifact_format = [f"<artifact>\n\t{artifact1[ArtifactKeys.CONTENT]}\n</artifact>",
                                    f"<artifact>\n\t{artifact2[ArtifactKeys.CONTENT]}\n</artifact>"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)
