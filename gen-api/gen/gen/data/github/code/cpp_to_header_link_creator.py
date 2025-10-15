import os
from typing import Dict, List, Optional, Tuple

from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.file_util import FileUtil

from gen.data.github.abstract_github_entity import AbstractGithubArtifact
from gen.data.github.gartifacts.gcode_file import GCodeFile
from gen.data.github.gtraces.glink import GLink

ARTIFACTS_TYPE = Dict[str, GCodeFile]
LINKS_TYPE = Dict[str, GLink]


class CPPToHeaderLinkCreator:
    """
    Constructs links between .cpp files and their header files (.hpp).
    """
    CPP_FOLDER_NAME = "source"
    HEADER_FOLDER_NAME = "include"
    HEADER_EXT = "hpp"
    CPP_EXT = "cpp"

    def __init__(self, cpp_file_paths: List[str], base_path: str):
        """
        Responsible for linking CPP files to their header file
        :param cpp_file_paths: A list of cpp file paths to create links for.
        :param base_path: Path to base project.
        """
        self.cpp_file_paths = cpp_file_paths
        self.base_path = base_path
        self._artifacts: ARTIFACTS_TYPE = {}
        self._links: LINKS_TYPE = {}

    def create_links(self, verbose: bool = False) -> Tuple[ARTIFACTS_TYPE, LINKS_TYPE]:
        """
        Creates links between CPP files and the corresponding Header file
        :param verbose: Whether to include all logs.
        :return a dictionary mapping id to artifact and a dictionary mapping id to link
        """
        if len(self._links) < 1:
            for cpp_file_path in self.cpp_file_paths:
                try:
                    header_path = self._get_header_path(cpp_file_path)
                    assert header_path is not None, "No header exists for the file."
                    cpp_file = GCodeFile(cpp_file_path, self.base_path)
                    hpp_file = GCodeFile(header_path, self.base_path)
                    self._add_artifact_to_dict(cpp_file, self._artifacts)
                    self._add_artifact_to_dict(hpp_file, self._artifacts)
                    self._add_artifact_to_dict(GLink(cpp_file.get_id(), hpp_file.get_id()), self._links)
                except Exception as e:
                    if verbose:
                        logger.warning(f"Unable to create link for {cpp_file_path} because {e}")
        return self._artifacts, self._links

    @staticmethod
    def from_dir_path(dir_path: str, base_path: str) -> "CPPToHeaderLinkCreator":
        """
        Creates a link creator from all the cpp files in a directory
        :param dir_path: The path to the directory containing cpp files
        :param base_path: The base path to remove from dir_path for use in code IDs.
        :return A link creator from all the cpp files in a directory
        """
        cpp_files = CPPToHeaderLinkCreator._get_all_cpp_files_in_dir(dir_path)
        return CPPToHeaderLinkCreator(cpp_files, base_path)

    @staticmethod
    def _add_artifact_to_dict(artifact: AbstractGithubArtifact, dict_: Dict[str, AbstractGithubArtifact]) -> None:
        """
        Adds the artifact to the dictionary mapping artifact id to artifact
        :param artifact: The artifact to add
        :param dict_: The dictionary to add the artifact to
        :return None
        """
        dict_[artifact.get_id()] = artifact

    @staticmethod
    def _get_header_path(cpp_file_path: str) -> str:
        """
        Gets the path to the header file corresponding with the cpp file, if one exists
        :param cpp_file_path: The path to the cpp file
        :return The path to the corresponding header file if one exists
        """
        module_path, code_path, filename = CPPToHeaderLinkCreator._get_cpp_file_path_parts(cpp_file_path)
        header_file_name = f"{filename}.{CPPToHeaderLinkCreator.HEADER_EXT}"
        header_base_path = os.path.join(module_path, CPPToHeaderLinkCreator.HEADER_FOLDER_NAME)
        return CPPToHeaderLinkCreator._find_header_file(header_base_path, header_file_name)

    @staticmethod
    def _find_header_file(dir_path: str, header_file_name: str) -> Optional[str]:
        """
        Finds the expected header file in the directory, if once exists
        :param dir_path: The path to the header folder
        :param header_file_name: The expected name of the header file
        :return The path to the header if one exists
        """
        for file_name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, file_name)
            if file_name == header_file_name:
                return full_path
            if os.path.isdir(full_path):
                header_file_path = CPPToHeaderLinkCreator._find_header_file(full_path, header_file_name)
                if header_file_path is not None:
                    return header_file_path

    @staticmethod
    def _get_cpp_file_path_parts(cpp_file_path: str) -> Tuple[str, str, str]:
        """
        Breaks the file_path into 3 parts - path to the module, path to the specific code file (expected to be same in both the header
        and source folder, and the filename (w/o ext)
        :param cpp_file_path: The full file_path
        :return the module and code path and filename without ext
        """
        base_path, filename = CPPToHeaderLinkCreator._split_base_path_and_filename(cpp_file_path)
        path_spits = base_path.split(CPPToHeaderLinkCreator.CPP_FOLDER_NAME)
        assert len(path_spits) == 2, f"{cpp_file_path} is expected to contain {CPPToHeaderLinkCreator.CPP_FOLDER_NAME} one time"
        module_path, code_path = path_spits
        return module_path, code_path, filename

    @staticmethod
    def _split_base_path_and_filename(file_path: str) -> Tuple[str, str]:
        """
        Splits the path into the base path and the filename (w/o ext)
        :param file_path: The full path to the file
        :return The base path and the file name without the ext
        """
        base_path, file_name = FileUtil.split_base_path_and_filename(file_path)
        return base_path, os.path.splitext(file_name)[0]

    @staticmethod
    def _get_all_cpp_files_in_dir(dir_path: str) -> List[str]:
        """
        Gets all the cpp files in a directory
        :param dir_path: The path to the directory
        :return a list of all cpp files in a directory
        """
        return GCodeFile.get_all_code_files_with_ext(dir_path, {f".{CPPToHeaderLinkCreator.CPP_EXT}"})
