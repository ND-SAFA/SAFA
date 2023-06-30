from enum import auto, Enum
from typing import List

from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt import Prompt
from tgen.util.enum_util import EnumDict
from tgen.util.override import overrides


class MultiArtifactPrompt(Prompt):
    """
    Responsible for formatting and parsing of presenting many artifacts in a prompt
    """

    class BuildMethod(Enum):
        """
        The method to build the prompt (determines prompt format)
        """
        XML = auto()
        NUMBERED = auto()

    def __init__(self, build_method: BuildMethod = BuildMethod.NUMBERED, include_ids: bool = True, requires_trace_link: bool = False):
        """
        Constructor for making a prompt from many artifacts
        :param build_method: The method to build the prompt (determines prompt format)
        :param include_ids: If True, includes artifact ids
        """
        self.build_method = build_method
        self.build_methods = {self.BuildMethod.XML: self._build_as_xml,
                              self.BuildMethod.NUMBERED: self._build_as_numbered}
        self.include_ids = include_ids
        super().__init__(value=EMPTY_STRING, response_tag=None, requires_traces=requires_trace_link,
                         requires_artifacts=not requires_trace_link)

    @overrides(Prompt)
    def _build(self, artifacts: List[EnumDict], **kwargs) -> str:
        """
        Builds the artifacts prompt using the given build method
        :param artifacts: The list of dictionaries containing the attributes representing each artifact
        :param kwargs: Ignored
        :return: The formatted prompt
        """
        if self.build_method in self.build_methods:
            return self.build_methods[self.build_method](artifacts, include_ids=self.include_ids)
        else:
            raise NameError(f"Unknown Build Method: {self.build_method}")

    @staticmethod
    def _build_as_numbered(artifacts: List[EnumDict], include_ids: bool = False) -> str:
        """
        Formats the artifacts as follows:
        1. ID: BODY
        2. ID: BODY
        :param artifacts: The list of dictionaries containing the attributes representing each artifact
        :param include_ids: If True, includes artifact ids
        :return: The formatted prompt
        """
        numbered_format = "{}. {}"
        artifact_prompt = ArtifactPrompt(build_method=ArtifactPrompt.BuildMethod.BASE, include_id=include_ids)
        formatted_artifacts = [numbered_format.format(i, artifact_prompt.build(artifact=artifact)) for i, artifact in enumerate(artifacts)]
        return NEW_LINE.join(formatted_artifacts)

    @staticmethod
    def _build_as_xml(artifacts: List[ArtifactPrompt], include_ids: bool = True):
        """
        Formats the artifacts as follows:
        <artifact>
            <id>ID</id>
            <body>BODY</body>
        <artifact>
        :param artifacts: The list of dictionaries containing the attributes representing each artifact
        :param include_ids: If True, includes artifact ids
        :return: The formatted prompt
        """
        artifact_prompt = ArtifactPrompt(build_method=ArtifactPrompt.BuildMethod.BASE, include_id=include_ids)
        formatted_artifacts = [artifact_prompt.build(artifact=artifact) for artifact in artifacts]
        raise NEW_LINE.join(formatted_artifacts)
