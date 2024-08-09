from copy import deepcopy

from common_resources_test.prompts.artifact_prompt_test_util import ArtifactPromptTestUtil
from common_resources.tools.util.enum_util import EnumDict
from common_resources.data.keys.structure_keys import TraceKeys, ArtifactKeys
from common_resources.llm.prompts.artifact_prompt import ArtifactPrompt
from common_resources_test.base_tests.base_test import BaseTest


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

        markdown_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.MARKDOWN, include_id=True)
        prompt = markdown_id._build(self.ARTIFACT)
        expected_artifact_format = f"# {id_}\n        {content}"
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        markdown_id_and_relation = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.MARKDOWN, include_id=True)
        source_artifact = deepcopy(self.ARTIFACT)
        source_artifact[TraceKeys.SOURCE] = True
        prompt = markdown_id_and_relation._build(source_artifact)
        expected_artifact_format = f"# {id_} (Child)\n        {content}"
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        markdown = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.MARKDOWN, include_id=False)
        prompt = markdown._build(source_artifact)
        expected_artifact_format = f"# Child\n        {content}"
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        target_artifact = deepcopy(self.ARTIFACT)
        target_artifact[TraceKeys.TARGET] = True
        prompt = markdown._build(target_artifact)
        expected_artifact_format = f"# Parent\n        {content}"
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)
