from enum import Enum, auto
from typing import List, Dict

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt import Prompt


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

    class DataType(Enum):
        TRACES = auto()
        ARTIFACT = auto()

    def __init__(self, prompt_prefix: str = EMPTY_STRING,
                 build_method: BuildMethod = BuildMethod.NUMBERED,
                 include_ids: bool = True,
                 xml_tags: Dict = None,
                 data_type: DataType = DataType.ARTIFACT):
        """
        Constructor for making a prompt containing many artifacts.
        :param prompt_prefix: The prefix to attach to prompt.
        :param build_method: The method to build the prompt (determines prompt format).
        :param include_ids: If True, includes artifact ids
        :param xml_tags: If building using XML, specify the names of the tags as such {outer_tag: [id_tag, body_tag]}
        :param data_type: Whether the data is coming from artifacts or traces
        """
        self.build_method = build_method
        self.build_methods = {self.BuildMethod.XML: self._build_as_xml,
                              self.BuildMethod.NUMBERED: self._build_as_numbered}
        self.include_ids = include_ids
        self.data_type = data_type
        self.xml_tags = xml_tags
        super().__init__(value=prompt_prefix)

    @overrides(Prompt)
    def _build(self, artifacts: List[EnumDict], **kwargs) -> str:
        """
        Builds the artifacts prompt using the given build method
        :param artifacts: The list of dictionaries containing the attributes representing each artifact
        :param kwargs: Ignored
        :return: The formatted prompt
        """
        prompt = f"{NEW_LINE}{self.value}{NEW_LINE}" if self.value else EMPTY_STRING
        if self.build_method in self.build_methods:
            artifacts = self.build_methods[self.build_method](artifacts, include_ids=self.include_ids, xml_tags=self.xml_tags)
            return f"{prompt}{artifacts}"
        else:
            raise NameError(f"Unknown Build Method: {self.build_method}")

    @staticmethod
    def _build_as_numbered(artifacts: List[EnumDict], include_ids: bool = False, **kwargs) -> str:
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
        formatted_artifacts = [numbered_format.format(i + 1, artifact_prompt.build(artifact=artifact))
                               for i, artifact in enumerate(artifacts)]
        return NEW_LINE.join(formatted_artifacts)

    @staticmethod
    def _build_as_xml(artifacts: List[ArtifactPrompt], xml_tags: Dict, include_ids: bool = True):
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
        artifact_prompt = ArtifactPrompt(build_method=ArtifactPrompt.BuildMethod.XML, xml_tags=xml_tags,
                                         include_id=include_ids)
        formatted_artifacts = [artifact_prompt.build(artifact=artifact) for artifact in artifacts]
        return NEW_LINE.join(formatted_artifacts)

    def __repr__(self) -> str:
        """
        Returns a representation of the artifact prompt as a string
        :return: The artifact promtp as a string
        """
        if self.build_method.XML:
            return "<artifact>{artifact}<artifact> <artifact>{artifact}<artifact> ..."
        elif self.build_method.NUMBERED:
            return "1. {artifact1} " \
                   "2. {artifact2} ..."
