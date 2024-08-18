from collections.abc import Set
from typing import Dict, List

from gen_common.data.chunkers.abstract_chunker import AbstractChunker
from gen_common.data.chunkers.sentence_chunker import SentenceChunker
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.util.dataframe_util import DataFrameUtil
from gen_common.util.str_util import StrUtil


def chunk_artifact_df(df: ArtifactDataFrame, chunker: AbstractChunker = None, artifact_ids: Set[str] = None,
                      unchunked_only: bool = True) -> Dict[str, List[str]]:
    """
    Breaks artifacts in dataframe into smaller chunks.
    :param df: The data frame to chunk
    :param chunker: The Chunker to use.
    :param artifact_ids: Specific artifacts to chunk (all by default).
    :param unchunked_only: If True, only chunks artifacts that dont already have chunks.
    :return: Dictionary mapping artifact id to the chunks.
    """
    chunker = SentenceChunker() if not chunker else chunker
    already_chunked = {i for i, a in df.itertuples()
                       if len(StrUtil.split_by_punctuation(Artifact.get_summary_or_content(a))) == 1}
    if unchunked_only:
        already_chunked.update({i for i, a in df.itertuples()
                                if DataFrameUtil.get_optional_value_from_df(a, ArtifactKeys.CHUNKS)})
    artifact_ids = set(df.index) if not artifact_ids else artifact_ids
    artifact_ids = artifact_ids.difference(already_chunked)
    artifacts2chunk = [a for _, a in df.filter_by_index(list(artifact_ids)).itertuples()]
    chunks = chunker.chunk(artifacts2chunk)
    df.update_values(ArtifactKeys.CHUNKS, [a[ArtifactKeys.ID] for a in artifacts2chunk], chunks)
    return df.get_chunk_map(artifact_ids)
