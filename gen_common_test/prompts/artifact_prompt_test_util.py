from typing import List, Union
from unittest import TestCase

from gen_common.constants import NEW_LINE


class ArtifactPromptTestUtil:
    @staticmethod
    def assert_expected_format(test_case: TestCase, prompt: str, expected_prompt: str,
                               expected_artifact_format: Union[str, List[str]]) -> None:
        """
        Verifies that prompt formatted the artifacts in the expected format.
        :param test_case: The test case to make assertions for.
        :param prompt: The prompt being checked for formatting.
        :param expected_prompt: The expected prompt message.
        :param expected_artifact_format: The expected artifact format.
        :return: None
        """
        if isinstance(expected_artifact_format, list):
            expected_artifact_format = NEW_LINE.join(expected_artifact_format)
        if expected_prompt:
            split_by_newline = [p for p in prompt.split(NEW_LINE) if p]
            prompt, *artifacts = split_by_newline
            artifacts = NEW_LINE.join(artifacts)
            test_case.assertEqual(expected_prompt, prompt)
        else:
            artifacts = prompt
        test_case.assertEqual(expected_artifact_format, artifacts)
