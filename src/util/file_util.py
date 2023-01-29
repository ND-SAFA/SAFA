import json
import os
import shutil
from copy import deepcopy
from typing import Dict, IO, List, Union

from util.json_util import JsonUtil
from util.uncased_dict import UncasedDict


class FileUtil:

    @staticmethod
    def create_dir_safely(output_path: str, *additional_path_parts) -> str:
        """
        Makes a directory, by first checking if the directory exists
        :return: the output path
        """
        if additional_path_parts:
            output_path = os.path.join(output_path, *additional_path_parts)
        os.makedirs(output_path, exist_ok=True)
        return output_path

    @staticmethod
    def read_file(file_path: str):
        """
        Reads file at given path if exists.
        :param file_path: Path of the file to read.
        :return: The content of the file.
        """
        with open(file_path) as file:
            return file.read()

    @staticmethod
    def read_json_file(file_path: str, as_uncased_dict: bool = False) -> Union[Dict, UncasedDict]:
        """
        Reads JSON from file at path.
        :param file_path: Path to JSON file.
        :param as_uncased_dict: Whether to convert output to uncased dict
        :return: Dictionary content of file.
        """
        with open(file_path) as file:
            content = json.load(file)
        return UncasedDict(content) if as_uncased_dict else content

    @staticmethod
    def get_file_list(data_path: str, exclude: List[str] = None) -> List[str]:
        """
        Gets list of files in the data path
        :param data_path: the path to the data
        :param exclude: list of strings to exclude
        :return: a list of files
        """
        if exclude is None:
            exclude = [".DS_Store"]
        if os.path.isfile(data_path):
            files = [data_path]
        elif os.path.isdir(data_path):
            files = list(filter(lambda f: f not in exclude, os.listdir(data_path)))
            files = list(map(lambda f: os.path.join(data_path, f), files))
        else:
            raise Exception("Unable to read pretraining data file path " + data_path)
        return files

    @staticmethod
    def expand_paths_in_dictionary(value: Union[List, Dict, str], replacements: Dict[str, str] = None):
        """
        For every string found in value, if its a path its expanded and
        :param value: List, Dict, or String containing one or more values.
        :param replacements: Dictionary from source to target string replacements in paths.
        :return: Same type as value, but with its content processed.
        """
        if isinstance(value, list):
            return [FileUtil.expand_paths_in_dictionary(v, replacements=replacements) for v in value]
        if isinstance(value, dict):
            return {k: FileUtil.expand_paths_in_dictionary(v, replacements=replacements) for k, v in value.items()}
        if isinstance(value, str):
            if "~" in value:
                return os.path.expanduser(value)
            if replacements:
                for k, v in replacements.items():
                    value = value.replace(k, v)
        return value

    @staticmethod
    def save_to_file(content: Union[str, Dict], output_file_path: str):
        """
        Soon to be mock function for saving files to storage but using the filesystem instead.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        if isinstance(content, dict):
            content = JsonUtil.dict_to_json(content)
        FileUtil.create_dir_safely(os.path.dirname(output_file_path))
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
            path_list.insert(0, "/")
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
