from typing import Any, Dict, Iterable, List, Set, Tuple, Type, Union, Optional

from tgen.common.constants.deliminator_constants import UNDERSCORE
from tgen.common.objects.artifact import Artifact
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.override import overrides
from tgen.common.util.str_util import StrUtil
from tgen.data.chunkers.abstract_chunker import AbstractChunker
from tgen.data.chunkers.sentence_chunker import SentenceChunker
from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, StructuredKeys, TraceKeys
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer


class ArtifactDataFrame(AbstractProjectDataFrame):
    """
    Contains the artifacts found in a project
    """

    OPTIONAL_COLUMNS = [StructuredKeys.Artifact.SUMMARY.value, StructuredKeys.Artifact.CHUNKS.value]
    _DEFAULT_FOR_OPTIONAL_COLS = None

    @overrides(AbstractProjectDataFrame)
    def process_data(self) -> None:
        """
        Sets the index of the dataframe and performs any other processing steps
        :return: None
        """
        super().process_data()
        if not self.empty:
            for col in self.OPTIONAL_COLUMNS:
                if col not in self.columns:
                    self[col] = [self._DEFAULT_FOR_OPTIONAL_COLS for _ in self.index]

    @classmethod
    def index_name(cls) -> str:
        """
        Returns the name of the index of the dataframe
        :return: The name of the index of the dataframe
        """
        return ArtifactKeys.ID.value

    @classmethod
    def data_keys(cls) -> Type:
        """
        Returns the class containing the names of all columns in the dataframe
        :return: The class containing the names of all columns in the dataframe
        """
        return ArtifactKeys

    def get_summaries_or_contents(self, artifact_ids: List[Any] = None, use_summary_for_code_only: bool = True) -> List[str]:
        """
        Returns the summary for each artifact if it exists else the content.
        :param artifact_ids: The list of artifact ids whose summary or content is return.
        :param use_summary_for_code_only: If True, only uses the summary if the artifact is code.
        :return: The list of contents or summaries.
        """
        artifact_df = self.filter_by_index(artifact_ids) if artifact_ids else self
        contents = []
        for _, artifact in artifact_df.itertuples():
            content = Artifact.get_summary_or_content(artifact, use_summary_for_code_only=use_summary_for_code_only)
            contents.append(content)
        return contents

    def add_artifacts(self, artifacts: List[Artifact]) -> None:
        """
        Adds artifacts to data frame.
        :param artifacts: The artifacts to add.
        :return: None
        """
        for a in artifacts:
            self.add_artifact(**a)

    def add_artifact(self, a_id: Any, content: str, layer_id: Any = "1", summary: str = _DEFAULT_FOR_OPTIONAL_COLS,
                     chunks: List[str] = _DEFAULT_FOR_OPTIONAL_COLS) -> EnumDict:
        """
        Adds artifact to dataframe
        :param a_id: The id of the Artifact
        :param content: The body of the artifact
        :param layer_id: The id of the layer that the artifact is part of
        :param summary: The summary of the artifact body
        :param chunks: The chunks that the artifact has been split into
        :return: The newly added artifact
        """
        row_as_dict = {ArtifactKeys.ID: a_id, ArtifactKeys.CONTENT: content, ArtifactKeys.LAYER_ID: layer_id,
                       ArtifactKeys.SUMMARY: summary, ArtifactKeys.CHUNKS: chunks}
        return self.add_or_update_row(row_as_dict)

    def get_artifact(self, artifact_id: Any, throw_exception: bool = False) -> EnumDict:
        """
        Gets the row of the dataframe with the associated artifact_id
        :param artifact_id: The id of the artifact to get
        :param throw_exception: If True, throws exception if artifact is missing.
        :return: The artifact if one is found with the specified params, else None
        """
        return self.get_row(artifact_id, throw_exception)

    def get_chunk_by_id(self, chunk_id: Any, throw_exception: bool = False) -> str:
        """
        Gets the chunk with the associated chunk
        :param chunk_id: The id of the chunk to get
        :param throw_exception: If True, throws exception if chunk does not exist.
        :return: The chunk if one is found with the specified params, else None
        """
        a_id = self.get_orig_id(chunk_id)
        artifact = self.get_artifact(a_id, throw_exception)
        if artifact:
            chunk_num = self.get_chunk_num(chunk_id)
            return artifact[ArtifactKeys.CHUNKS][chunk_num] if chunk_num else None

    def get_artifacts_from_trace(self, trace: EnumDict) -> Tuple[EnumDict, EnumDict]:
        """
        Gets the source and target artifacts from a trace dict
        :param trace: The trace link represented as a dict
        :return: The source and target artifacts
        """
        return self.get_artifact(trace[TraceKeys.SOURCE]), self.get_artifact(trace[TraceKeys.TARGET])

    def get_artifacts_by_type(self, artifact_types: Union[str, List[str]]) -> "ArtifactDataFrame":
        """
        Returns data frame with artifacts of given type.
        :param artifact_types: The type to filter by.
        :return: Artifacts in data frame of given type.
        """
        if isinstance(artifact_types, str):
            artifact_types = [artifact_types]
        all_types_df = ArtifactDataFrame()
        for type_name in artifact_types:
            curr_type_df = self.filter_by_row(lambda r: r[ArtifactKeys.LAYER_ID.value] == type_name)
            all_types_df = ArtifactDataFrame.concat(all_types_df, curr_type_df)
        return all_types_df

    def get_type_counts(self) -> Dict[str, str]:
        """
        Returns how many artifacts of each type exist in data frame.
        :return: map between type to number of artifacts of that type.
        """
        counts_df = self[ArtifactKeys.LAYER_ID].value_counts()
        type2count = dict(counts_df)
        return type2count

    def get_artifact_types(self) -> List[str]:
        """
        :return: Returns list of unique artifact types in data frame.
        """
        return list(self[ArtifactKeys.LAYER_ID].unique())

    def to_map(self, use_code_summary_only: bool = True, include_chunks: bool = False) -> Dict[str, str]:
        """
        :param use_code_summary_only: If True, only uses the summary if the artifact is code.
        :param include_chunks: If True, chunks are included in the content map.
        :return: Returns map of artifact ids to content.
        """
        artifact_map = {}
        for name, row in self.itertuples():
            content = Artifact.get_summary_or_content(row, use_code_summary_only)
            if content is None or len(content) == 0:
                content = row[ArtifactKeys.CONTENT]
            artifact_map[name] = content
        if include_chunks:
            chunk_map = self.get_chunk_map(use_code_summary_only=use_code_summary_only)
            artifact_map.update(chunk_map)
        return artifact_map

    def get_chunk_map(self, orig_artifact_ids: Set[str] = None, use_code_summary_only: bool = True) -> Dict[str, str]:
        """
        Gets a map of artifact id to a list of its chunks.
        :param orig_artifact_ids: If provided, only retrieves chunks for given artifacts.
        :param use_code_summary_only: If True, only uses the summary if the artifact is code and there are no chunks.
        :return: Returns a map of artifact id to a list of its chunks.
        """
        orig_artifact_ids = set(self.index) if not orig_artifact_ids else orig_artifact_ids
        chunk_map = {self.get_chunk_id(name, i): chunk for name, a in self.itertuples()
                     for i, chunk in enumerate(Artifact.get_chunks(a, use_code_summary_only))
                     if DataFrameUtil.get_optional_value_from_df(a, ArtifactKeys.CHUNKS) and name in orig_artifact_ids}
        return chunk_map

    def chunk(self, chunker: AbstractChunker = None, artifact_ids: Set[str] = None, unchunked_only: bool = True) -> Dict[
        str, List[str]]:
        """
        Breaks artifacts in dataframe into smaller chunks.
        :param chunker: The Chunker to use.
        :param artifact_ids: Specific artifacts to chunk (all by default).
        :param unchunked_only: If True, only chunks artifacts that dont already have chunks.
        :return: Dictionary mapping artifact id to the chunks.
        """
        chunker = SentenceChunker() if not chunker else chunker
        already_chunked = {i for i, a in self.itertuples()
                           if len(StrUtil.split_by_punctuation(Artifact.get_summary_or_content(a))) == 1}
        if unchunked_only:
            already_chunked.update({i for i, a in self.itertuples()
                                    if DataFrameUtil.get_optional_value_from_df(a, ArtifactKeys.CHUNKS)})
        artifact_ids = set(self.index) if not artifact_ids else artifact_ids
        artifact_ids = artifact_ids.difference(already_chunked)
        artifacts2chunk = [a for _, a in self.filter_by_index(list(artifact_ids)).itertuples()]
        chunks = chunker.chunk(artifacts2chunk)
        self.update_values(ArtifactKeys.CHUNKS, [a[ArtifactKeys.ID] for a in artifacts2chunk], chunks)
        return self.get_chunk_map(artifact_ids)

    def get_orig_id(self, a_id: str) -> str:
        """
        Gets the id of the whole artifact.
        :param a_id: The id of the artifact/chunk.
        :return: The id of the whole artifact.
        """
        if a_id in self:
            return a_id  # ensures this was the original id and not another id with an underscore
        split_id = a_id.split(UNDERSCORE)
        if len(split_id) > 1:
            orig_id = UNDERSCORE.join(split_id[:-1])
            return orig_id
        raise NameError("Unknown artifact")

    def is_chunk(self, a_id: str) -> bool:
        """
        Returns True if the artifact id is associated with a chunk else False.
        :param a_id: The id of the artifact/chunk.
        :return: True if the artifact id is associated with a chunk else False.
        """
        return self.get_chunk_num(a_id) is not None

    def get_chunk_num(self, chunk_id: str) -> Optional[int]:
        """
        Gets the chunk number from the id.
        :param chunk_id: The id of the chunk.
        :return: The number of the chunk.
        """
        orig_id = self.get_orig_id(chunk_id)
        artifact = self.get_artifact(orig_id)
        assert artifact is not None, "Unknown artifact"
        if orig_id == chunk_id:
            return
        try:
            chunk_num = int(StrUtil.remove_substrings(chunk_id, [orig_id, UNDERSCORE]))
            assert chunk_num < len(artifact[ArtifactKeys.CHUNKS])
            return chunk_num
        except (ValueError, AssertionError):
            raise NameError("Chunk does not exist")

    @staticmethod
    def get_chunk_id(orig_id: str, chunk_num: int) -> str:
        """
        Creates an id for an artifact chunk.
        :param orig_id: The id of the whole artifact.
        :param chunk_num: The number of the chunk.
        :return: An id for an artifact chunk.
        """
        return f"{orig_id}{UNDERSCORE}{chunk_num}"

    def to_artifacts(self) -> List[Artifact]:
        """
        Converts entries in data frame to converts.
        :return: The list of artifacts.
        """
        artifacts = [Artifact(id=artifact_id,
                              content=artifact_row[ArtifactKeys.CONTENT],
                              layer_id=artifact_row[ArtifactKeys.LAYER_ID],
                              summary=artifact_row[ArtifactKeys.SUMMARY],
                              chunks=artifact_row[ArtifactKeys.CHUNKS])
                     for artifact_id, artifact_row in self.itertuples()]
        return artifacts

    def get_body(self, artifact_id: str) -> str:
        """
        Retrieves the body of the artifact with given ID.
        :param artifact_id: The ID of the artifact.
        :return: The content of the artifact.
        """
        return self.loc[artifact_id][ArtifactKeys.CONTENT.value]

    def set_body(self, artifact_id: str, new_body: str) -> None:
        """
        Sets the body of the artifact with given ID.
        :param artifact_id: The id of the artifact.
        :param new_body: The body to update the artifact with.
        :return: None 
        """
        self.loc[artifact_id][ArtifactKeys.CONTENT.value] = new_body

    def summarize_content(self, summarizer: ArtifactsSummarizer, re_summarize: bool = False) -> List[str]:
        """
        Summarizes the content in the artifact df
        :param summarizer: The summarizer to use
        :param re_summarize: True if old summaries should be replaced
        :return: The summaries
        """
        if re_summarize or not self.is_summarized(code_only=summarizer.code_or_above_limit_only):
            missing_all = self[ArtifactKeys.SUMMARY].isna().all() or re_summarize
            if missing_all:
                summaries = summarizer.summarize_dataframe(self, ArtifactKeys.CONTENT.value, ArtifactKeys.ID.value)
                self[ArtifactKeys.SUMMARY] = summaries
            else:
                ids, content = self._find_missing_summaries()
                summaries = summarizer.summarize_bulk(bodies=content, ids=ids, use_content_if_unsummarized=False)
                self.update_values(ArtifactKeys.SUMMARY, ids, summaries)
        return self[ArtifactKeys.SUMMARY]

    def is_summarized(self, layer_ids: Union[str, Iterable[str]] = None, code_only: bool = False) -> bool:
        """
        Checks if the artifacts (or artifacts in given layer) are summarized
        :param layer_ids: The layer to check if it is summarized
        :param code_only: If True, only checks that artifacts that are code are summarized
        :return: True if the artifacts (or artifacts in given layer) are summarized
        """
        if not layer_ids and code_only:
            layer_ids = self.get_code_layers()
        if not isinstance(layer_ids, set):
            layer_ids = set(layer_ids) if isinstance(layer_ids, list) else {layer_ids}
        for layer_id in layer_ids:
            df = self if layer_id is None else self.get_artifacts_by_type(layer_id)
            summaries = df[ArtifactKeys.SUMMARY.value]
            missing_summaries = [self.get_row(i)[ArtifactKeys.ID] for i in DataFrameUtil.find_nan_empty_indices(summaries)]
            missing_summaries = [a_id for a_id in missing_summaries if FileUtil.is_code(a_id) or not code_only]
            if len(missing_summaries) > 0:
                return False
        return True

    def get_code_layers(self) -> Set[str]:
        """
        Gets the id of all code layers
        :return: A set of the ids of all code layers
        """
        code_layers = set()
        for i, artifact in self.itertuples():
            if FileUtil.is_code(i):
                code_layers.add(artifact[ArtifactKeys.LAYER_ID])
        return code_layers

    def _find_missing_summaries(self) -> Tuple[List, List]:
        """
        Finds artifacts that are missing summaries
        :return: The ids and content of the missing summaries
        """
        ids = []
        content = []
        for i, artifact in self.itertuples():
            if not DataFrameUtil.get_optional_value(artifact[ArtifactKeys.SUMMARY]):
                ids.append(i)
                content.append(artifact[ArtifactKeys.CONTENT])
        return ids, content
