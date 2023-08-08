from tgen.common.util.enum_util import EnumDict
from tgen.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestArtifactPrompt(BaseTest):
    ARTIFACT = EnumDict({ArtifactKeys.ID: "id", ArtifactKeys.CONTENT: "content"})
    PROMPT = "This is a prompt"

    def test_build(self):
        id_, content = self.ARTIFACT[ArtifactKeys.ID], self.ARTIFACT[ArtifactKeys.CONTENT]

        base_with_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.BASE, include_id=True)
        output = base_with_id._build(self.ARTIFACT)
        expected_format = f"{id_}: {content}"
        self.eval_format(expected_format, output)

        base_without_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.BASE, include_id=False)
        output = base_without_id._build(self.ARTIFACT)
        expected_format = f"{content}"
        self.eval_format(expected_format, output)

        xml_with_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.XML, include_id=True)
        output = xml_with_id._build(self.ARTIFACT)
        expected_format = f"<artifact><id>{id_}</id><body>{content}</body></artifact>"
        self.eval_format(expected_format, output)

        xml_without_id = ArtifactPrompt(self.PROMPT, build_method=ArtifactPrompt.BuildMethod.XML, include_id=False)
        output = xml_without_id._build(self.ARTIFACT)
        expected_format = f"<artifact>{content}</artifact>"
        self.eval_format(expected_format, output)

    def eval_format(self, expected_format: str, output: str):
        split_by_newline = [p for p in output.split(NEW_LINE) if p]
        prompt = split_by_newline[0]
        a_format = EMPTY_STRING.join(split_by_newline[1:])
        self.assertEqual(prompt, self.PROMPT)
        self.assertEqual(a_format, expected_format)
