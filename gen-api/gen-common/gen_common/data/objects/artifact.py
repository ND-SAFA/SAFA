import uuid
from typing import List, Optional

from langchain_core.documents.base import Document

from gen_common.constants.symbol_constants import UNDERSCORE
from gen_common.data.keys.structure_keys import ArtifactKeys, StructuredKeys
from gen_common.data.objects.chunk import Chunk
from gen_common.util.dataframe_util import DataFrameUtil
from gen_common.util.enum_util import EnumDict
from gen_common.util.file_util import FileUtil
from gen_common.util.typed_enum_dict import TypedEnumDict


class Artifact(TypedEnumDict, keys=ArtifactKeys):
    """
    Typed entity representing single artifact entry.
    """
    id: str
    content: str
    layer_id: str
    summary: Optional[str]
    chunks: Optional[List[Chunk]]

    @staticmethod
    def get_summary_or_content(artifact: EnumDict, use_summary_for_code_only: bool = True) -> str:
        """
        Returns the summary if it exists else the content.
        :param artifact: The artifact whose summary or content is extracted.
        :param use_summary_for_code_only: If True, only uses the summary if the artifact is code.
        :return: The traceable string.
        """
        use_summary = FileUtil.is_code(artifact[ArtifactKeys.ID]) or not use_summary_for_code_only
        artifact_summary = DataFrameUtil.get_optional_value_from_df(artifact, StructuredKeys.Artifact.SUMMARY)
        if artifact_summary is None or not use_summary:
            return artifact[StructuredKeys.Artifact.CONTENT]
        return artifact_summary

    @staticmethod
    def get_chunks(artifact: EnumDict, use_summary_for_code_only: bool = True) -> List[str]:
        """
        Returns the chunks if it exists else the full content.
        :param artifact: The artifact whose chunks are extracted.
        :param use_summary_for_code_only: If True, only uses the summary if the artifact is code and there are no chunks.
        :return: The chunks..
        """
        chunks = DataFrameUtil.get_optional_value_from_df(artifact, StructuredKeys.Artifact.CHUNKS)
        if not chunks:
            chunks = [Artifact.get_summary_or_content(artifact, use_summary_for_code_only)]
        return chunks

    @staticmethod
    def get_chunk_id(orig_id: str, chunk_num: int) -> str:
        """
        Creates an id for an artifact chunk.
        :param orig_id: The id of the whole artifact.
        :param chunk_num: The number of the chunk.
        :return: An id for an artifact chunk.
        """
        return f"{orig_id}{UNDERSCORE}{chunk_num}"

    @staticmethod
    def convert_to_document(artifact: EnumDict) -> Document:
        """
        Converts an artifact into a langchain document.
        :param artifact: The artifact to convert.
        :return: Artifact as a langchain document.
        """
        document = Document(
            id=artifact[ArtifactKeys.ID],
            page_content=artifact[ArtifactKeys.CONTENT],
            metadata={k: v for k, v in artifact.items() if isinstance(v, str) and k != ArtifactKeys.CONTENT.value}
        )
        return document

    @staticmethod
    def convert_from_document(document: Document, generate_id_if_missing: bool = True) -> EnumDict:
        """
        Converts a langchain document  into an artifact.
        :param document: The document to convert to artifact.
        :param generate_id_if_missing: Ensures that the artifact has an id by creating one if it is missing from the metadata.
        :return: Langchain document as an artifact.
        """
        artifact = EnumDict(document.metadata)
        artifact[ArtifactKeys.CONTENT] = document.page_content
        if not artifact[ArtifactKeys.ID] and generate_id_if_missing:
            artifact[ArtifactKeys.ID] = str(uuid.uuid4())
        return artifact
