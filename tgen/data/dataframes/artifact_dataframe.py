from typing import Any, Dict, Iterable, List, Set, Tuple, Type, Union

from tgen.common.constants.anthropic_constants import ANTHROPIC_MAX_MODEL_TOKENS
from tgen.common.logging.logger_manager import logger
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.chunk import Chunk
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.str_util import StrUtil
from tgen.data.chunkers.abstract_chunker import AbstractChunker
from tgen.data.chunkers.sentence_chunker import SentenceChunker
from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, StructuredKeys, TraceKeys
from tgen.models.tokens.token_calculator import TokenCalculator
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.summarizer_util import SummarizerUtil


class ArtifactDataFrame(AbstractProjectDataFrame):
    """
    Contains the artifacts found in a project
    """

    OPTIONAL_COLUMNS = [StructuredKeys.Artifact.SUMMARY.value, StructuredKeys.Artifact.CHUNKS.value]
    DEFAULT_FOR_OPTIONAL_COLS = EnumDict({StructuredKeys.Artifact.SUMMARY: None, StructuredKeys.Artifact.CHUNKS: None})

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

    def add_artifact(self, a_id: Any, content: str, layer_id: Any = "1",
                     summary: str = DEFAULT_FOR_OPTIONAL_COLS[ArtifactKeys.SUMMARY],
                     chunks: List[str] = DEFAULT_FOR_OPTIONAL_COLS[ArtifactKeys.CHUNKS]) -> EnumDict:
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
        return self.add_row(row_as_dict)

    def get_artifact(self, artifact_id: Any, throw_exception: bool = False) -> EnumDict:
        """
        Gets the row of the dataframe with the associated artifact_id
        :param artifact_id: The id of the artifact to get
        :param throw_exception: If True, throws exception if artifact is missing.
        :return: The artifact if one is found with the specified params, else None
        """
        return self.get_row(artifact_id, throw_exception)

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

    def to_artifacts(self) -> List[Artifact]:
        """
        Converts entries in data frame to converts.
        :return: The list of artifacts.
        """
        artifacts = [Artifact(**artifact_row) for artifact_id, artifact_row in self.itertuples()]
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
        if re_summarize or not self.is_summarized(code_or_above_limit_only=summarizer.code_or_above_limit_only):
            missing_all = self[ArtifactKeys.SUMMARY].isna().all() or re_summarize
            if missing_all:
                summaries = summarizer.summarize_dataframe(self, ArtifactKeys.CONTENT.value, ArtifactKeys.ID.value)
                self[ArtifactKeys.SUMMARY] = summaries
            else:
                ids, content = self._find_missing_summaries()
                summaries = summarizer.summarize_bulk(bodies=content, ids=ids, use_content_if_unsummarized=False)
                self.update_values(ArtifactKeys.SUMMARY, ids, summaries)
        return self[ArtifactKeys.SUMMARY]

    def is_summarized(self, layer_ids: Union[str, Iterable[str]] = None, code_or_above_limit_only: bool = False) -> bool:
        """
        Checks if the artifacts (or artifacts in given layer) are summarized
        :param layer_ids: The layer to check if it is summarized
        :param code_or_above_limit_only: If True, only checks that code artifacts are summarized.
        :return: True if the artifacts (or artifacts in given layer) are summarized
        """
        if not layer_ids and code_or_above_limit_only:
            layer_ids = self.get_code_layers()
        if not isinstance(layer_ids, set):
            layer_ids = set(layer_ids) if isinstance(layer_ids, list) else {layer_ids}
        for layer_id in layer_ids:
            df = self if layer_id is None else self.get_artifacts_by_type(layer_id)
            summaries = df[ArtifactKeys.SUMMARY.value]
            missing_summaries = [self.get_row(i)[ArtifactKeys.ID] for i in DataFrameUtil.find_nan_empty_indices(summaries)]
            missing_summaries = [a_id for a_id in missing_summaries if FileUtil.is_code(a_id) or not code_or_above_limit_only]
            if len(missing_summaries) > 0:
                return False

        for artifact in self.to_artifacts():
            artifact_content = artifact[ArtifactKeys.CONTENT]
            has_summary = isinstance(artifact[ArtifactKeys.SUMMARY], str)
            if SummarizerUtil.is_above_limit(artifact_content) and not has_summary:
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

    def drop_large_files(self) -> None:
        """
        Removes files that are too large for prompt from data frame.
        :return: None
        """
        large_file_ids = self.identify_large_files(self)
        if len(large_file_ids) > 0:
            self.drop(index=large_file_ids, inplace=True)
            logger.info(f"Files are too large for generations: {large_file_ids}")

    @staticmethod
    def identify_large_files(artifact_df: "ArtifactDataFrame") -> Set[int]:
        """
        Identifies and removes files from project that are too large for current models.
        :param artifact_df: The artifact data frame to filter.
        :return: Indices of files extending beyond model limit.
        """
        large_file_ids = set()
        for artifact in artifact_df.to_artifacts():
            a_id = artifact[ArtifactKeys.ID]
            artifact_content = artifact[ArtifactKeys.CONTENT]
            n_tokens = TokenCalculator.estimate_num_tokens(artifact_content)
            if n_tokens > ANTHROPIC_MAX_MODEL_TOKENS:
                large_file_ids.add(a_id)
        return large_file_ids

    def chunk(self, chunker: AbstractChunker = None, artifact_ids: Set[str] = None,
              unchunked_only: bool = True) -> Dict[str, List[str]]:
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

    def get_chunk_map(self, orig_artifact_ids: Set[str] = None, use_code_summary_only: bool = True) -> Dict[str, str]:
        """
        Gets a map of artifact id to a list of its chunks.
        :param orig_artifact_ids: If provided, only retrieves chunks for given artifacts.
        :param use_code_summary_only: If True, only uses the summary if the artifact is code and there are no chunks.
        :return: Returns a map of artifact id to a list of its chunks.
        """
        orig_artifact_ids = set(self.index) if not orig_artifact_ids else orig_artifact_ids
        chunk_map = {Chunk.get_chunk_id(name, i): chunk for name, a in self.itertuples()
                     for i, chunk in enumerate(Artifact.get_chunks(a, use_code_summary_only))
                     if DataFrameUtil.get_optional_value_from_df(a, ArtifactKeys.CHUNKS) and name in orig_artifact_ids}
        return chunk_map

    def get_artifact_from_chunk_id(self, c_id: str, id_only: bool = False, raise_exception: bool = False) -> Union[str, Artifact]:
        """
        Gets the id of the whole artifact.
        :param c_id: The id of the artifact/chunk.
        :param id_only: If True, only returns the id of the artifact.
        :param raise_exception: If True, raises an exception if the artifact does not exist.
        :return: The id of the whole artifact.
        """
        artifact = self.get_artifact(c_id)
        if artifact is None:
            a_id = Chunk.get_base_id(c_id)
            artifact = self.get_artifact(a_id)
        if artifact:
            return artifact if not id_only else artifact[ArtifactKeys.ID]
        if raise_exception:
            raise KeyError("Unknown artifact")

    def get_chunk_by_id(self, chunk_id: str, raise_exception: bool = False) -> str:
        """
        Gets the chunk number from the id.
        :param chunk_id: The id of the chunk.
        :param raise_exception: If True, raises exception if the chunk does not exist.
        :return: The number of the chunk.
        """
        artifact = self.get_artifact_from_chunk_id(chunk_id, raise_exception=raise_exception)

        if artifact:
            chunk_num = Chunk.get_chunk_num(chunk_id, artifact[ArtifactKeys.ID])
            chunks = artifact.get(ArtifactKeys.CHUNKS, [])
            if chunk_num and chunk_num < len(chunks):
                return chunks[chunk_num]

        if raise_exception:
            raise KeyError(f"Unknown artifact or chunk {chunk_id}")

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
