import os
import pickle
import shutil
from copy import deepcopy
from os.path import splitext
from typing import Any, Callable, Dict, IO, List, Optional, Tuple, Type, Union

import yaml
from yaml.dumper import Dumper
from yaml.loader import Loader, SafeLoader

from tgen.common.constants.deliminator_constants import EMPTY_STRING, F_SLASH
from tgen.common.constants.path_constants import CURRENT_PROJECT_PARAM, DATA_PATH_PARAM, MODEL_PARAM, OUTPUT_PATH_PARAM, PROJ_PATH, \
    ROOT_PATH_PARAM, \
    USER_SYM
from tgen.common.util.json_util import JsonUtil
from tgen.common.util.logging.logger_manager import logger

CODE_EXTENSIONS = ["CPP", "SH", "C", "HPP", "JS", "CS", "RB", "PHP",
                   "SWIFT", "M", "GO", "RS", "KT", "TS", "HTML", "CSS",
                   "PL", "R", "PY", "JAVA", "VUE", "CC"]

ENV_REPLACEMENT_VARIABLES = [DATA_PATH_PARAM, ROOT_PATH_PARAM, OUTPUT_PATH_PARAM, CURRENT_PROJECT_PARAM, MODEL_PARAM]
import numpy as np


class FileUtil:
    JSON_EXT = "json"
    CSV_EXT = "csv"
    YAML_EXT = "yaml"
    NUMPY_EXT = "npy"

    @staticmethod
    def get_directory_path(file_path: str) -> str:
        """
        Gets the lowest level directory path from the file path (if it's already a directory, just return as is)
        :param file_path: The path to file/directory
        :return: The path to the lowest level directory
        """
        if FileUtil.is_file(file_path):
            return os.path.join(*os.path.split(file_path)[:-1])
        return file_path

    @staticmethod
    def is_file(path: str) -> bool:
        """
        Returns whether the given path contains a filename at the end or not
        :param path: The path
        :return: True if the given path contains a filename at the end
        """
        if FileUtil.get_file_ext(path):
            return True
        return False

    @staticmethod
    def get_file_ext(path: str) -> str:
        """
        Gets the file extension for a given path
        :param path: The path to get the extension for
        :return: The extension of the file
        """
        return os.path.splitext(path)[-1]

    @staticmethod
    def create_dir_safely(output_path: str, *additional_path_parts) -> str:
        """
        Makes a directory, by first checking if the directory exists
        :return: the output path
        """
        if additional_path_parts:
            output_path = os.path.join(output_path, *additional_path_parts)
        output_path = FileUtil.get_directory_path(output_path)  # ensure is a directory
        os.makedirs(output_path, exist_ok=True)
        return output_path

    @staticmethod
    def read_file(file_path: str, raise_exception: bool = True) -> Optional[str]:
        """
        Reads file at given path if exists.
        :param file_path: Path of the file to read.
        :param raise_exception: If True, raises an exception if reading fails
        :return: The content of the file.
        """
        try:
            with open(file_path) as file:
                file_content = file.read()
                return file_content
        except Exception as e:
            logger.exception(f"Failed reading file: {file_path}")
            if raise_exception:
                raise e
            return None

    @staticmethod
    def read_file_lines(file_path: str) -> List[str]:
        """
        Reads file at given path if exists.
        :param file_path: Path of the file to read.
        :return: The content of the file.
        """
        with open(file_path) as file:
            return file.readlines()

    @staticmethod
    def get_env_replacements(env_variables: List[str]) -> Dict[str, str]:
        """
        :return: Dictionary of environment variables to their values.
        """
        replacements = {}
        for replacement_path in env_variables:
            path_value = os.environ.get(replacement_path, None)
            if path_value:
                path_key = "[%s]" % replacement_path
                replacements[path_key] = os.path.expanduser(path_value)
        return replacements

    @staticmethod
    def get_file_list(data_path: str, exclude: List[str] = None, exclude_ext: List[str] = None) -> List[str]:
        """
        Gets list of files in the data path
        :param data_path: the path to the data
        :param exclude: list of strings to exclude
        :param exclude_ext: list of file extensions to exclude
        :return: a list of files
        """
        if exclude is None:
            exclude = [".DS_Store"]
        if exclude_ext is None:
            exclude_ext = []
        if os.path.isfile(data_path):
            files = [data_path]
        elif os.path.isdir(data_path):
            files = list(filter(lambda f: not (f in exclude or splitext(f)[1] in exclude_ext), os.listdir(data_path)))
            files = list(map(lambda f: os.path.join(data_path, f), files))
            all_files = []
            for file in files:
                all_files.extend(FileUtil.get_file_list(file, exclude=exclude, exclude_ext=exclude_ext))
            files = all_files
        else:
            raise Exception("Unable to read pretraining data file path " + data_path)
        return files

    @staticmethod
    def expand_paths(paths: Union[List, Dict, str], replacements: Dict[str, str] = None,
                     use_abs_paths: bool = True):
        """
        For every string found in value, if its a path its expanded completed path
        :param paths: List, Dict, or String containing one or more paths.
        :param replacements: Dictionary from source to target string replacements in paths.
        :param use_abs_paths: If True, returns the absolute path
        :return: Same type as value, but with its content processed.
        """

        def expand(path: str, replacements: Dict[str, str] = None):
            """
            Performs replacements on path.
            :param path: The path possibly containing keys.
            :param replacements: They keys and values to be replaced with.
            :return: The processed path.
            """
            if replacements:
                for k, v in replacements.items():
                    path = path.replace(k, v)
            path = os.path.expanduser(path)
            if use_abs_paths:
                path = FileUtil.get_path_relative_to_proj_path(path)
            return path

        return FileUtil.perform_function_on_paths(paths, expand, replacements=replacements)

    @staticmethod
    def collapse_paths(paths: Union[List, Dict, str], replacements: Dict[str, str] = None):
        """
        For every string found in value, if its a path its collapsed into a shorter form
        :param paths: List, Dict, or String containing one or more paths.
        :param replacements: Dictionary from source to target string replacements in paths.
        :return: Same type as value, but with its content processed.
        """

        def collapse(path: str, replacements: Dict[str, str] = None):
            """
            Performs replacements on path.
            :param path: The path possibly containing keys.
            :param replacements: They keys and values to be replaced with.
            :return: The processed path.
            """
            if replacements:
                path2var = {v: k for k, v in replacements.items()}
                ordered_paths = FileUtil.order_paths_by_overlap(list(replacements.values()), reverse=True)
                for path2replace in ordered_paths:
                    path = path.replace(path2replace, path2var[path2replace])
            if os.path.isabs(path):
                path = os.path.relpath(path, PROJ_PATH)
            return path

        return FileUtil.perform_function_on_paths(paths, collapse, replacements=replacements)

    @staticmethod
    def perform_function_on_paths(paths: Union[List, Dict, str], func: Callable, replacements: Dict[str, str] = None, **kwargs):
        """
        For every string found in value, if its a path its collapsed into a shorter form
        :param paths: List, Dict, or String containing one or more paths.
        :param func: Function to perform
        :param replacements: Dictionary from source to target string replacements in paths.
        :return: Same type as value, but with its content processed.
        """
        if replacements is None:
            replacements = FileUtil.get_env_replacements(ENV_REPLACEMENT_VARIABLES)
        if isinstance(paths, list):
            return [FileUtil.perform_function_on_paths(v, func, replacements=replacements, **kwargs) for v in paths]
        if isinstance(paths, dict):
            return {k: FileUtil.perform_function_on_paths(v, func, replacements=replacements, **kwargs) for k, v in paths.items()}
        if isinstance(paths, str):
            paths = func(paths, replacements=replacements, **kwargs)
        return paths

    @staticmethod
    def get_path_relative_to_proj_path(abspath) -> str:
        """
        Gets the path relative to the proj path
        :param abspath: The absolute path
        :return: The path relative to the proj path
        """
        return os.path.normpath(os.path.join(PROJ_PATH, abspath))

    @staticmethod
    def get_user_path() -> str:
        """
        Gets the current users home path
        :return: The current users home path
        """
        return os.path.expanduser(USER_SYM)

    @staticmethod
    def order_paths_by_overlap(paths: List[str], reverse: bool = False) -> List[str]:
        """
        Orders the paths so that base paths come before any branches (e.g. root before root/dir1 before root/dir1/dir2)
        :param paths: The list of unordered paths
        :param reverse: If True, returns the most overlap to the least (e.g. root AFTER root/dir1 AFTEr root/dir1/dir2)
        :return: The ordered paths
        """
        orderings = {}
        for a in paths:
            ordered = [a]
            for b in paths:
                if a == b:
                    continue
                if a in b:
                    ordered.append(b)
                elif b in a:
                    ordered.insert(0, b)
            orderings[a] = ordered
        final_orderings = []
        for path, ordering in orderings.items():
            if path == ordering[0]:
                if reverse:
                    ordering.reverse()
                final_orderings.extend(ordering)
        return final_orderings

    @staticmethod
    def write(content: Union[str, Dict], output_file_path: str):
        """
        Soon to be mock function for saving files to storage but using the filesystem instead.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        if isinstance(content, dict):
            content = JsonUtil.dict_to_json(content)
        with FileUtil.safe_open_w(output_file_path) as file:
            file.write(content)

    @staticmethod
    def safe_open_w(path: str) -> IO:
        """
        Opens given file without throwing exception if it does not exist
        :param path: the path to file
        :return: the file object
        """
        FileUtil.create_dir_safely(os.path.dirname(path))
        return open(path, 'w')

    @staticmethod
    def delete_dir(dir_path: str) -> None:
        """
        Deletes folder and everything inside it if it exists.
        :param dir_path: The path to the folder.
        """
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def move_dir_contents(orig_path: str, new_path: str, delete_after_move: bool = False) -> None:
        """
        Moves the directory at the original path to the new path
        :param orig_path: the original path to move
        :param new_path: the new path to move the dir to
        :param delete_after_move: if True, deletes the original directory after moving all contents
        :return: None
        """
        FileUtil.create_dir_safely(new_path)
        for file in os.listdir(orig_path):
            file_path = os.path.join(orig_path, file)
            shutil.move(file_path, new_path)
        if delete_after_move:
            FileUtil.delete_dir(orig_path)

    @staticmethod
    def add_to_path(path: str, addition: str, index: int) -> str:
        """"
        Adds component to path at given index.
        :param path: The path to add component to.
        :param addition: The component to add to path.
        :param index: The index to add component in path.
        :return path with component added.
        """
        path = deepcopy(path)
        path_list = FileUtil.path_to_list(path)
        index = index if index >= 0 else len(path_list) + index + 1
        path_list.insert(index, addition)
        if os.path.isabs(path):
            path_list.insert(0, F_SLASH)
        return os.path.join(*path_list)

    @staticmethod
    def path_to_list(path: str) -> List[str]:
        """
        Creates list of folders and files in path.
        :param path: The path to split into components.
        :return: List of components creating path.
        """
        path = os.path.normpath(path)
        return [p for p in path.split(os.sep) if p != ""]

    @staticmethod
    def ls_dir(path: str, **kwargs):
        """
        Gets the directories at the current path
        :param path: Path to the directory
        :param kwargs: Additional parameters
        :return: The list of directories at the path
        """
        function_kwargs = {"add_base_path": True}
        function_kwargs.update(kwargs)
        return FileUtil.ls_filter(path, f=lambda f: os.path.isdir(f), **function_kwargs)

    @staticmethod
    def ls_filter(base_path: str, f: Callable[[str], bool] = None, ignore: List[str] = None, add_base_path: bool = False) -> List[str]:
        """
        List and filters files in path.
        :param base_path: The path to list its contents.
        :param f: The filtering function to select entities or not.
        :param ignore: List of files to ignored completely.
        :param add_base_path: Whether listed files should be complete paths.
        :return: List of files in path.
        """
        if f is None:
            f = lambda s: s
        if ignore is None:
            ignore = []
        results = os.listdir(base_path)
        results = list(filter(lambda p: p not in ignore, results))
        if add_base_path:
            results = list(map(lambda r: os.path.join(base_path, r), results))
        results = list(filter(lambda p: f(p), results))
        return results

    @staticmethod
    def split_base_path_and_filename(file_path: str) -> Tuple[str, str]:
        """
        Splits the filepath into base directory and the filename
        :param file_path: The path to the file
        :return: A tuple containing the base directory and the filename
        """
        return os.path.dirname(file_path), os.path.basename(file_path)

    @staticmethod
    def get_file_name(script_path: str, n_parents: int = 0, delimiter: str = "-"):
        """
        Returns the name of the file referenced in path.
        :param script_path: Path to script file whose name is returned.
        :param n_parents: The number of directories above file to include.
        :param delimiter: The delimiter to use if parents included.
        :return: The name of the script.
        """
        base_name, _ = os.path.splitext(script_path)
        components = []
        for i in range(n_parents + 1):  # file name + parents
            base_name, file_name = os.path.split(base_name)
            components.append(file_name)
        components.reverse()
        return delimiter.join(components)

    @staticmethod
    def get_all_paths(dir_path: Union[List[str], str], condition: Callable = None) -> List[str]:
        """
        Reads all code files in directory with allowed extensions.
        :param dir_path: Path to directory where code files live
        :param condition: A callable that returns True if the filepath should be included
        :return: List containing all code file paths.
        """
        if isinstance(dir_path, list):
            paths = set()
            for p in dir_path:
                paths.update(set(FileUtil.get_all_paths(p)))
            return list(paths)
        condition = condition if condition is not None else lambda x: True
        file_paths = []
        for subdir, dirs, files in os.walk(dir_path):
            for f in files:
                if condition(f):
                    file_paths.append(os.path.join(subdir, f))
        return file_paths

    @staticmethod
    def delete_file_safely(file_path: str) -> None:
        """
        Deletes a file if it exists, else does nothing
        :param file_path: The path to the file
        :return: None
        """
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def read_yaml(file_path: str, loader: Type[Loader] = None) -> Dict:
        """
        Reads a yaml file at given path if exists.
        :param file_path: Path of the file to read.
        :param loader: The loader to use for loading the yaml file
        :return: The content of the file.
        """
        loader = SafeLoader if loader is None else loader
        with open(file_path, 'r') as file:
            return yaml.load(file, Loader=loader)

    @staticmethod
    def write_yaml(content: Any, output_file_path: str, dumper: Type[Dumper] = None):
        """
        Saves yaml to given file
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        dumper = Dumper if dumper is None else dumper
        FileUtil.create_dir_safely(output_file_path)
        output_file_path = os.path.expanduser(output_file_path)
        with open(output_file_path, 'w') as file:
            yaml.dump(content, file, Dumper=dumper)

    @staticmethod
    def read_pickle(file_path: str) -> Any:
        """
        Reads a pickled obj
        :param file_path: Path of the file to read.
        :return: The content of the file.
        """
        with open(file_path, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def write_pickle(content: Any, output_file_path: str) -> None:
        """
        Saves yaml to given file
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        with open(output_file_path, 'wb') as file:
            pickle.dump(content, file)
            yaml.dump(content, file)

    @staticmethod
    def save_numpy(array: Union[np.array, list], file_path: str) -> None:
        """
        Saves a numpy array to a file
        :param array: The np array or python list to save
        :param file_path: Where to save the array to
        :return: None
        """
        FileUtil.create_dir_safely(file_path)
        if not isinstance(array, np.ndarray):
            array = np.asarray(array)
        np.save(file_path, array)

    @staticmethod
    def load_numpy(file_path: str) -> np.array:
        """
        Loads a numpy array from a file
        :param file_path: Where to load the array from
        :return: The numpy array
        """
        file_path = FileUtil.add_ext(file_path, FileUtil.NUMPY_EXT)
        return np.load(file_path)

    @staticmethod
    def add_ext(file_path: str, ext: str) -> str:
        """
        Adds a file ext to the path if it doesn't have it already
        :param file_path: The path to the file
        :param ext: The extension to include
        :return: The filepath with the ext
        """
        full_path = os.path.splitext(file_path)[0] + os.path.extsep + ext
        return full_path

    @staticmethod
    def is_code(path_or_ext: str) -> bool:
        """
        Determines if a file is a code file based on the ext
        :param path_or_ext: The ext of the file or the full path
        :return: The summary to use
        """
        if not isinstance(path_or_ext, str):
            path_or_ext = str(path_or_ext)
        tmp = os.path.splitext(path_or_ext)
        if tmp[-1]:
            path_or_ext = tmp[-1].replace(os.extsep, EMPTY_STRING)
        path_or_ext = path_or_ext.upper()
        if path_or_ext in CODE_EXTENSIONS:
            return True
        return False

    @staticmethod
    def filter_by_ext(file_names: List[str], ext: Union[str, List[str]]) -> List[str]:
        """
        Returns the artifact ids with given extension.
        :param file_names: The file names to filter.
        :param ext: The extension(s) of the files to keep.
        :return: List of files ending with extension.
        """
        if isinstance(ext, str):
            ext = [ext]
        code_ids = [p for p in file_names for e in ext if p.endswith(e)]
        return code_ids

    @staticmethod
    def get_file_base_name(file_path: str):
        """
        Returns the file name without extension.
        :param file_path: The path to the file.
        :return: The name of the file without extension.
        """
        file_name = os.path.basename(file_path)
        file_name_base, file_ext = os.path.splitext(file_name)
        return file_name_base

    @staticmethod
    def split_into_parts(file_path: str) -> List[str]:
        """
        Splits path into list of directories and file name (last element).
        :param file_path: The path to split.
        :return: Parts that make up the path.
        """
        file_path = os.path.normpath(file_path)
        parts = file_path.split(os.sep)
        return parts

    @staticmethod
    def get_str_or_read(path: str):
        """
        Returns file content if path otherwise string is returned.
        :param path: The path to a file or a string.
        :return: The string value of the file or string.
        """
        try:
            return FileUtil.read_file(path)
        except Exception as e:
            return path
