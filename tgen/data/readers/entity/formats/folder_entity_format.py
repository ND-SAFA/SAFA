import os
from typing import List

import pandas as pd
from tqdm import tqdm

from tgen.constants.dataset_constants import EXCLUDED_FILES
from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from tgen.data.summarizer.summarizer import Summarizer
from tgen.util.enum_util import EnumDict
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger


class FolderEntityFormat(AbstractEntityFormat):
    """
    Defines entity format that will read files in folder as artifacts using the file name
    as the id and the content as the body.
    """

    @classmethod
    def _parse(cls, data_path: str, summarizer: Summarizer = None, **params) -> pd.DataFrame:
        """
        Parses a data into DataFrame of entities.
        :param data_path: The path to the data to parse
        :param summarizer: If provided, will summarize the artifact content
        :return: DataFrame of parsed entities.
        """
        return FolderEntityFormat.read_folder(data_path, summarizer=summarizer, **params)

    @staticmethod
    def get_file_extensions() -> List[str]:
        """
        :return: Return empty list because this method should not have any associated file types.
        Note, This is kept to simplify iteration through formats.
        """
        return []

    @staticmethod
    def read_folder(path: str, exclude: List[str] = None, exclude_ext: List[str] = None, **kwargs) -> pd.DataFrame:
        """
        Creates artifact for each file in folder path.
        :param path: Path to folder containing artifact files.
        :param exclude: The files to exclude in folder path.
        :param exclude_ext: list of file extensions to exclude
        :return: DataFrame containing artifact ids and tokens.
        """
        exclude = EXCLUDED_FILES if exclude is None else exclude + EXCLUDED_FILES
        files_in_path = FileUtil.get_file_list(path, exclude=exclude, exclude_ext=exclude_ext)
        return FolderEntityFormat.read_files_as_artifacts(files_in_path, base_path=path, **kwargs)

    @staticmethod
    def read_files_as_artifacts(file_paths: List[str], base_path: str, use_file_name: bool = True,
                                with_extension: bool = True, summarizer: Summarizer = None) -> pd.DataFrame:
        """
        Reads file at each path and creates artifact with name
        :param file_paths: List of paths to file to read as artifacts
        :param base_path: The base path to use for all relative paths
        :param use_file_name: Whether to use file name as artifact id, otherwise file path is used.
        :param with_extension: Whether file extracted should contain its file extension.
        :param summarizer: If provided, will summarize the artifact content
        :return: DataFrame containing artifact properties id and body.
        """
        entries = []
        summarize_desc = "and summarizing" if summarizer is not None else EMPTY_STRING
        for file_path in tqdm(file_paths, f"Adding files as artifacts {summarize_desc}"):
            artifact_name = os.path.basename(file_path) if use_file_name else os.path.sep + os.path.relpath(file_path, base_path)
            if not with_extension:
                artifact_name = os.path.splitext(artifact_name)[0]
            entry = EnumDict({
                ArtifactKeys.ID: artifact_name,
                ArtifactKeys.CONTENT: FileUtil.read_file(file_path)
            })
            if summarizer is not None:
                chunker_type = SupportedChunker.determine_from_path(file_path)
                entry[ArtifactKeys.CONTENT] = summarizer.summarize_single(entry[ArtifactKeys.CONTENT], chunker_type, id_=file_path)
            if not entry[ArtifactKeys.CONTENT]:
                logger.warning(f"{artifact_name} does not contain any content. Skipping...")
                continue
            entries.append(entry)
        return pd.DataFrame(entries).sort_values([ArtifactKeys.ID.value], ignore_index=True)

    @staticmethod
    def performs_summarization() -> bool:
        """
        Returns True since summarizations are handled internally and do not need to be performed by parent
        :return: True
        """
        return True
