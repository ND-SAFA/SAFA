from typing import List

from tgen.common.util.enum_util import EnumDict
from tgen.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestMultiArtifactPrompt(BaseTest):
    ARTIFACTS = [EnumDict({ArtifactKeys.ID: "id1", ArtifactKeys.CONTENT: "content1"}),
                 EnumDict({ArtifactKeys.ID: "id2", ArtifactKeys.CONTENT: "content2"})]
    PROMPT = "This is a prompt"

    def test_build(self):
        artifact1, artifact2 = self.ARTIFACTS[0], self.ARTIFACTS[1]

        num_with_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.NUMBERED, include_ids=True)
        output = num_with_id._build(self.ARTIFACTS)
        expected_format = [f"1. {artifact1[ArtifactKeys.ID]}: {artifact1[ArtifactKeys.CONTENT]}",
                           f"2. {artifact2[ArtifactKeys.ID]}: {artifact2[ArtifactKeys.CONTENT]}"]
        self.eval_format(expected_format, output)

        num_without_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.NUMBERED, include_ids=False)
        output = num_without_id._build(self.ARTIFACTS)
        expected_format = [f"1. {artifact1[ArtifactKeys.CONTENT]}",
                           f"2. {artifact2[ArtifactKeys.CONTENT]}"]
        self.eval_format(expected_format, output)

        xml_with_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.XML, include_ids=True)
        output = xml_with_id._build(self.ARTIFACTS)
        expected_format = [f"<artifact><id>{artifact1[ArtifactKeys.ID]}</id><body>{artifact1[ArtifactKeys.CONTENT]}</body></artifact>",
                           f"<artifact><id>{artifact2[ArtifactKeys.ID]}</id><body>{artifact2[ArtifactKeys.CONTENT]}</body></artifact>"]
        self.eval_format(expected_format, output)

        xml_without_id = MultiArtifactPrompt(self.PROMPT, build_method=MultiArtifactPrompt.BuildMethod.XML, include_ids=False)
        output = xml_without_id._build(self.ARTIFACTS)
        expected_format = [f"<artifact>{artifact1[ArtifactKeys.CONTENT]}</artifact>",
                           f"<artifact>{artifact2[ArtifactKeys.CONTENT]}</artifact>"]
        self.eval_format(expected_format, output)

    def eval_format(self, expected_format: List[str], output: str):
        split_by_newline = [p for p in output.split(NEW_LINE) if p]
        prompt = split_by_newline[0]
        a_format = EMPTY_STRING.join(split_by_newline[1:])
        self.assertEqual(prompt, self.PROMPT)
        self.assertEqual(a_format, EMPTY_STRING.join(expected_format))
