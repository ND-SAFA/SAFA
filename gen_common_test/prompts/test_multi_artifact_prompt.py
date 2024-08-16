from copy import deepcopy

from gen_common.constants import MAX_TOKENS_FOR_NO_SUMMARIES
from gen_common.data.keys.structure_keys import ArtifactKeys, TraceKeys
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.util import EnumDict
from gen_common_test.base_tests.base_test import BaseTest
from gen_common_test.prompts.artifact_prompt_test_util import ArtifactPromptTestUtil


class TestMultiArtifactPrompt(BaseTest):
    ARTIFACTS = [EnumDict({ArtifactKeys.ID: "id1.py", ArtifactKeys.CONTENT: "content1", ArtifactKeys.SUMMARY: "summary1"}),
                 EnumDict({ArtifactKeys.ID: "id2", ArtifactKeys.CONTENT: "content2", ArtifactKeys.SUMMARY: "summary1"})]
    PROMPT = "This is a prompt"

    def test_build_numbered(self):
        artifact1, artifact2 = self.ARTIFACTS[0], self.ARTIFACTS[1]

        num_with_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.NUMBERED, include_ids=True)
        prompt = num_with_id._build(self.ARTIFACTS)
        expected_artifact_format = [f"1. {artifact1[ArtifactKeys.ID]}: {artifact1[ArtifactKeys.SUMMARY]}",
                                    f"2. {artifact2[ArtifactKeys.ID]}: {artifact2[ArtifactKeys.CONTENT]}"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

        num_without_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.NUMBERED, include_ids=False)
        prompt = num_without_id._build(self.ARTIFACTS)
        expected_artifact_format = [f"1. {artifact1[ArtifactKeys.SUMMARY]}",
                                    f"2. {artifact2[ArtifactKeys.CONTENT]}"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

    def test_build_markdown(self):
        artifact1, artifact2 = self.ARTIFACTS[0], self.ARTIFACTS[1]
        markdown_id_with_prompt = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                                      include_ids=True)
        trace_artifacts = [deepcopy(self.ARTIFACTS[0]), deepcopy(self.ARTIFACTS[1])]
        trace_artifacts[0][TraceKeys.SOURCE] = True
        trace_artifacts[1][TraceKeys.TARGET] = True
        prompt = markdown_id_with_prompt._build(trace_artifacts)
        expected_artifact_format = [f"## {artifact1[ArtifactKeys.ID]} (Child)\n        {artifact1[ArtifactKeys.SUMMARY]}",
                                    f"## {artifact2[ArtifactKeys.ID]} (Parent)\n        {artifact2[ArtifactKeys.CONTENT]}"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)
        markdown_without_id = MultiArtifactPrompt(build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                                  include_ids=False)
        prompt = markdown_without_id._build(trace_artifacts)
        expected_artifact_format = [f"# Child\n        {artifact1[ArtifactKeys.SUMMARY]}",
                                    f"# Parent\n        {artifact2[ArtifactKeys.CONTENT]}"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, '', expected_artifact_format)

    def test_build_xml(self):
        artifact1, artifact2 = self.ARTIFACTS[0], self.ARTIFACTS[1]
        xml_with_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.XML, include_ids=True)
        prompt = xml_with_id._build(self.ARTIFACTS)
        expected_artifact_format = [
            f"<artifact>\n\t<id>{artifact1[ArtifactKeys.ID]}</id>\n\t<body>{artifact1[ArtifactKeys.SUMMARY]}</body>\n</artifact>",
            f"<artifact>\n\t<id>{artifact2[ArtifactKeys.ID]}</id>\n\t<body>{artifact2[ArtifactKeys.CONTENT]}</body>\n</artifact>"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)
        xml_without_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.XML, include_ids=False)
        prompt = xml_without_id._build(self.ARTIFACTS)
        expected_artifact_format = [f"<artifact>\n\t{artifact1[ArtifactKeys.SUMMARY]}\n</artifact>",
                                    f"<artifact>\n\t{artifact2[ArtifactKeys.CONTENT]}\n</artifact>"]
        ArtifactPromptTestUtil.assert_expected_format(self, prompt, self.PROMPT, expected_artifact_format)

    def test_build_with_no_summaries(self):
        artifact1, artifact2 = self.ARTIFACTS[0], self.ARTIFACTS[1]
        num_with_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.NUMBERED, include_ids=True,
                                          use_summary=False)
        prompt = num_with_id._build(self.ARTIFACTS)
        self.assertIn(artifact1[ArtifactKeys.CONTENT], prompt)
        self.assertIn(artifact2[ArtifactKeys.CONTENT], prompt)
        self.assertNotIn(artifact1[ArtifactKeys.SUMMARY], prompt)
        self.assertNotIn(artifact2[ArtifactKeys.SUMMARY], prompt)

        num_with_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.NUMBERED, include_ids=True,
                                          use_summary=False)
        prompt = num_with_id._build([self.ARTIFACTS[i % 2] for i in range(MAX_TOKENS_FOR_NO_SUMMARIES + 1)])
        # should use summary if more than 65K tokens are used os using 65K artifacts.
        self.assertIn(artifact1[ArtifactKeys.SUMMARY], prompt)
        self.assertIn(artifact2[ArtifactKeys.CONTENT], prompt)
        self.assertNotIn(artifact1[ArtifactKeys.CONTENT], prompt)
