from enum import Enum, auto
from typing import Union

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE, TAB
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.prompts.prompt import Prompt


class ArtifactPrompt(Prompt):
    """
    Responsible for formatting and parsing of presenting a single artifact in a prompt.
    --- Examples ---
    Please rank the following children based on the parent artifact: <artifact></artifact>
    """

    class BuildMethod(Enum):
        """
        The method to build the prompt (determines prompt format)
        """
        XML = auto()
        BASE = auto()

    def __init__(self, prompt_start: str = EMPTY_STRING, build_method: BuildMethod = BuildMethod.BASE, include_id: bool = True):
        """
        Constructor for making a prompt from an artifact
        :param build_method: The method to build the prompt (determines prompt format)
        :param include_id: If True, includes the id of the artifact
        """
        self.build_method = build_method
        self.build_methods = {
            self.BuildMethod.XML: self._build_as_xml,
            self.BuildMethod.BASE: self._build_as_base}
        self.include_id = include_id
        super().__init__(value=prompt_start)

    @overrides(Prompt)
    def _build(self, artifact: EnumDict, **kwargs) -> str:
        """
        Builds the artifact prompt using the given build method
        :param artifact: The dictionary containing the attributes representing an artifact
        :param kwargs: Ignored
        :return: The formatted prompt
        """
        prompt = f"{NEW_LINE}{self.value}{NEW_LINE}" if self.value else EMPTY_STRING
        if self.build_method not in self.build_methods:
            raise NameError(f"Unknown Build Method: {self.build_method}")
        build_method = self.build_methods[self.build_method]
        artifact_id = artifact.get(ArtifactKeys.ID.value, EMPTY_STRING)
        content = artifact[ArtifactKeys.CONTENT]
        artifact = build_method(artifact_id=artifact_id, artifact_body=content, include_id=self.include_id)
        return f"{prompt}{artifact}"

    @staticmethod
    def _build_as_xml(artifact_id: Union[int, str], artifact_body: str, include_id: bool = True) -> str:
        """
        Formats the artifact as follows:
        <artifact>
            <id>ID</id> (if include_id)
            <body>BODY</body>
        </artifact>
        :param artifact_id: The id of the artifact
        :param artifact_body: The body of the artifact
        :param include_id: If True, includes the id of the artifact
        :return: The formatted prompt
        """
        formatted_id = PromptUtil.create_xml(tag_name="id", tag_content=artifact_id)
        formatted_content = PromptUtil.create_xml(tag_name="body", tag_content=artifact_body)
        content_for_prompt = f"{NEW_LINE}{TAB}".join([formatted_id, formatted_content]) if include_id else formatted_content
        formatted_artifact = PromptUtil.create_xml(tag_name="artifact",
                                                   tag_content=f"{NEW_LINE}{TAB}{content_for_prompt}{NEW_LINE}")
        return formatted_artifact

    @staticmethod
    def _build_as_base(artifact_id: Union[int, str], artifact_body: str, include_id: bool = True) -> str:
        """
        Formats the artifact as follows: [ID]: [BODY] if include id else just [BODY]
        :param artifact_id: The id of the artifact
        :param artifact_body: The body of the artifact
        :param include_id: If True, includes the id of the artifact
        :return: The formatted prompt
        """
        if include_id:
            return f"{artifact_id}: {artifact_body}"
        return artifact_body

    def __repr__(self) -> str:
        """
        Returns a representation of the artifact prompt as a string
        :return: The artifact promtp as a string
        """
        if self.build_method.XML:
            return "<artifact>{artifact}<artifact>"
        else:
            return "{artifact}"
