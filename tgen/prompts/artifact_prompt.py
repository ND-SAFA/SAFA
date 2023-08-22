from enum import Enum, auto
from typing import Union, Dict, List

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE, TAB
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.prompts.prompt import Prompt


class ArtifactPrompt(Prompt):
    """
    Responsible for formatting and parsing of presenting a single artifact in a prompt.
    --- Examples ---
    Please rank the following children based on the parent artifact: <artifact></artifact>
    """
    DEFAULT_XML_TAGS = {"artifact": ["id", "body"]}

    class BuildMethod(Enum):
        """
        The method to build the prompt (determines prompt format)
        """
        XML = auto()
        BASE = auto()

    def __init__(self, prompt_start: str = EMPTY_STRING, build_method: BuildMethod = BuildMethod.BASE,
                 include_id: bool = True, xml_tags: Dict[str, List[str]] = None):
        """
        Constructor for making a prompt from an artifact
        :param build_method: The method to build the prompt (determines prompt format)
        :param xml_tags: If building using XML, specify the names of the tags as such {outer_tag: [id_tag, body_tag]}
        :param include_id: If True, includes the id of the artifact
        """
        self.xml_tags = xml_tags if xml_tags else self.DEFAULT_XML_TAGS
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
        artifact_id = artifact.get(StructuredKeys.Artifact.ID.value, EMPTY_STRING)
        content = artifact.get(StructuredKeys.Artifact.SUMMARY, None)
        if not content:
            content = artifact[StructuredKeys.Artifact.CONTENT]
        artifact = build_method(artifact_id=artifact_id, artifact_body=content, xml_tags=self.xml_tags,
                                include_id=self.include_id)
        return f"{prompt}{artifact}"

    @staticmethod
    def _build_as_xml(artifact_id: Union[int, str], artifact_body: str, xml_tags: Dict, include_id: bool = True) -> str:
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
        outer_tag = list(xml_tags.keys())[0]
        id_tag, body_tag = xml_tags[outer_tag]
        formatted_id = PromptUtil.create_xml(tag_name=id_tag, tag_content=artifact_id)
        formatted_content = PromptUtil.create_xml(tag_name=body_tag, tag_content=artifact_body) if include_id else artifact_body
        content_for_prompt = f"{NEW_LINE}{TAB}".join([formatted_id, formatted_content]) if include_id else formatted_content
        formatted_artifact = PromptUtil.create_xml(tag_name=outer_tag,
                                                   tag_content=f"{NEW_LINE}{TAB}{content_for_prompt}{NEW_LINE}")
        return formatted_artifact

    @staticmethod
    def _build_as_base(artifact_id: Union[int, str], artifact_body: str, include_id: bool = True, **kwargs) -> str:
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
