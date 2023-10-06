from enum import Enum, auto
from typing import Union, Dict, List, Optional

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE, TAB
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.trace_dataframe import TraceKeys
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
        MARKDOWN = auto()
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
            self.BuildMethod.BASE: self._build_as_base,
            self.BuildMethod.MARKDOWN: self._build_as_markdown
        }
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
        content = DataFrameUtil.get_optional_value(artifact.get(StructuredKeys.Artifact.SUMMARY, None))
        relation = self.get_relationship(artifact)
        if not content:
            content = artifact[StructuredKeys.Artifact.CONTENT]
        artifact = build_method(artifact_id=artifact_id, artifact_body=content, xml_tags=self.xml_tags,
                                include_id=self.include_id, relation=relation, **kwargs)
        return f"{prompt}{artifact}"

    @staticmethod
    def get_relationship(artifact: Dict) -> Optional[str]:
        """
        Gets the relationship of the artifact (parent or child) if provided
        :param artifact: Dictionary containing artifact attributes
        :return: The relationship of the artifact (parent or child) if provided
        """
        relation = None
        if artifact.get(TraceKeys.child_label().value, False):
            relation = "child"
        elif artifact.get(TraceKeys.parent_label().value, False):
            relation = "parent"
        return relation

    @staticmethod
    def _build_as_xml(artifact_id: Union[int, str], artifact_body: str, xml_tags: Dict, include_id: bool = True, **kwargs) -> str:
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
    def _build_as_markdown(artifact_id: Union[int, str], artifact_body: str, relation: str,
                           include_id: bool = True, header_level: int = 1, **kwargs) -> str:
        """
        Formats the artifact as follows:
        # id
            body
        :param artifact_id: The id of the artifact
        :param artifact_body: The body of the artifact
        :param relation: The relationship of the artifact (parent or child) if provided
        :param include_id: Whether to include id or not
        :return: The formatted prompt
        """
        artifact_id = relation if relation and not include_id else artifact_id
        assert artifact_id, f"Building artifact as {ArtifactPrompt.BuildMethod.MARKDOWN.name} requires an artifact id to be given."

        header = PromptUtil.as_markdown_header(original_string=artifact_id.capitalize(), level=header_level)
        content = PromptUtil.indent_for_markdown(artifact_body)
        return f"{header}{NEW_LINE}{content}"

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
