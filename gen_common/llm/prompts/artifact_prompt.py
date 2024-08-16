from enum import Enum, auto
from typing import Dict, List, Optional, Union

from gen_common.constants import EMPTY_STRING, NEW_LINE, TAB, USE_NL_SUMMARY_PROMPT
from gen_common.data.keys.structure_keys import ArtifactKeys, StructuredKeys, TraceKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.util import EnumDict, PromptUtil
from gen_common.util.override import overrides


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

    def __init__(self, prompt_start: str = EMPTY_STRING, prompt_args: PromptArgs = None, build_method: BuildMethod = BuildMethod.BASE,
                 include_id: bool = True, xml_tags: Dict[str, List[str]] = None, use_summary: bool = True):
        """
        Constructor for making a prompt from an artifact
        :param prompt_start: Goes before the artifact.
        :param prompt_args: The args to the base prompt.
        :param build_method: The method to build the prompt (determines prompt format)
        :param xml_tags: If building using XML, specify the names of the tags as such {outer_tag: [id_tag, body_tag]}
        :param use_summary: If True, won't use the artifact's summary when constructing
        :param include_id: If True, includes the id of the artifact
        """
        self.xml_tags = xml_tags if xml_tags else self.DEFAULT_XML_TAGS
        self.build_method = build_method
        self.build_methods = {
            self.BuildMethod.XML: self._build_as_xml,
            self.BuildMethod.BASE: self._build_as_base,
            self.BuildMethod.MARKDOWN: self._build_as_markdown
        }
        self.use_summary = use_summary
        self.include_id = include_id
        prompt_args = PromptArgs() if not prompt_args else prompt_args
        prompt_args.allow_formatting = False
        super().__init__(value=prompt_start, prompt_args=prompt_args)

    @overrides(Prompt)
    def _build(self, artifact: EnumDict, structure: bool = True, **kwargs) -> str:
        """
        Builds the artifact prompt using the given build method
        :param artifact: The dictionary containing the attributes representing an artifact
        :param structure: Kept for API purposes.
        :param kwargs: Additional build formatting.
        :return: The formatted prompt
        """
        prompt = super()._build(structure=True, **kwargs)
        if self.build_method not in self.build_methods:
            raise NameError(f"Unknown Build Method: {self.build_method}")
        build_method = self.build_methods[self.build_method]
        artifact_id = artifact.get(StructuredKeys.Artifact.ID.value, EMPTY_STRING)
        relation = self.get_relationship(artifact)
        if not self.use_summary:
            content = artifact[StructuredKeys.Artifact.CONTENT]
        else:
            content = Artifact.get_summary_or_content(artifact, use_summary_for_code_only=not USE_NL_SUMMARY_PROMPT)

        layer_id = artifact.get(ArtifactKeys.LAYER_ID.value)
        if layer_id:
            kwargs[ArtifactKeys.LAYER_ID.value] = layer_id

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
            relation = "Child"
        elif artifact.get(TraceKeys.parent_label().value, False):
            relation = "Parent"
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
        :param xml_tags: The tags defining how to wrap artifact id and content.
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
        :param header_level: The header level used to print each artifact ID.
        :return: The formatted prompt
        """
        if relation:
            if not include_id or not artifact_id:
                artifact_id = relation
                include_id = True
            elif artifact_id:
                artifact_id = f"{artifact_id} ({relation})"
        header = f"{PromptUtil.as_markdown_header(original_string=artifact_id, level=header_level)}" if include_id else EMPTY_STRING
        if header and ArtifactKeys.LAYER_ID.value in kwargs:
            header += f" ({kwargs[ArtifactKeys.LAYER_ID.value]})"
        content = PromptUtil.indent_for_markdown(artifact_body, level=2)
        return f"{header}{NEW_LINE}{content}" if header else content

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
