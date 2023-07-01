from enum import auto, Enum
from typing import Union

from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.prompts.prompt import Prompt
from tgen.util.enum_util import EnumDict
from tgen.util.override import overrides
from tgen.util.prompt_util import PromptUtil


class ArtifactPrompt(Prompt):
    """
    Responsible for formatting and parsing of presenting a artifact in a prompt
    """

    class BuildMethod(Enum):
        """
        The method to build the prompt (determines prompt format)
        """
        XML = auto()
        BASE = auto()

    def __init__(self, build_method: BuildMethod = BuildMethod.BASE, include_id: bool = True):
        """
        Constructor for making a prompt from an artifact
        :param build_method: The method to build the prompt (determines prompt format)
        :param include_id: If True, includes the id of the artifact
        """
        self.build_method = build_method
        self.build_methods = {self.BuildMethod.XML: self._build_as_xml,
                              self.BuildMethod.BASE: self._build_as_base}
        self.include_id = include_id
        super().__init__(value=EMPTY_STRING, response_tag=None)

    @overrides(Prompt)
    def _build(self, artifact: EnumDict, **kwargs) -> str:
        """
        Builds the artifact prompt using the given build method
        :param artifact: The dictionary containing the attributes representing an artifact
        :param kwargs: Ignored
        :return: The formatted prompt
        """
        if self.build_method in self.build_methods:
            return self.build_methods[self.build_method](artifact_id=artifact.get(ArtifactKeys.ID, EMPTY_STRING),
                                                         artifact_body=artifact[ArtifactKeys.CONTENT],
                                                         include_id=self.include_id)
        else:
            raise NameError(f"Unknown Build Method: {self.build_method}")

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
        content_for_prompt = NEW_LINE.join([formatted_id, formatted_content]) if include_id else formatted_content
        formatted_artifact = PromptUtil.create_xml(tag_name="artifact",
                                                   tag_content=f"{NEW_LINE}{content_for_prompt}{NEW_LINE}")
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
