import os
from typing import List, Tuple

import pandas as pd

from common_resources.tools.constants.dataset_constants import EXCLUDED_FILES
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.file_util import FileUtil
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from common_resources.data.summarizer.artifacts_summarizer import ArtifactsSummarizer


class FolderEntityFormat(AbstractEntityFormat):
    """
    Defines entity format that will read files in folder as artifacts using the file name
    as the id and the content as the body.
    """

    @classmethod
    def _parse(cls, data_path: str, summarizer: ArtifactsSummarizer = None, **params) -> pd.DataFrame:
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
    def read_folder(path: str, exclude: List[str] = None, exclude_ext: List[str] = None, with_extension: bool = True,
                    **kwargs) -> pd.DataFrame:
        """
        Creates artifact for each file in folder path.
        :param path: Path to folder containing artifact files.
        :param exclude: The files to exclude in folder path.
        :param exclude_ext: list of file extensions to exclude
        :param with_extension: Whether to include file extension in artifact ids.
        :return: DataFrame containing artifact ids and tokens.
        """
        exclude = EXCLUDED_FILES if exclude is None else exclude + EXCLUDED_FILES
        files_in_path = FileUtil.get_file_list(path, exclude=exclude, exclude_ext=exclude_ext)
        return FolderEntityFormat.read_files_as_artifacts(files_in_path, base_path=path, with_extension=with_extension, **kwargs)

    @staticmethod
    def read_files_as_artifacts(file_paths: List[str], base_path: str, use_file_name: bool = True,
                                with_extension: bool = True, summarizer: ArtifactsSummarizer = None) -> pd.DataFrame:
        """
        Reads file at each path and creates artifact with name
        :param file_paths: List of paths to file to read as artifacts
        :param base_path: The base path to use for all relative paths
        :param use_file_name: Whether to use file name as artifact id, otherwise file path is used.
        :param with_extension: Whether file extracted should contain its file extension.
        :param summarizer: If provided, will summarize the artifact content
        :return: DataFrame containing artifact properties id and body.
        """
        artifact_names = []
        contents = []
        for file_path in file_paths:
            artifact_name = os.path.basename(file_path) if use_file_name else os.path.sep + os.path.relpath(file_path, base_path)
            if not with_extension:
                artifact_name = os.path.splitext(artifact_name)[0]
            artifact_names.append(artifact_name)
            contents.append(FileUtil.read_file(file_path))

        artifact_names, contents = FolderEntityFormat._remove_empty_contents(artifact_names, contents)
        summaries = summarizer.summarize_bulk(bodies=contents, ids=artifact_names) \
            if summarizer is not None else None
        entries = EnumDict({
            ArtifactKeys.ID: artifact_names,
            ArtifactKeys.CONTENT: contents
        })
        if summaries:
            entries[ArtifactKeys.SUMMARY] = summaries
        return pd.DataFrame(entries).sort_values([ArtifactKeys.ID.value], ignore_index=True)

    @staticmethod
    def performs_summarization() -> bool:
        """
        Returns True since summarizations are handled internally and do not need to be performed by parent
        :return: True
        """
        return True

    @staticmethod
    def _remove_empty_contents(artifact_names: List[str], contents: List[str]) -> Tuple[List[str], List[str]]:
        """
        Removes artifact names and content if the content is empty
        :param artifact_names: Names of the artifacts
        :param contents: Contents of the artifacts
        :return: The names and contents with all artifacts with empty content removed
        """
        missing_content = {i for i, content in enumerate(contents) if not content}
        artifact_names = [name for i, name in enumerate(artifact_names) if i not in missing_content]
        contents = [content for i, content in enumerate(contents) if i not in missing_content]
        for i in missing_content:
            logger.warning(f"{artifact_names[i]} does not contain any content. Skipping...")
            continue
        return artifact_names, contents
