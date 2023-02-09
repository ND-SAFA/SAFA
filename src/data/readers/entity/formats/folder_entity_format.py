import os
from typing import List

import pandas as pd

from data.keys.structure_keys import StructuredKeys
from data.readers.entity.entity_parser_type import EntityParserType
from data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from util.file_util import FileUtil


class FolderEntityFormat(AbstractEntityFormat):
    """
    Defines entity format that will read files in folder as artifacts using the file name
    as the id and the content as the body.
    """

    @classmethod
    def get_parser(cls) -> EntityParserType:
        """
        :return: Returns custom method for reading folder as artifact entities.
        """
        return cls.read_folder

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
        files_in_path = FileUtil.get_file_list(path, exclude=exclude, exclude_ext=exclude_ext)
        return FolderEntityFormat.read_files_as_artifacts(files_in_path, base_path=path, **kwargs)

    @staticmethod
    def read_files_as_artifacts(file_paths: List[str], base_path: str, use_file_name: bool = True, with_extension: bool = True) -> pd.DataFrame:
        """
        Reads file at each path and creates artifact with name
        :param file_paths: List of paths to file to read as artifacts
        :param base_path: The base path to use for all relative paths
        :param use_file_name: Whether to use file name as artifact id, otherwise file path is used.
        :param with_extension: Whether file extracted should contain its file extension.
        :return: DataFrame containing artifact properties id and body.
        """
        entries = []
        for file_path in file_paths:
            artifact_name = os.path.basename(file_path) if use_file_name else os.path.sep + os.path.relpath(file_path, base_path)
            if not with_extension:
                artifact_name = os.path.splitext(artifact_name)[0]
            entry = {
                StructuredKeys.Artifact.ID: artifact_name,
                StructuredKeys.Artifact.BODY: FileUtil.read_file(file_path)
            }
            entries.append(entry)
        return pd.DataFrame(entries).sort_values([StructuredKeys.Artifact.ID], ignore_index=True)
